Vendor-Risk Golden Workflow Example

Purpose
This example is Fork's golden workflow for the current product surface.

It demonstrates:
AI-assisted vendor-risk recommendation -> internal decision memo -> downstream reliance attempt.

Scenario
A team requests an AI-assisted vendor-risk summary. The AI produces a recommendation. A human reviewer edits and accepts parts of the output. The resulting memo becomes eligible for institutional reliance. A downstream consumer later attempts to treat the memo as broader vendor approval.

Fork preserves the evidence boundary around that handoff.

Reviewer artifacts
This example includes:
evidence-card.md
boundary-map.md
non-claims.json
verification-receipt.json
review-packet/README.md

What this example shows
What was requested
What AI produced
What a human reviewed or changed
What evidence was referenced
The first moment of institutional reliance
What was explicitly not established
How a downstream expansion attempt is surfaced
Whether the record structurally verifies

What this example does not show
This example does not certify vendor approval, legal sufficiency, compliance, model correctness, safety, or truth of the underlying sources.

## Human-readable non-claims panel

See `NON_CLAIMS_PANEL.md` for the reviewer-facing **Not Established by This Record** panel. The JSON file `non-claims.json` remains the machine-readable companion; the Markdown panel is the human-readable boundary-control surface.
