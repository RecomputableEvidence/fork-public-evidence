# Worked Example: Vendor Risk AI-Assisted Decision Record v0.1

## Purpose

This worked example shows what Fork may preserve in an AI-assisted workflow without implying that Fork proves the underlying decision was correct, lawful, compliant, complete, or safe.
The example is synthetic and illustrative.

## Scenario

A procurement analyst uses an AI assistant to summarize risk signals for a proposed vendor.
The analyst asks the AI system to review provided vendor-risk materials and produce a summary for internal review.
The AI output is then used as one input in a human vendor-risk discussion.

## What Fork preserves

Fork may preserve a bounded evidence record showing:

- the declared workflow boundary;
- the user or system request, where captured;
- the AI-assisted output, where captured;
- referenced input artifacts or artifact digests, where captured;
- human review state, where declared;
- claim and non-claim boundaries;
- checker output;
- package membership;
- digest or receipt relationships;
- PASS, FAIL, or NOT_CHECKED states emitted by the relevant public checker;
- unresolved unknowns or non-established properties where declared.

## Example preserved record shape

A simplified record might preserve:

`yaml
workflow_type: vendor_risk_review
event_type: ai_assisted_summary
input_refs:
  - vendor_questionnaire_digest
  - sanctions_screening_report_digest
  - contract_risk_notes_digest
ai_output_ref: ai_vendor_risk_summary_digest
human_review_state: reviewed_for_internal_discussion
claim_boundary: record_integrity_and_boundary_structure_only
non_claims:
  - does_not_prove_vendor_is_safe
  - does_not_prove_vendor_is_compliant
  - does_not_prove_sanctions_status
  - does_not_prove_contract_approval
  - does_not_prove_procurement_readiness
checker_result: PASS
not_checked:
  - source_truth
  - legal_sufficiency
  - compliance_satisfaction
  - production_timestamp_validation
`

## Six-month review question

Six months later, a legal, audit, or risk reviewer asks:
What did the organization rely on when the vendor-risk discussion occurred?

Fork does not answer whether the vendor was good, safe, compliant, or properly approved.
Fork helps the reviewer inspect the bounded record:

- what was requested;
- what AI-assisted output was preserved;
- what evidence references were declared;
- what human review state was declared;
- what the checker verified structurally;
- what the checker did not check;
- what claims were explicitly not established.

## What this example does not prove

This example does not establish:

- vendor suitability;
- vendor compliance;
- sanctions status;
- financial stability;
- contract approval;
- procurement approval;
- legal sufficiency;
- risk acceptance;
- audit sufficiency;
- source-system completeness;
- AI-output correctness;
- production deployment;
- customer deployment.

## Why this matters

AI-assisted workflows often leave organizations with a reconstruction problem.
A later reviewer may need to know whether a decision relied on an AI output, what the AI output said, what evidence was referenced, what human review occurred, and what was never established.

Fork's value is not that it makes the original decision correct.
Fork's value is that it preserves a bounded evidence record so the later review does not silently inherit claims the record never made.

## Contact

For a bounded discovery conversation about applying this pattern to a specific AI-assisted workflow, contact Ryan Feller via LinkedIn at https://www.linkedin.com/in/YOUR-LINKEDIN-SLUG/.
