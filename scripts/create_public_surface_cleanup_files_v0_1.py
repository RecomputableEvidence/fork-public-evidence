from pathlib import Path

files = {
    "docs/REVIEWER_ROUTING_GUIDE_v0_1.md": """# Reviewer Routing Guide v0.1

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
""",

    "docs/evaluation/VENDOR_RISK_HANDOFF_RESULTS_v0_1.md": """# Vendor Risk Handoff Evaluation Results v0.1

## Status

Template only. No evaluation results have been recorded yet.

Fork's current evidence supports an engineering pattern and a motivated hypothesis, not a proven general systems theory.

## Evaluation Reference

Design document:

`docs/evaluation/VENDOR_RISK_HANDOFF_EVALUATION_DESIGN_v0_1.md`

## Evaluation Question

Do Fork-style boundary records help reviewers reconstruct the basis for reliance more accurately and consistently than ordinary artifacts and logs alone?

## Conditions

### Baseline Condition

Reviewers receive:

- final AI-assisted vendor risk artifact;
- ordinary workflow logs or supporting materials;
- no explicit Fork-style boundary records.

### Boundary-Record Condition

Reviewers receive the same baseline materials plus explicit handoff-state records identifying:

- what was claimed;
- what evidence was referenced;
- what authority context applied;
- what was excluded;
- what remained unresolved;
- what required revalidation;
- what downstream reliance occurred.

## Participants

| Reviewer ID | Role / Background | Condition | Notes |
|---|---|---|---|
| R-001 | TBD | TBD | TBD |
| R-002 | TBD | TBD | TBD |
| R-003 | TBD | TBD | TBD |

## Measures

| Measure | Baseline Result | Boundary-Record Result | Difference / Notes |
|---|---:|---:|---|
| Time to reconstruct reliance basis | TBD | TBD | TBD |
| Unsupported assumptions made | TBD | TBD | TBD |
| Agreement on what was established | TBD | TBD | TBD |
| Agreement on what was not established | TBD | TBD | TBD |
| Ability to distinguish evidence from authorization | TBD | TBD | TBD |
| Ability to identify preserved / narrowed / expanded / newly justified reliance | TBD | TBD | TBD |
| Reviewer confidence in claim scope | TBD | TBD | TBD |
| Reviewer confidence in non-claims | TBD | TBD | TBD |

## Qualitative Observations

TBD.

## Preliminary Interpretation

TBD.

## Hypothesis Impact

The hypothesis is strengthened if boundary records reduce ambiguity, improve reviewer agreement, and make unsupported inheritance easier to identify.

The hypothesis is weakened if reviewers perform equally well with ordinary artifacts and logs, or if boundary records introduce more confusion than clarity.
""",

    "docs/PUBLIC_SURFACE_CLEANUP_CHECKLIST_v0_1.md": """# Public Surface Cleanup Checklist v0.1

## Purpose

This checklist tracks the cleanup work needed before treating the public surface as ready for cold legal, compliance, procurement, and audit reviewers.

Fork's current evidence supports an engineering pattern and a motivated hypothesis, not a proven general systems theory.

## Required Before Cold Legal / Compliance Review

### 1. Character Encoding

- [ ] Search for mojibake artifacts.
- [ ] Repair documented encoding artifacts by codepoint sequence, including U+00C3, U+00C2, U+00E2-prefixed mojibake, and corrupted arrow artifacts.
- [ ] Confirm files are UTF-8 without BOM where practical.
- [ ] Confirm no unintended semantic changes were introduced.

### 2. Root README Compression

- [ ] Reduce `README.md` to a short public entry surface.
- [ ] Keep primary reviewer path only.
- [ ] Move detailed routing to `docs/REVIEWER_ROUTING_GUIDE_v0_1.md`.
- [ ] Preserve explicit non-claims.
- [ ] Preserve verification quickstart.
- [ ] Keep buyer / pricing content bounded and clearly marked as indicative.

### 3. Routing Discipline

- [ ] Root README points to one primary path.
- [ ] Technical validation, non-claim, research, and pilot paths live in the routing guide.
- [ ] No contradictory or duplicative routing blocks remain.

### 4. Link Integrity

- [ ] Run grep for outdated `rrelease_packages`.
- [ ] Confirm all `release_packages/` links are spelled correctly.
- [ ] Confirm new research, evaluation, and reviewer-note links resolve.

### 5. Commit Discipline

- [ ] Keep encoding / README cleanup separate from research-package commits.
- [ ] Do not mix unrelated experimental changes unless intentionally scoped.
- [ ] Review `git diff --stat` before staging.
- [ ] Avoid `git add .` unless the full working tree has been reviewed.

## Non-Claims

This checklist does not certify that the public surface is legally sufficient, compliance-ready, production-ready, or complete.

It records cleanup criteria for reviewer-facing legibility and boundary discipline.
""",

    "docs/README_SLIM_TEMPLATE_v0_1.md": """# Fork

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
"""
}

for rel, content in files.items():
    path = Path(rel)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        print(f"SKIP existing file: {rel}")
        continue
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"WROTE: {rel}")

print("Done.")
