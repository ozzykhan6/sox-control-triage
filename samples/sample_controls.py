# Three sample SOX controls used to pre-load the input box.
# One from each major category: ITGC, financial close, and purchase-to-pay.
SAMPLE_CONTROLS = {
    "1. Quarterly User Access Review (ITGC)": (
        "On a quarterly basis, the IT Security Administrator generates a complete "
        "listing of all users with access to the SAP ERP financial modules. "
        "Each application owner reviews the listing to confirm that every user's "
        "access remains appropriate and that no terminated employees retain access. "
        "Any access identified as inappropriate is revoked within five business days. "
        "Evidence of the review, including sign-off and remediation tickets, "
        "is retained in the GRC tool for audit support."
    ), 
    "2. Journal Entry Approval Threshold (Financial Close)": (
        "All manual journal entries posted to the general ledger must be reviewed "
        "and approved by an individual independent of the preparer prior to posting. "
        "Manual journal entries with a value of $50,000 or greater require an "
        "additional level of approval by the Controller. The accounting system "
        "enforces segregation of duties by preventing the preparer from approving "
        "their own entry. Approved entries and supporting documentation are retained "
        "in the financial close system and reviewed monthly by the Accounting Manager."
    ),
    "3. Three-Way Match Before Payment (Purchase-to-Pay)": (
        "Prior to releasing payment to a vendor, the Accounts Payable system "
        "performs an automated three-way match between the approved purchase order, "
        "the goods receipt note, and the vendor invoice. Invoices that match within "
        "established tolerance thresholds of less than five percent variance are "
        "automatically approved for payment. Invoices that fail the match are routed "
        "to the Accounts Payable Manager for manual investigation and documented "
        "approval before any payment is released."
    ),
}
SAMPLE_LABELS = list(SAMPLE_CONTROLS.keys())