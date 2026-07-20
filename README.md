# Fork

> **Fork is read-only evidence-boundary infrastructure for AI-assisted workflows: it preserves bounded, recomputable records so later reviewers can inspect what crossed a boundary without inheriting claims, authority, or certainty the record did not establish.**

Fork is a research implementation and public proof surface. It is not a runtime control plane, policy engine, approval system, compliance certificate, legal-sufficiency determination, truth oracle, or production-readiness authorization.

## Start here

| Your goal | First action |
|---|---|
| Understand Fork in plain language | Read [Fork in 60 seconds](#fork-in-60-seconds) and [what Fork does not claim](#what-fork-does-not-claim). |
| Run a verification path | Follow the [Public Review Quickstart](docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md) or run the [primary verifier](#run-the-primary-public-verifier). |
| Inspect one concrete artifact | Open the [recomputation-receipt example](docs/review/boundary-pressure/fixtures/valid/BPR_RR_VALID_001_receipt_preserved_as_structural_v0_1.json). |
| Review the evidence | Use [Reviewer Start Here](docs/REVIEWER_START_HERE_v0_1.md) and the [Current Proof Surface](docs/CURRENT_PROOF_SURFACE_v0_1.md). |
| Contribute or adversarially test | Use the [draft contributor route](docs/coherence/front-door-routing-v0.1/ROLE_PATH_OUTLINES_v0_1.md#2-contributor-path). |
| Evaluate governance or buyer relevance | Read the [Buyer Quick Start for GC / CISO / Risk](docs/commercial/BUYER_QUICK_START_GC_CISO_RISK_v0_1.md). |
| Study the research and architecture | Read the [research position paper](docs/research/ACCOUNTABLE_HANDOFF_INTEROPERABILITY_POSITION_PAPER_v0_1.md) and [Modular Surface](docs/modular-surface/FORK_MODULAR_SURFACE_v0_1.md). |
| Inspect limitations and negative evidence | Start with [negative evidence, residuals, and unresolved standing](#negative-evidence-residuals-and-unresolved-standing). |
| Ask a bounded question or report a problem | [Open a repository issue](https://github.com/RecomputableEvidence/fork-public-evidence/issues). |

## Fork in 60 seconds

AI-assisted work can cross organizational, technical, or decision boundaries while losing the context needed to interpret it safely. A downstream reader may see an output or receipt but not know:

- what was requested;
- what the AI produced;
- what a human reviewed;
- what evidence was available;
- what authority or policy context was asserted;
- what was excluded or unresolved;
- what the next actor was not entitled to infer.

Fork records those distinctions in bounded artifacts and provides checkers that replay declared structural conditions. The intended result is not automatic trust. It is an inspectable record that is difficult to overread.

The governing constraint is:

> **Preservation without inheritance.**

Evidence may be preserved, referenced, recomputed, and reviewed without becoming inherited authority, approval, compliance, truth, or permission to act.

## Research status

Fork currently supports an engineering pattern and a motivated hypothesis, not a proven general systems theory. Its canonical hypothesis expression is:

```text
E[U | H = 1] < E[U | H = 0]
```

Here, `U` denotes unsupported-inheritance events and `H` denotes the presence of explicit handoff-state artifacts. The hypothesis predicts fewer unsupported-inheritance events when explicit handoff-state artifacts are present. Fork does not establish that this relationship is universal, causal, sufficient for accountability, or superior to every existing mechanism.

## Run the primary public verifier

From the repository root on Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1
```

For structured output:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1 -Json
```

Expected high-level signal at a conforming exact head:

```text
PUBLIC_REVIEW_PACKAGE_VERIFY_PASS
```

A pass means only that the verifier's declared files and bounded structural checks succeeded at the tested checkout. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, production readiness, endorsement, certification, admission, or institutional authority.

For Linux or macOS reviewers without PowerShell, use the [platform fallback](docs/review/PUBLIC_VERIFIER_PLATFORM_FALLBACK_v0_1.md). Manual reconstruction is useful review evidence, but it is not identical to executing the named verifier artifact.

## Inspect one example before reading the full architecture

Start with this compact fixture:

- [Recomputation receipt preserved as structural evidence only](docs/review/boundary-pressure/fixtures/valid/BPR_RR_VALID_001_receipt_preserved_as_structural_v0_1.json)

Then read the associated case:

- [Boundary Pressure: Recomputation Receipt Overread](docs/review/boundary-pressure/BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_TEST_CASE_v0_1.md)

The example demonstrates a central boundary: a receipt may show that a bounded replay occurred while remaining insufficient to replace the underlying artifact or establish truth, approval, compliance, legal sufficiency, authorization, or production readiness.

Run the fixture family directly:

```powershell
python tools/check_boundary_pressure_review_cases_v0_1.py --json --run-adversarial
```

## What Fork preserves

Fork helps later reviewers inspect:

- the claim and its declared scope;
- the request, output, human-review, and handoff context that was recorded;
- referenced evidence and its declared role;
- non-claims and excluded interpretations;
- unresolved, failed, blocked, or not-checked conditions;
- changes in state across a declared transition;
- whether a bounded artifact still satisfies its applicable structural checks.

## What Fork does not claim

Fork does not:

- determine whether an AI-assisted decision or artifact is correct or true;
- authorize execution, retries, reliance, deployment, or downstream action;
- certify compliance, security, safety, audit sufficiency, or legal adequacy;
- establish that asserted authority or policy context was sufficient;
- approve production use or procurement;
- replace governance, legal, risk, compliance, audit, security, or institutional judgment;
- convert a receipt, successful recomputation, green workflow, exterior observation, or merge into inherited authority;
- convert post-execution evidence into retrospective authorization;
- resolve an unknown cause or incomplete evidence state by assumption.

Read the detailed boundaries:

- [Fork Non-Claim Boundary](docs/FORK_NON_CLAIM_BOUNDARY_v0_1.md)
- [Fork Operational Boundary Map](docs/FORK_OPERATIONAL_BOUNDARY_MAP_v0_1.md)
- [Maturity and Terminology Boundary](docs/architecture/FORK_MATURITY_AND_TERMINOLOGY_BOUNDARY_v0_1.md)
- [Repository Review Posture](docs/review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md)

## Status vocabulary

| State | Meaning within the named scope | It must not be read as |
|---|---|---|
| **PASS** | Every declared check succeeded. | Truth, approval, authority, compliance, safety, readiness, or complete coverage. |
| **FAIL** | At least one declared check did not succeed. | Proof that every unrelated artifact or claim is invalid. |
| **UNRESOLVED** | Available evidence does not support a conclusive classification. | Permission to assume the favorable explanation or continue execution. |
| **NOT_CHECKED** | The property was outside the cited check's scope. | PASS, FAIL, closure, or evidence that no problem exists. |

Fork-specific lifecycle and control states—such as `CANDIDATE_NOT_ADMITTED`, `STRUCTURALLY_READY_EXECUTION_BLOCKED`, or `DRIFT_CLASSIFIED_RETRY_NOT_AUTHORIZED`—must remain verbatim and must not be collapsed into one success badge.

See the [draft status glossary](docs/coherence/front-door-routing-v0.1/STATUS_GLOSSARY_v0_1.md).

## Current proof and state

Use these surfaces rather than inferring current standing from a green badge or an older narrative statement:

- [Current Proof Surface v0.1](docs/CURRENT_PROOF_SURFACE_v0_1.md)
- [Canonical proof-surface state](docs/state/FORK_PROOF_SURFACE_STATE_v0_1.json)
- [Pair-001 sequence projection](docs/sequence-surface/PAIR_001_SEQUENCE_PROJECTION_v0_1.json)
- [Experimental Extension Protocol](docs/experiments/FORK_EXPERIMENTAL_EXTENSION_PROTOCOL_v0_1.md)

The exact artifact, version, and commit govern the interpretation. Earlier successful results do not validate a later head.

## Choose a guided role path

The coherence candidate contains four draft pathways:

- [Reviewer](docs/coherence/front-door-routing-v0.1/ROLE_PATH_OUTLINES_v0_1.md#1-reviewer-path)
- [Contributor](docs/coherence/front-door-routing-v0.1/ROLE_PATH_OUTLINES_v0_1.md#2-contributor-path)
- [Governance or buyer reader](docs/coherence/front-door-routing-v0.1/ROLE_PATH_OUTLINES_v0_1.md#3-governance-or-buyer-reader-path)
- [Researcher](docs/coherence/front-door-routing-v0.1/ROLE_PATH_OUTLINES_v0_1.md#4-researcher-path)

Each route ends in a concrete next action and preserves exact-head, evidence-scope, non-claim, and authority boundaries.

## Architecture in one view

Fork's modular architecture organizes existing materials across six functional surfaces:

1. Evidence Boundary
2. Transition
3. Reliance
4. Interoperability
5. Simulation
6. Commercial

Start with:

- [Fork Modular Surface](docs/modular-surface/FORK_MODULAR_SURFACE_v0_1.md)
- [Surface Interaction Contract](docs/modular-surface/FORK_SURFACE_INTERACTION_CONTRACT_v0_1.md)
- [Modular Surface Crosswalk](docs/modular-surface/FORK_MODULAR_SURFACE_CROSSWALK_v0_1.md)

This architecture organizes evidence and interaction boundaries. It does not create a seventh authority layer or absorb the authority of an external system.

## Negative evidence, residuals, and unresolved standing

Fork preserves adverse findings and limitations rather than presenting only successful checks. Start here:

- [Boundary-pressure cases](docs/review/boundary-pressure/)
- [Longitudinal adversarial cases](docs/reconstruction/adversarial/)
- [Exterior observations](docs/exterior-observations/)
- [Root-checksum discrepancy preservation](docs/preservation/root-checksum-integrity-v0.1/)
- [Current proof surface: what Fork does not prove](docs/CURRENT_PROOF_SURFACE_v0_1.md#10-what-fork-currently-does-not-prove)

A successful correction may close a defect prospectively while preserving the original failure and the limits of earlier green runs.

## Human recomputation and exterior review

- [Boundary-State Interop human recomputation sandbox v0.1.1](docs/recomputation/boundary-state-interop-v0.1.1/README.md)
- [Public Review Quickstart](docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md)
- [Public Review Package Index](docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md)

Exterior observations and recomputation receipts are evidence within their declared scope. They are not endorsements, certifications, approvals, or authority transfers.

## Research and commercial orientation

Research:

- [Accountable Handoff Interoperability Position Paper](docs/research/ACCOUNTABLE_HANDOFF_INTEROPERABILITY_POSITION_PAPER_v0_1.md)

Governance and buyer orientation:

- [Buyer Quick Start for GC / CISO / Risk](docs/commercial/BUYER_QUICK_START_GC_CISO_RISK_v0_1.md)
- [Commercial package](docs/commercial/)

Commercial materials describe a bounded problem and possible discovery path. They do not establish client suitability, procurement approval, implementation authority, or production readiness.

## Coherence-upgrade review materials

This draft front-door branch is supported by:

- [Current front-door inventory](docs/coherence/front-door-routing-v0.1/CURRENT_FRONT_DOOR_INVENTORY_v0_1.md)
- [Canonical proof-path selection](docs/coherence/front-door-routing-v0.1/PROOF_PATH_SELECTION_v0_1.md)
- [Visitor role-path outlines](docs/coherence/front-door-routing-v0.1/ROLE_PATH_OUTLINES_v0_1.md)
- [Status glossary](docs/coherence/front-door-routing-v0.1/STATUS_GLOSSARY_v0_1.md)
- [Newcomer walkthrough forms](docs/coherence/front-door-routing-v0.1/NEWCOMER_WALKTHROUGH_FORMS_v0_1.md)

These files are draft coherence materials. They do not amend Fork's substantive claims, evidence, authority boundaries, experiment controls, historical standing, or admission state.

---

**Front-door invariant:** simplify access without simplifying the evidence, weakening the boundaries, or converting unresolved conditions into certainty.
