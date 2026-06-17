# VERSION 1 - First attempt prompt.
# Simple and unstructured. Works, but output is inconsistent
# and cannot be reliably parsed into UI cards.
# Kept intentionally to show the prompt iteration story.


def build_prompt_v1(control_description):
    return (
        "You are an internal auditor. Analyze the following SOX internal control "
        "and tell me what type of control it is, the risk, and how to test it.\n\n"
        f"Control:\n{control_description}\n"
    )