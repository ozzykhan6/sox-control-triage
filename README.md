# SOX Control Triage Tool
# SOX Control Triage Tool

An AI-assisted audit tool that analyzes SOX internal control descriptions and returns structured output: control type, framework alignment, risk rating, a plain-English summary, and recommended test procedures. Built with Streamlit and the Anthropic Claude API.
🔗 **Live app:** https://nextrend-sox-triage.streamlit.app
[Screenshot coming soon]

---

## How to run locally

```bash
# 1. Clone or download this folder

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/Scripts/activate  # Windows bash
# or: .venv\Scripts\activate   # Windows cmd

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key
cp .env.example .env
# Edit .env and paste your key from console.anthropic.com

# 5. Run the app
streamlit run app.py
```

Mock Mode is ON by default -- the app works immediately with no API key.

---

## The prompt iteration story

### v1 -- the first attempt
This works but produces inconsistent output -- sometimes prose, sometimes bullets, field names drift between runs. It cannot be parsed reliably into UI cards.

### v2 -- the production prompt

The refined prompt makes five changes:

1. Assigns a precise persona -- SOX/ICFR specialist grounded in COSO 2013 and PCAOB AS 2201
2. Defines all five output fields explicitly
3. Constrains allowed values -- Control Type must be Preventive, Detective, or Corrective
4. Requires strict JSON output so the app parses it into cards reliably
5. Uses real audit terminology throughout

The v1 prompt is kept in the repo intentionally to show this iteration. You can switch between them live using the Prompt Version dropdown.

---

## Why this project exists

This demonstrates AI-assisted audit automation -- taking a real, repetitive audit task and building a reliable tool around an LLM. It shows prompt engineering discipline, structured output parsing, graceful degradation via Mock Mode, and secrets hygiene. It sits at the intersection of SOX domain knowledge and practical AI engineering.