# Contributing to `fork-public-evidence`

Thank you for contributing to the public Fork evidence repository.

Fork preserves bounded evidence structures for AI-assisted workflows. It does not certify truth, approve decisions, authorize execution, establish compliance, determine legal sufficiency, or transfer institutional authority. Contributions must preserve those boundaries.

## Governing relationship

This guide governs contribution preparation and pull-request submission.

Where this guide conflicts with a frozen specification, schema, experiment preregistration, admission procedure, artifact-specific verification guide, or other more specific governing artifact, the more specific artifact controls for that surface.

Submission, verification, review, merge, and admission are separate repository events. A local or CI pass does not by itself admit a contribution into a canonical, frozen, or published evidence surface.

## Start with the change class

Classify the contribution before editing:

- **Editorial** — wording, links, spelling, or formatting with no intended semantic effect.
- **Implementation** — checker, parser, tooling, workflow, or executable behavior.
- **Schema or contract** — structural fields, validation rules, enums, precedence, or normative semantics.
- **Canonical fixture or registry** — canonical examples, registered findings, participant or experiment records, or other controlled data.
- **Experiment or receipt** — instrumentation, execution, raw outputs, receipts, or result records.
- **Historical correction** — repair, supersession, defect recording, or current-state projection concerning a previously published artifact.
- **Admission or publication** — an explicit act that admits, freezes, anchors, releases, or publishes an artifact.

Use the highest applicable class when a change spans more than one class. See [`docs/governance/CHANGE_CLASSIFICATION_v0_1.md`](docs/governance/CHANGE_CLASSIFICATION_v0_1.md) for the controlling review requirements.

Keep ordinary changes ordinary. A typo correction should not be represented as a schema amendment, and a semantic change must not be hidden inside formatting or regeneration.

## Core contribution requirements

Every contribution must preserve the distinction between:

- asserted claims and declared non-claims;
- observed, unavailable, unobserved, and unresolved information;
- evidence references and substantive conclusions;
- structural verification and factual truth;
- preserved authority context and transferred authority;
- historical state and current-state projection.

A parser, checker, transformer, report generator, fixture, or documentation change must not silently expand, narrow, resolve, approve, authorize, or otherwise change the standing of recorded content.

Intentional transformations must be explicit, attributable, versioned where required, and testable under the applicable contract.

## Local verification

Use the verification procedure declared by the component or artifact you changed. The repository-wide command map is maintained in [`docs/VERIFICATION_COMMANDS_v0_1.md`](docs/VERIFICATION_COMMANDS_v0_1.md).

The integrated Windows proof-surface command currently documented by the repository is:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify_fork_proof_surface_v0_1.ps1
```

That path is documented for Windows PowerShell 5.1. Cross-platform component commands are also available and should be used where the affected component supports them.

Do not replace a required canonical command with a translated Bash, WSL, PowerShell, or other shell command and report the result as equivalent unless that alternative path is explicitly supported and validated. Other environments may be used for repository operations and supported component checks.

Before opening a pull request:

1. identify the governing artifact and change class;
2. run the commands applicable to the changed surface;
3. record the exact command, environment, and observed result;
4. inspect generated diffs for unrelated changes;
5. confirm that no historical or frozen artifact was rewritten unintentionally.

See [`docs/verification/LOCAL_RECOMPUTATION_v0_1.md`](docs/verification/LOCAL_RECOMPUTATION_v0_1.md) for environment, shell-equivalence, and generated-artifact rules.

## Tests and fixtures

Behavioral changes require tests appropriate to the affected contract.

Where applicable, include:

- a conforming case;
- an invalid or adversarial case;
- an explicit expected failure or finding;
- a regression case for a previously observed defect;
- deterministic finding order or output expectations;
- interpretation boundaries for what a pass does and does not establish.

Do not alter a canonical fixture merely to make a checker pass. Determine whether the checker, fixture, specification, or expectation is incorrect, and preserve that determination in the pull request.

Documentation-only changes do not automatically require new fixtures, but they must not overstate the supporting technical surface.

## Historical and generated artifacts

Do not rewrite a published, admitted, frozen, or historical artifact merely to make it reflect a later interpretation.

When correcting a historical defect:

1. preserve the original artifact or its sealed representation;
2. record the defect and its coordinates;
3. add a corrective or superseding artifact;
4. identify the relationship between old and new records;
5. keep historical state distinct from any current-state projection.

Do not manually edit generated receipts unless the format explicitly permits manual authorship. Regenerate them from identified inputs and commands, and investigate unrelated output changes before submission.

The detailed procedure is in [`docs/governance/ADMISSION_AND_AMENDMENT_v0_1.md`](docs/governance/ADMISSION_AND_AMENDMENT_v0_1.md).

## Commit and pull-request scope

Use clear, descriptive commit messages. Reference the relevant commit, issue, specification, receipt, or pull request when repairing a regression.

Keep materially different change classes separate. In particular, do not combine:

- formatting cleanup with logic changes;
- schema amendments with unrelated documentation;
- historical repair with new feature development;
- experiment execution with instrumentation changes that alter the experiment;
- admission or publication acts with the implementation being admitted unless the governing procedure explicitly permits it.

## Pull-request contents

Use the repository pull-request template and provide:

- **Change class** — the highest applicable class.
- **Claim** — the specific improvement or correction supported by the diff.
- **Scope and exclusions** — files affected and surfaces intentionally unchanged.
- **Governing artifact** — specification, schema, guide, or procedure controlling the change.
- **Verification commands** — exact commands actually executed.
- **Observed and expected results** — exit status, test count, findings, or receipt location.
- **Boundary impact** — changes to claims, non-claims, exclusions, authority limits, unresolved state, evidence references, schema meaning, classification, or verification scope.
- **Historical impact** — whether any prior artifact is corrected, superseded, projected from, or intentionally left unchanged.
- **Admission posture** — whether the pull request is only a submission or also requests a separately governed admission or publication act.

Do not report a suite as passing unless it was run against the submitted commit or an identified equivalent commit.

## Review posture

Review verifies only the bounded conditions actually inspected. Independent review is not endorsement, certification, legal approval, compliance determination, production approval, or authority transfer.

Changes affecting frozen specifications, canonical fixtures, admission records, public receipts, authority boundaries, or experiment results may require independent recomputation or heightened review before admission.

For the broader review discipline, see [`docs/review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md`](docs/review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md).

## Sensitive information

Do not commit credentials, access tokens, private personal data, confidential evidence, proprietary material without authorization, or third-party content the repository may not redistribute.

Use bounded fixtures, synthetic data, redacted references, hashes, or explicitly authorized public material when demonstrating sensitive workflows.

## Conduct

Keep review precise, respectful, and attributable. Critique claims, artifacts, methods, and verification results rather than presumed motives.

Distinguish observed defects, failed verification, unresolved questions, interpretive disagreement, and allegations of misconduct. A malformed contribution should be preserved and addressed through the applicable repository procedure without unnecessary attribution of intent.
