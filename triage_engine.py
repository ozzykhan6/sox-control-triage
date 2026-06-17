import json
import os

from prompts.prompt_v1_generic import build_prompt_v1
from prompts.prompt_v2_refined import build_prompt_v2, EXPECTED_KEYS

MODEL_NAME = "claude-haiku-4-5-20251001"
MAX_TOKENS = 1024
def analyze_control(control_description, api_key, prompt_version="v2"):
    if not control_description or not control_description.strip():
        raise ValueError("Please enter a control description before running the analysis.")
    if not api_key or not api_key.strip():
        raise ValueError("No API key found. Add ANTHROPIC_API_KEY to your .env file, or turn on Mock Mode.")

    try:
        import anthropic
    except ImportError:
        raise RuntimeError("The anthropic package is not installed. Run: pip install -r requirements.txt")

    if prompt_version == "v1":
        prompt = build_prompt_v1(control_description)
    else:
        prompt = build_prompt_v2(control_description)

    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as exc:
        raise RuntimeError(f"Claude API call failed: {exc}")

    raw_text = "".join(
        block.text for block in response.content if getattr(block, "type", None) == "text"
    ).strip()

    return _parse_response(raw_text, prompt_version)
def mock_analyze(control_description, sample_label=None):
    if sample_label and sample_label in _MOCK_RESPONSES:
        return _MOCK_RESPONSES[sample_label]
    return _MOCK_GENERIC
def _parse_response(raw_text, prompt_version):
    if prompt_version == "v1":
        return {
            "control_type": "(v1 prompt returns unstructured output)",
            "framework_alignment": "(v1 prompt returns unstructured output)",
            "risk_rating": "(v1 prompt returns unstructured output)",
            "plain_english_summary": raw_text,
            "recommended_test_procedures": [
                "Switch to the v2 prompt for structured output."
            ],
        }

    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        raise RuntimeError("Could not parse the model response as JSON. Raw response:\n\n" + raw_text)

    result = {}
    for key in EXPECTED_KEYS:
        result[key] = data.get(key, "(not returned by model)")

    procs = result["recommended_test_procedures"]
    if isinstance(procs, str):
        result["recommended_test_procedures"] = [procs]
    elif not isinstance(procs, list):
        result["recommended_test_procedures"] = [str(procs)]

    return result
_MOCK_RESPONSES = {
    "1. Quarterly User Access Review (ITGC)": {
        "control_type": "Detective",
        "framework_alignment": "COSO 2013 - Control Activities. This is an IT general control and a key area in PCAOB AS 2201 testing, since the integrity of ITGCs underpins reliance on automated controls.",
        "risk_rating": "Medium - The review is periodic and reliant on reviewer diligence, so inappropriate access could persist for up to a quarter before detection.",
        "plain_english_summary": "Every three months, someone checks the full list of people who can access the financial system and confirms each person still needs that access. Anyone who should not have access gets removed, and proof of the check is kept on file.",
        "recommended_test_procedures": [
            "Obtain the population of quarterly access reviews and select a sample of quarters for testing.",
            "Inspect the user access listing, reviewer sign-off, and review date to confirm the review was complete and timely.",
            "For users flagged as inappropriate, confirm access was revoked within the five-business-day requirement.",
            "Compare a sample of terminated employees from HR records to the access listing.",
        ],
    },
    "2. Journal Entry Approval Threshold (Financial Close)": {
        "control_type": "Preventive",
        "framework_alignment": "COSO 2013 - Control Activities. This is a key business-process control over financial reporting and is highly relevant to PCAOB AS 2201 given the fraud risk associated with manual journal entries.",
        "risk_rating": "High - Manual journal entries are a recognized fraud and error vector, and the dollar threshold makes this a direct control over material misstatement.",
        "plain_english_summary": "Before a manual accounting entry is recorded, a second person who did not create it must approve it, and bigger entries need the Controller's sign-off. The system also blocks people from approving their own entries.",
        "recommended_test_procedures": [
            "Obtain the complete population of manual journal entries and reconcile to the general ledger.",
            "Select a sample above and below the $50,000 threshold and inspect evidence of independent approval.",
            "For entries at or above $50,000, inspect evidence of Controller approval.",
            "Confirm the system prevents a preparer from approving their own entry.",
        ],
    },
    "3. Three-Way Match Before Payment (Purchase-to-Pay)": {
        "control_type": "Preventive",
        "framework_alignment": "COSO 2013 - Control Activities. This is an automated application control in the purchase-to-pay cycle; its reliability depends on supporting ITGCs.",
        "risk_rating": "Medium - The match is automated and consistent, but tolerance thresholds and manual override introduce residual risk of improper payment.",
        "plain_english_summary": "Before paying a supplier, the system checks that the order, the goods received, and the invoice all agree. If they match closely enough, payment is approved automatically; if not, a manager must investigate first.",
        "recommended_test_procedures": [
            "Perform a walkthrough of the three-way match configuration to understand the automated control.",
            "Inspect system configuration to confirm the under-5% variance tolerance is set correctly.",
            "Select a sample of paid invoices and reperform the three-way match.",
            "For overridden invoices, inspect evidence of AP Manager approval before payment.",
        ],
    },
}

_MOCK_GENERIC = {
    "control_type": "Detective",
    "framework_alignment": "Mock Mode is ON. Turn it off and add an API key for a real analysis.",
    "risk_rating": "Medium - Illustrative rating only. Turn off Mock Mode for a real assessment.",
    "plain_english_summary": "This is sample output shown because Mock Mode is enabled. No API call was made.",
    "recommended_test_procedures": [
        "Obtain the full population of control occurrences and select a sample.",
        "Inspect evidence supporting each sampled occurrence.",
        "Reperform or recalculate a sample to evaluate operating effectiveness.",
        "Corroborate inquiry responses with independent documentation.",
    ],
}