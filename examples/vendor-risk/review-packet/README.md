Fork Review Packet: Vendor-Risk Example Workflow

Purpose
This review packet provides a reviewer-operable view of the vendor-risk example workflow.
It is intended for Legal, Audit, Risk, Compliance, Procurement, Security, or AI governance review.

Workflow
AI-assisted vendor-risk recommendation -> internal decision memo -> downstream reliance attempt.

Packet components
Evidence Card: ../evidence-card.md
Boundary Map: ../boundary-map.md
Non-Claims: ../non-claims.json
Verification Receipt: ../verification-receipt.json

Reviewer questions
This packet helps answer:
What was requested?
What did the AI produce?
What did the human reviewer accept or change?
What evidence was referenced?
When did the AI-assisted memo become eligible for institutional reliance?
What did a downstream consumer attempt to infer?
What does the record explicitly not establish?
Does the packet structurally verify?

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
