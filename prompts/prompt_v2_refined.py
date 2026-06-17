# VERSION 2 - Production prompt.
# Structured, constrained, and returns strict JSON.
# See README for the full v1 vs v2 iteration story.


EXPECTED_KEYS = [
    "control_type",
    "framework_alignment",
    "risk_rating",
    "plain_english_summary",
    "recommended_test_procedures",
]
def build_prompt_v2(control_description):
    return f"""You are a SOX / ICFR controls specialist with deep experience in COSO 2013 and PCAOB Auditing Standard AS 2201. Analyze the internal control described below and return EXACTLY the following five fields.

FIELD DEFINITIONS:

1. control_type: Must be exactly one of: "Preventive", "Detective", or "Corrective".

2. framework_alignment: Identify the primary COSO 2013 component and add a brief PCAOB relevance note. One to two sentences.

3. risk_rating: Must start with exactly one of: "High", "Medium", or "Low", followed by " - " and one sentence of rationale.

4. plain_english_summary: Explain what this control does in plain English. Two to three sentences.

5. recommended_test_procedures: A list of 3 to 5 concrete test steps an auditor would execute.

OUTPUT FORMAT:
- Return ONLY a single valid JSON object.
- Do NOT include any text before or after the JSON.
- Use exactly these keys: control_type, framework_alignment, risk_rating, plain_english_summary, recommended_test_procedures.

CONTROL TO ANALYZE:
\"\"\"
{control_description}
\"\"\"
"""