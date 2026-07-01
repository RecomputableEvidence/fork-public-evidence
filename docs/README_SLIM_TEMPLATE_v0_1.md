# Fork

Fork is evidence-boundary infrastructure for AI-assisted institutional workflows.

It preserves bounded handoff records showing what was claimed, what was relied upon, what was excluded, what authority context was recorded, what remained unresolved, and what should not be inferred downstream.

Fork's current evidence supports an engineering pattern and a motivated hypothesis, not a proven general systems theory.

## What Fork Is

Fork is a boundary-recording pattern for AI-assisted workflow handoffs. It helps later reviewers inspect:

- what crossed a boundary;
- what did not cross;
- what claim scope was preserved;
- what authority or policy context was recorded;
- what evidence was referenced;
- what non-claims remained explicit;
- what required revalidation.

## What Fork Is Not

- Fork does not determine whether a decision was correct.
- Fork does not authorize execution.
- Fork does not certify compliance.
- Fork does not prove institutional authority.
- Fork does not replace governance, runtime authority, audit, legal review, procurement review, or compliance review.
- Fork does not convert post-execution evidence into retrospective authorization.

## Golden Workflow

Current worked example:

AI-assisted vendor-risk recommendation -> internal decision memo -> downstream reliance attempt.

This workflow demonstrates how an AI-assisted artifact can move into institutional reliance, and how a bounded record can prevent downstream actors from silently expanding the claim.

## Start Here

Primary reviewer path:

1. `docs/REVIEWER_START_HERE_v0_1.md`
2. `docs/reviewer-artifacts/README.md`
3. `examples/vendor-risk/README.md`
4. `docs/research/FORK_BOUNDARY_RECORDS_ENGINEERING_NOTE_v0_1.md`

Detailed routing guide:

- `docs/REVIEWER_ROUTING_GUIDE_v0_1.md`

## Research Context

The broader research hypothesis is described here:

- `docs/research/ACCOUNTABLE_HANDOFF_INTEROPERABILITY_POSITION_PAPER_v0_1.md`

Short form:

> Accountable Handoff Interoperability is the hypothesis that independently accountable systems require explicit handoff-state communication when exchanging consequential state. Fork is one implementation case for AI-assisted institutional workflows. The hypothesis is not proven.

## Verification

Verification commands and structural checks are documented here:

- `docs/VERIFICATION_COMMANDS_v0_1.md`

A passing command indicates only the bounded structural result described by that checker. It does not establish correctness, compliance, legal sufficiency, production readiness, or institutional authority.

## Non-Claims

Fork preserves bounded handoff records so later reviewers can inspect what was claimed, relied upon, excluded, changed, unresolved, or explicitly not transferred.

It does not decide whether downstream reliance is justified.
