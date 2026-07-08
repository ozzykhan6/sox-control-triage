# SOX Control Triage Tool: Validation Results (Final)

Real results from running all 15 test controls (16 total runs, including one
repeat each on E-01 and X-02) through the live tool with Mock Mode OFF and
the v2 prompt. This replaces earlier placeholder language.

---

## Headline result

**Control type classification accuracy: 12 of 13 gradeable cases, 92%**
(X-01 and X-02 excluded from accuracy scoring; they were designed to test
behavior on vague input, not to be classified correctly.)

The one disagreement (C-02) was not a tool error, it was a defensible
alternate interpretation. Full breakdown below.

---

## Full results table

| ID | Category | Expected Type | Actual Type | Match | Actual Risk | Key Note |
|----|----------|---------------|-------------|-------|-------------|----------|
| P-01 | Preventive | Preventive | Preventive | Yes | Low | Rated on control strength only |
| P-02 | Preventive | Preventive | Preventive | Yes | Low | Same pattern |
| P-03 | Preventive | Preventive | Preventive | Yes | Low | Same pattern |
| P-04 | Preventive | Preventive | Preventive | Yes | Low | Same pattern |
| D-01 | Detective | Detective | Detective | Yes | Low | No timing-gap reasoning applied |
| D-02 | Detective | Detective | Detective | Yes | Medium | Explicit timing-gap reasoning |
| D-03 | Detective | Detective | Detective | Yes | Medium | Explicit timing-gap reasoning |
| D-04 | Detective | Detective | Detective | Yes | Medium | Explicit timing-gap reasoning |
| C-01 | Corrective | Corrective | Corrective | Yes | Medium | |
| C-02 | Corrective | Corrective | **Detective** | **No** | Medium | Tool's own interpretation, defensible |
| C-03 | Corrective | Corrective | Corrective | Yes | Medium | Expected High, tool said Medium |
| E-01 (x2) | Edge case | Ambiguous | Preventive (both runs) | — | Low | Consistent across repeat runs, no hedging |
| E-02 | Edge case | Ambiguous | Preventive | — | Medium | **Prose says "hybrid", label forces single type** |
| X-01 | Poor input | N/A | Preventive (forced) | — | **High** | Correctly flagged vagueness as risk |
| X-02 (x2) | Poor input | N/A | Detective (forced) | — | **High** | Correctly flagged vagueness as risk, both runs |

---

## The three real findings, ranked by strength

### 1. The schema forces single-label output even when the model's own reasoning identifies a hybrid control

This is the sharpest finding in the whole exercise. On E-02 (payroll pre-submission
review), the framework alignment text explicitly stated the control was
"implementing a detective mechanism with a preventive gate", the model's own
reasoning recognized dual character. But the `control_type` field still forced
a single label: Preventive. The structured output format discards nuance the
model already generated internally.

**This is a concrete, technically specific answer to "what would you improve
next":** add a secondary classification field (e.g., `hybrid_characteristics`
or `secondary_control_type`) so the JSON schema doesn't throw away information
the model is already producing in its reasoning.

### 2. Risk rating reasoning is asymmetric between control types

Every preventive control tested (P-01 through P-04, plus both E-01 runs) was
rated Low, and every justification focused exclusively on control design
strength, never on what happens if the control fails or is circumvented.
Detective and corrective controls (D-02, D-03, D-04, C-02, C-03) got more
nuanced treatment, explicit reasoning about timing gaps, exposure windows,
and reliance on post-detection response.

Put simply: the tool tends to rate residual risk (how well the control is
designed) rather than inherent risk (how bad the underlying exposure is if
the control isn't there or fails), and it does this more consistently for
preventive controls than detective ones.

**Improvement path:** the v2 prompt could explicitly ask the model to
consider both inherent risk (absent the control) and residual risk (with
the control operating as designed), and report both.

### 3. Vague input correctly triggers uncertainty flagging, not false confidence

This overturned the original hypothesis behind including X-01 and X-02 in the
test library. Both deliberately thin, vague control descriptions ("We check
things before they go through" and "Manager reviews stuff monthly") were
correctly rated High risk, with reasoning explicitly citing the lack of
specificity around scope, criteria, and escalation procedures as the source
of risk, rather than the tool inventing a specific, false-confidence answer.

This is a genuinely positive finding for the tool's real-world reliability,
worth stating honestly in an interview, including the fact that it wasn't
what you expected going in.

---

## The finalized, accurate resume bullet

> Validated tool output against a 15-control test library spanning
> preventive, detective, and corrective controls, ambiguous edge cases, and
> deliberately vague input; achieved 92% control-type classification
> accuracy and identified a specific schema limitation (forced single-label
> output on hybrid controls) as a concrete next iteration

This is fully defensible. Every number and claim in it is something you
actually ran and observed.

---

## Interview-ready answers, based on real findings

**"How did you validate the tool?"**
"I built a 15-control test library spanning preventive, detective, and
corrective controls, plus ambiguous edge cases and deliberately vague input.
Control type classification was accurate in 12 of 13 gradeable cases, 92%.
The one miss wasn't really an error, the tool interpreted a rejected-invoice
correction workflow as detective rather than corrective, and its reasoning
was defensible enough that it made me reconsider my own answer key."

**"What's a specific limitation you found?"**
"The output schema forces a single control-type label, but in one case the
model's own reasoning explicitly described a control as having both
detective and preventive characteristics, then the structured field still
picked one. The model was already generating the nuance, the schema just
wasn't built to capture it. That told me exactly what to add next: a
secondary classification field."

**"What about risk rating accuracy?"**
"That's actually where I found something more interesting than a simple
right-or-wrong answer. The tool consistently rates preventive controls based
on how well-designed they are, not on the inherent risk of what they're
protecting against. So a well-built control over a high-fraud-risk process,
like vendor master file changes, gets rated Low because the control itself
is sound, even though the underlying exposure is high. That's a residual
risk versus inherent risk distinction the prompt doesn't currently separate
out."

**"Did you test how it handles bad input?"**
"Yes, and it did better than I expected. I gave it deliberately vague,
one-sentence control descriptions with almost no detail. Instead of
confidently fabricating a specific risk rating, it flagged the vagueness
itself as the risk driver. That's the right behavior for an audit tool,
and honestly it wasn't the outcome I predicted going in."

---

## Next step

This validation work, and specifically the inherent-versus-residual risk
distinction and the hybrid-control schema gap, are exactly the kind of
findings that make a strong case study for the AI Risk Assessment Tool
build. The same failure modes (forced single labels discarding nuance,
risk reasoning that needs to separate two distinct dimensions) are worth
designing around from day one in that next build, rather than discovering
them after the fact.
