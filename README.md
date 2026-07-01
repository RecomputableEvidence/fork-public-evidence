# Fork

Fork is a research implementation exploring whether explicit handoff-state artifacts reduce unsupported inheritance in AI-assisted institutional workflows.

Fork does **not** certify, validate, approve, authorize, guarantee, or establish legal, compliance, operational, or institutional sufficiency.

Start here: [`docs/REVIEWER_START_HERE_v0_1.md`](docs/REVIEWER_START_HERE_v0_1.md)

## Research Status

Fork's current evidence supports an engineering pattern and a motivated hypothesis, not a proven general systems theory.

Fork is one implementation case for AI-assisted institutional workflows. It does not establish that explicit handoff-state communication is universally required, superior to existing mechanisms, or sufficient for accountability by itself.

## What Fork Is

Fork is a boundary-recording pattern for AI-assisted workflow handoffs. It helps later reviewers inspect:

- what crossed a boundary;
- what did not cross;
- what claim scope was preserved;
- what authority or policy context was recorded;
- what evidence was referenced;
- what non-claims remained explicit;
- what required revalidation;
- what should not be inferred downstream.

Fork implements and explores an accountable handoff pattern. It provides initial evidence consistent with the hypothesis that explicit handoff-state records may reduce unsupported inheritance in bounded workflows.

## What Fork Is Not

- Fork does not determine whether a decision was correct.
- Fork does not authorize execution.
- Fork does not certify compliance.
- Fork does not prove institutional authority.
- Fork does not establish legal sufficiency.
- Fork does not approve production use.
- Fork does not verify the correctness, legality, completeness, or adequacy of underlying workflow data.
- Fork does not replace governance, runtime authority, audit, legal review, procurement review, compliance review, or institutional judgment.
- Fork does not convert post-execution evidence into retrospective authorization.
- Fork does not decide whether downstream reliance is justified.

## Example Workflow

Current worked example:

AI-assisted vendor-risk recommendation → internal decision memo → downstream reliance attempt.

This is one test case, not a recommended, validated, or industry-standard pattern.

The example explores how an AI-assisted artifact can move into institutional reliance, and how a bounded handoff record can help reviewers inspect whether downstream actors silently expanded the claim, authority basis, evidence basis, or reliance context.

## Start Here

Primary reviewer path:

1. [`docs/REVIEWER_START_HERE_v0_1.md`](docs/REVIEWER_START_HERE_v0_1.md)

Additional routing is available here:

- [`docs/REVIEWER_ROUTING_GUIDE_v0_1.md`](docs/REVIEWER_ROUTING_GUIDE_v0_1.md)

## Research Context

The broader research hypothesis is described here:

- [`docs/research/ACCOUNTABLE_HANDOFF_INTEROPERABILITY_POSITION_PAPER_v0_1.md`](docs/research/ACCOUNTABLE_HANDOFF_INTEROPERABILITY_POSITION_PAPER_v0_1.md)

Short form:

> Accountable Handoff Interoperability is the hypothesis that independently accountable systems require explicit handoff-state communication when exchanging consequential state. Fork is one implementation case for AI-assisted institutional workflows. The hypothesis is not proven.

## Falsifiability

Let `U` represent the rate of unsupported inheritance events per workflow.

Let `H` represent the presence of explicit handoff-state artifacts.

The hypothesis predicts:

> E[U | H = 1] < E[U | H = 0]

If controlled or quasi-controlled evaluation fails to show reduced unsupported inheritance, reliance ambiguity, or authority leakage in workflows with explicit handoff-state records, the hypothesis is weakened or requires refinement.

## Policy Reference Non-Claim

Presence of a policy reference does not imply:

- policy applicability;
- policy approval;
- compliance determination;
- authority sufficiency;
- legal adequacy;
- operational readiness.

A policy reference records only that a policy context was asserted or referenced in the bounded workflow record. Any determination that the policy was applicable, adequate, current, satisfied, or sufficient requires separate institutional authority.

## Verification

Verification commands and structural checks are documented here:

- [`docs/VERIFICATION_COMMANDS_v0_1.md`](docs/VERIFICATION_COMMANDS_v0_1.md)

A passing command indicates only the bounded structural result described by that checker. It does not establish correctness, compliance, legal sufficiency, production readiness, institutional authority, or factual truth.

## Non-Claims

Fork preserves bounded handoff records so later reviewers can inspect what was claimed, relied upon, excluded, changed, unresolved, or explicitly not transferred.

The following non-claims are invariant:

- This system does not assert legal sufficiency.
- This system does not grant authority.
- This system does not certify compliance.
- This system does not approve production use.
- This system does not replace institutional review.
- This system does not verify correctness of underlying workflow data.
