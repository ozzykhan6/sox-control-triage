# SOX Control Triage Tool - Validation Test Library
#
# Purpose: 15 controls spanning preventive, detective, corrective, ambiguous
# edge cases, and deliberately poor-quality input. Used to validate that the
# tool's classifications are reasonable and consistent, and to give the
# builder (Ozzy) specific, defensible examples to reference in interviews.
#
# How to use:
# 1. Run each control_text through the live tool (Mock Mode OFF, v2 prompt).
# 2. Record the actual output in the companion VALIDATION_METHODOLOGY.md
#    results table.
# 3. Compare actual control_type to expected_control_type. For risk_rating
#    and framework_alignment, judgment calls are expected. Note whether
#    Claude's reasoning is defensible, not whether it matches word for word.

TEST_LIBRARY = [

    # ---------------- PREVENTIVE (4) ----------------
    {
        "id": "P-01",
        "category": "Preventive",
        "name": "Vendor Master File Change Approval",
        "control_text": (
            "Before any change to vendor banking details or payment terms in the "
            "vendor master file, the change request must be approved by an AP "
            "supervisor who did not initiate the request. The system routes all "
            "vendor master changes to a pending queue and blocks the change from "
            "taking effect until approval is logged."
        ),
        "expected_control_type": "Preventive",
        "expected_risk_tier": "High",
        "rationale": (
            "Vendor master changes are a classic fraud vector (fictitious vendor, "
            "redirected payments). The control blocks the change before it takes "
            "effect, which is definitionally preventive, and the fraud risk "
            "justifies a High rating even though the control design is sound."
        ),
    },
    {
        "id": "P-02",
        "category": "Preventive",
        "name": "System-Enforced Segregation of Duties (SAP)",
        "control_text": (
            "SAP security roles are configured so that no single user can both "
            "create a new vendor and post a payment to that vendor. Role "
            "conflicts are enforced at the system level through mutually "
            "exclusive authorization objects."
        ),
        "expected_control_type": "Preventive",
        "expected_risk_tier": "Medium",
        "rationale": (
            "Automated SoD enforcement is strong preventive design. Residual risk "
            "sits in role provisioning errors or emergency access overrides, "
            "which is why Medium rather than Low is defensible."
        ),
    },
    {
        "id": "P-03",
        "category": "Preventive",
        "name": "Standard Journal Entry Template Restricting GL Accounts",
        "control_text": (
            "Recurring manual journal entries must be entered using a "
            "pre-configured template that restricts entries to a defined list "
            "of GL accounts relevant to that entry type. The system rejects any "
            "entry attempting to post to an account outside the template."
        ),
        "expected_control_type": "Preventive",
        "expected_risk_tier": "Medium",
        "rationale": (
            "System-enforced restriction before posting is preventive. Medium "
            "risk reflects that templates must be maintained and could become "
            "outdated as the chart of accounts changes."
        ),
    },
    {
        "id": "P-04",
        "category": "Preventive",
        "name": "Purchase Order Approval Matrix by Dollar Threshold",
        "control_text": (
            "Purchase orders route for approval based on a tiered dollar "
            "threshold matrix: under $10,000 requires department manager "
            "approval, $10,000 to $100,000 requires director approval, and "
            "above $100,000 requires VP approval. The system will not release "
            "a PO to the vendor until the required approval level is met."
        ),
        "expected_control_type": "Preventive",
        "expected_risk_tier": "Medium",
        "rationale": (
            "Tiered pre-approval before commitment is preventive. Medium risk "
            "given reliance on correct threshold configuration and approver "
            "diligence rather than Low, since manual judgment is still involved."
        ),
    },

    # ---------------- DETECTIVE (4) ----------------
    {
        "id": "D-01",
        "category": "Detective",
        "name": "Monthly Bank Reconciliation Review",
        "control_text": (
            "Each month, the accounting team prepares a bank reconciliation "
            "comparing the general ledger cash balance to the bank statement. "
            "A second reviewer, the Assistant Controller, reviews the "
            "reconciliation and supporting reconciling items, and signs off "
            "within five business days of month-end close."
        ),
        "expected_control_type": "Detective",
        "expected_risk_tier": "Medium",
        "rationale": (
            "The reconciliation happens after transactions post, so it detects "
            "rather than prevents discrepancies. Medium reflects the monthly "
            "cadence, a discrepancy could persist up to a month before catch."
        ),
    },
    {
        "id": "D-02",
        "category": "Detective",
        "name": "Quarterly User Access Recertification (ITGC)",
        "control_text": (
            "Every quarter, application owners review the full list of users "
            "with access to the financial reporting system and confirm each "
            "user's access is still appropriate for their current role. Any "
            "inappropriate access identified is removed within five business "
            "days, and the completed review is retained as evidence."
        ),
        "expected_control_type": "Detective",
        "expected_risk_tier": "Medium",
        "rationale": (
            "Classic ITGC detective control. Close to the app's own built-in "
            "demo sample, useful as a consistency check against the tool's "
            "existing hardcoded mock output for the same scenario."
        ),
    },
    {
        "id": "D-03",
        "category": "Detective",
        "name": "Exception Report Review for Duplicate Payments",
        "control_text": (
            "The AP system generates a weekly exception report flagging "
            "potential duplicate payments based on matching vendor, invoice "
            "number, and amount. The AP manager reviews the report, "
            "investigates each flagged item, and documents resolution before "
            "the following week's report is generated."
        ),
        "expected_control_type": "Detective",
        "expected_risk_tier": "Medium",
        "rationale": (
            "Payments have already occurred by the time the report is reviewed, "
            "so this detects rather than prevents. Weekly cadence limits "
            "exposure window, supporting Medium over High."
        ),
    },
    {
        "id": "D-04",
        "category": "Detective",
        "name": "Flux Analysis of P&L Accounts",
        "control_text": (
            "During financial close, the FP&A team performs a variance analysis "
            "comparing current period P&L account balances to prior period and "
            "budget. Variances exceeding 10% or $100,000 require a documented "
            "explanation from the account owner before the close is finalized."
        ),
        "expected_control_type": "Detective",
        "expected_risk_tier": "Low",
        "rationale": (
            "Well-established detective control with a clear quantitative "
            "threshold and a gate before close is final, supporting Low to "
            "Medium depending on how strictly the reviewer weighs the fact "
            "that it still occurs after entries post."
        ),
    },

    # ---------------- CORRECTIVE (3) ----------------
    {
        "id": "C-01",
        "category": "Corrective",
        "name": "Remediation Tracking for Control Deficiencies",
        "control_text": (
            "When internal audit or management identifies a control "
            "deficiency, it is logged in a central tracker with an assigned "
            "owner and remediation deadline. Internal audit follows up monthly "
            "until the deficiency is remediated and retests the control before "
            "closing the item."
        ),
        "expected_control_type": "Corrective",
        "expected_risk_tier": "Medium",
        "rationale": (
            "Exists specifically to fix identified problems after the fact, "
            "the textbook definition of corrective. Good one to lead with "
            "since corrective controls are underrepresented in most sample "
            "sets and show range."
        ),
    },
    {
        "id": "C-02",
        "category": "Corrective",
        "name": "Error Correction Workflow for Rejected Invoices",
        "control_text": (
            "Invoices rejected by the three-way match process are routed to a "
            "correction queue. AP staff investigate the discrepancy, correct "
            "the underlying data or obtain a corrected invoice, and resubmit "
            "for matching. A supervisor reviews all corrections before "
            "resubmission is approved."
        ),
        "expected_control_type": "Corrective",
        "expected_risk_tier": "Low",
        "rationale": (
            "Good edge case for discussion. Could arguably be framed as an "
            "extension of the preventive three-way match, but the action "
            "itself, correcting and resubmitting, is corrective in nature. "
            "Useful in interviews to show nuanced thinking."
        ),
    },
    {
        "id": "C-03",
        "category": "Corrective",
        "name": "Post-Close Adjusting Entry Process",
        "control_text": (
            "When a misstatement is identified after financial close, an "
            "adjusting entry is prepared with a memo describing the root cause, "
            "approved by the Controller, and disclosed to the audit committee "
            "if the amount exceeds the materiality threshold."
        ),
        "expected_control_type": "Corrective",
        "expected_risk_tier": "High",
        "rationale": (
            "Post-close misstatement correction carries real financial "
            "reporting risk, and materiality-based audit committee disclosure "
            "signals this is treated as high-risk in practice."
        ),
    },

    # ---------------- AMBIGUOUS EDGE CASES (2) ----------------
    {
        "id": "E-01",
        "category": "Edge Case",
        "name": "Three-Way Match with Manual Override",
        "control_text": (
            "The system automatically matches purchase order, receipt, and "
            "invoice before releasing payment. If the match is within a 5% "
            "tolerance, payment releases automatically. If outside tolerance, "
            "the invoice routes to an AP manager who investigates and can "
            "manually approve the override before payment releases."
        ),
        "expected_control_type": "Preventive (with detective characteristics)",
        "expected_risk_tier": "Medium",
        "rationale": (
            "Intentionally ambiguous. The automated match is preventive, but "
            "the manual override path functions more like a detective review "
            "of an exception. Use this one to test whether Claude picks one "
            "classification confidently or hedges, and to discuss in "
            "interviews as an example of where auditor judgment adds value "
            "beyond the tool's single-label output."
        ),
    },
    {
        "id": "E-02",
        "category": "Edge Case",
        "name": "Manager Review of System-Generated Report Before Posting",
        "control_text": (
            "Before payroll is submitted for processing, the payroll manager "
            "reviews a system-generated pre-submission report comparing this "
            "period's payroll to the prior period, flagging any employee whose "
            "pay changed by more than 15%. Flagged items must be resolved "
            "before the payroll manager releases the batch."
        ),
        "expected_control_type": "Preventive",
        "expected_risk_tier": "Medium",
        "rationale": (
            "Ambiguous because it has a detective-style review mechanism "
            "(comparing to prior period, flagging variances) but occurs "
            "before money moves, which pulls it toward preventive. A "
            "reasonable model could argue either way. Good one to have ready "
            "for 'why did the tool classify this the way it did' questions."
        ),
    },

    # ---------------- POOR-QUALITY INPUT (2) ----------------
    {
        "id": "X-01",
        "category": "Poor Input",
        "name": "Vague Description",
        "control_text": "We check things before they go through.",
        "expected_control_type": "Not reliably determinable",
        "expected_risk_tier": "Not reliably determinable",
        "rationale": (
            "Deliberately underspecified. The point is not to see if the tool "
            "gets it 'right', there is no right answer here. The point is to "
            "observe whether the tool overstates confidence on bad input or "
            "appropriately signals uncertainty. Best example for discussing "
            "the tool's limitations honestly."
        ),
    },
    {
        "id": "X-02",
        "category": "Poor Input",
        "name": "Incomplete Description",
        "control_text": "Manager reviews stuff monthly.",
        "expected_control_type": "Not reliably determinable",
        "expected_risk_tier": "Not reliably determinable",
        "rationale": (
            "Similar purpose to X-01. If the tool confidently returns a "
            "specific High/Medium/Low rating and a detailed test procedure "
            "list for this input, that is a real finding worth naming in an "
            "interview: the tool does not currently flag when input is too "
            "thin to assess, a legitimate 'what would you improve next' answer."
        ),
    },
]

if __name__ == "__main__":
    for item in TEST_LIBRARY:
        print(f"[{item['id']}] {item['category']}: {item['name']}")
    print(f"\nTotal test cases: {len(TEST_LIBRARY)}")
