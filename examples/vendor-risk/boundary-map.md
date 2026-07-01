Fork Boundary Map: Vendor-Risk Golden Workflow

Canonical flow
requested -> generated -> reviewed -> accepted/modified -> relied upon -> consumed downstream

Nodes
N1 - Request
Type: REQUESTED
Description: A user requests an AI-assisted vendor-risk summary.
Boundary effect: PRESERVED

N2 - AI output
Type: GENERATED
Description: The AI produces a vendor-risk recommendation.
Boundary effect: PRESERVED

N3 - Human review
Type: REVIEWED
Description: A human reviewer evaluates the AI output.
Boundary effect: PRESERVED

N4 - Human modification / acceptance
Type: ACCEPTED_MODIFIED
Description: The reviewer accepts some parts and modifies others.
Boundary effect: NARROWED

N5 - Institutional reliance
Type: RELIED_UPON
Description: The reviewed memo becomes eligible to inform an internal vendor-risk decision.
Boundary effect: PRESERVED

N6 - Downstream consumption attempt
Type: CONSUMED_DOWNSTREAM
Description: A downstream consumer attempts to treat the memo as broader vendor approval.
Boundary effect: EXPANDED

Boundary issue
The downstream consumption attempt expands the original record from a reviewed vendor-risk memo into apparent vendor approval. Fork does not silently accept that expansion.
The expansion requires additional authority or evidence outside this packet.

Not Established by This Record
This record does not certify legal sufficiency.
This record does not establish vendor approval.
This record does not certify model correctness.
This record does not establish regulatory compliance.
This record does not transfer upstream authority.
This record does not prove underlying sources were true.
This record preserves only the bounded evidence and reliance structure.

## Human-readable non-claims panel

See `NON_CLAIMS_PANEL.md` for the reviewer-facing **Not Established by This Record** panel. The JSON file `non-claims.json` remains the machine-readable companion; the Markdown panel is the human-readable boundary-control surface.

## Authority and policy context

See `authority-policy-context.md` for the reviewer-facing authority and policy context associated with this vendor-risk workflow.

That file preserves the stated role, policy context, reliance purpose, unresolved authority questions, and downstream authority-context expansion. It does not establish that the authority was sufficient, that the policy was adequate, or that the decision was legally, commercially, operationally, or regulatorily sufficient.
