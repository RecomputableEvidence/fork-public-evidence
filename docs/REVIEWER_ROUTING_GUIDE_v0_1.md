# Reviewer Routing Guide v0.1

## Purpose

This guide moves detailed reviewer routing out of the root README so the public entry surface stays short, legible, and useful for cold reviewers.

Fork's current evidence supports an engineering pattern and a motivated hypothesis, not a proven general systems theory.

## Primary Reviewer Path

Use this path for most first-time reviewers.

1. `README.md`
2. `docs/REVIEWER_START_HERE_v0_1.md`
3. `docs/reviewer-artifacts/README.md`
4. `examples/vendor-risk/README.md`
5. `docs/research/FORK_BOUNDARY_RECORDS_ENGINEERING_NOTE_v0_1.md`

## Technical Validation Path

Use this path when the reviewer asks whether Fork records are structurally inspectable.

1. `docs/VERIFICATION_COMMANDS_v0_1.md`
2. `docs/reviewer-artifacts/VERIFICATION_RECEIPT_SPEC_v0_1.md`
3. `docs/reviewer-artifacts/REVIEW_PACKET_SPEC_v0_1.md`
4. `examples/vendor-risk/review-packet/README.md`
5. `tools/`, `schemas/`, `examples/`, and `tests/`

## Boundary / Non-Claim Review Path

Use this path when the reviewer asks what Fork does not establish.

1. `docs/FORK_NON_CLAIM_BOUNDARY_v0_1.md`
2. `docs/reviewer-artifacts/NON_CLAIM_PANEL_SPEC_v0_1.md`
3. `examples/vendor-risk/NON_CLAIMS_PANEL.md`
4. `docs/reviewer-artifacts/AUTHORITY_POLICY_CONTEXT_SPEC_v0_1.md`
5. `examples/vendor-risk/authority-policy-context.md`

## Research / Hypothesis Path

Use this path for reviewers evaluating the broader research hypothesis.

1. `docs/research/ACCOUNTABLE_HANDOFF_INTEROPERABILITY_POSITION_PAPER_v0_1.md`
2. `docs/research/FORK_BOUNDARY_RECORDS_ENGINEERING_NOTE_v0_1.md`
3. `docs/reviewer_notes/ACCOUNTABLE_HANDOFF_REVIEWER_NOTE_v0_1.md`
4. `docs/evaluation/VENDOR_RISK_HANDOFF_EVALUATION_DESIGN_v0_1.md`

## Pilot / Buyer Path

Use this path only after the reviewer understands Fork's boundaries.

1. `docs/pilots/FORK_RELIANCE_EVIDENCE_PILOT_v0_1.md`
2. `docs/BOUNDED_WORKFLOW_POV_SCOPE_TEMPLATE_v0_1.md`
3. `docs/ENTERPRISE_DISCOVERY_POV_PACKET_v0_1.md`
4. `docs/FORK_CLIENT_INTAKE_READINESS_STATEMENT_v0_1.md`

## Non-Claims

This guide does not assert that Fork proves correctness, authorization, compliance, legal sufficiency, vendor approval, production readiness, or institutional authority.

Fork preserves bounded handoff records so later reviewers can inspect what was claimed, relied upon, excluded, changed, unresolved, or explicitly not transferred.
