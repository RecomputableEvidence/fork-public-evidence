# Contributing to `fork-public-evidence`

Thank you for contributing to `RecomputableEvidence/fork-public-evidence`.

This repository contains public specifications, schemas, fixtures, checkers, receipts, experiments, review surfaces, and release artifacts for research into recomputable evidence in AI-assisted workflows.

Contributions are evaluated for structural integrity, explicit claim boundaries, provenance, deterministic verification where required, and preservation of non-claims and unresolved conditions.

Acceptance of a contribution means only that it satisfied the applicable repository procedure. It does not certify truth, correctness, legality, compliance, safety, authority, endorsement, production readiness, or institutional sufficiency.

## Controlling documents

This guide governs ordinary contribution preparation and submission.

More specific artifacts control when they apply, including frozen specifications, schemas, experiment preregistrations, package verification guides, branch-specific admission procedures, and artifact contracts.

Detailed repository guidance:

- [Change Classification v0.1](docs/governance/CHANGE_CLASSIFICATION_v0_1.md)
- [Admission and Amendment v0.1](docs/governance/ADMISSION_AND_AMENDMENT_v0_1.md)
- [Local Recomputation v0.1](docs/verification/LOCAL_RECOMPUTATION_v0_1.md)
- [Verification Commands v0.1](docs/VERIFICATION_COMMANDS_v0_1.md)

## Before making a change

Identify:

1. the artifact or surface you intend to change;
2. its governing specification, schema, procedure, or verification guide;
3. the highest material change class;
4. the exact commands required to verify the change;
5. whether the change affects historical, canonical, experimental, admission, or publication state.

Do not assume that a similarly named checker, fixture, receipt, or workflow is governed by the same contract.

## Change classes

Declare the highest-impact class in the pull request.

- **C0 — Editorial:** presentation-only correction with no semantic or behavioral effect.
- **C1 — Explanatory documentation:** non-normative guidance or non-canonical examples.
- **C2 — Implementation or verification logic:** executable behavior under an unchanged contract.
- **C3 — Schema, contract, or normative rule:** structural or semantic contract changes.
- **C4 — Canonical evidence artifact:** fixtures, registries, receipts, manifests, or public evidence records.
- **C5 — Experiment surface:** preregistration, instrumentation, execution controls, raw evidence, or result formation.
- **C6 — Historical correction or amendment:** preservation, correction, recovery, projection, or supersession.
- **C7 — Admission or publication:** repository-standing, release-anchor, or canonical-state transition.

A mixed pull request is governed by its highest material class. Separate unrelated formatting, logic, schema, historical, experimental, and admission changes unless atomicity is necessary and explained.

## Core contribution boundaries

### Preserve claims and non-claims

A contribution must preserve the distinction between:

- asserted claims;
- declared non-claims;
- exclusions and authority limitations;
- unresolved or unobserved conditions;
- evidence references;
- reliance and rejection records;
- verification results.

A parser, transformer, checker, report, or fixture must not silently expand, narrow, resolve, approve, authorize, or otherwise change the standing of recorded content.

Any intentional transformation must be explicit, attributable, versioned where required, and testable.

### Keep public disclosure bounded

Clearly distinguish:

- information included in the public evidence surface;
- information retained privately or out of band;
- unavailable or unobserved information;
- unresolved references;
- contributor assumptions.

Do not represent unavailable, private, unobserved, or unresolved information as absent, false, verified, or immaterial.

### Interpret verification narrowly

A passing checker demonstrates only the declared structural or procedural result under the identified ruleset and inputs.

It does not establish the truth or authority of the underlying claim and must not be described as compliance approval, legal sufficiency, safety certification, production approval, endorsement, or authority transfer.

## Local validation

There is no single repository-wide command that controls every artifact.

Use the command declared by the most specific applicable verification guide, package README, experiment procedure, or workflow documentation.

The consolidated public/reviewer path is documented in [Verification Commands v0.1](docs/VERIFICATION_COMMANDS_v0_1.md).

The current integrated proof-surface verifier declares Windows PowerShell 5.1:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify_fork_proof_surface_v0_1.ps1
```

Several direct Python component checks are documented as cross-platform commands.

Do not substitute a translated Bash, WSL, PowerShell 7, or other command for a declared canonical verifier and report it as identical execution unless equivalence is separately tested and documented. Alternative environments may still provide valid component or manual-reconstruction evidence when their governing instructions support them.

Before submitting:

1. record the exact candidate commit;
2. run the narrowest controlling checks;
3. run required regression, integration, tamper, or adversarial suites;
4. inspect the working tree for unexpected generated changes;
5. preserve failures, warnings, skips, and unresolved conditions;
6. use a clean checkout or fresh scratch directory when the governing procedure requires independent recomputation.

Do not report a suite as passing unless that exact suite was executed against the reported candidate.

## Making changes

### Specifications and schemas

For a normative, contract, or schema change:

- identify the governing artifact and version;
- state the exact semantic delta;
- identify affected tools, fixtures, and documentation;
- add valid and invalid tests where applicable;
- document compatibility and migration effects;
- state whether historical results remain valid under their original ruleset.

Do not rewrite the meaning of an existing released version in place when an amendment or successor version is required.

### Checkers and parsers

Verification-logic changes should test:

- intended conforming behavior;
- relevant failure behavior;
- malformed inputs;
- non-claim and unresolved-state preservation;
- deterministic output or finding order where required;
- regression behavior for previously admitted fixtures.

A checker must not emit conclusions beyond the authority granted by its governing contract.

### Fixtures, receipts, and generated artifacts

State the artifact class, tested condition, governing rule, expected result, and mutability status.

Do not alter a canonical fixture only to make a checker pass. Determine whether the fixture, checker, contract, or expectation is incorrect and preserve the rationale.

Do not manually edit generated receipts unless the format explicitly permits manual authorship. After regeneration, run verification without write mode and confirm that no further changes occur.

### Historical records

Do not rewrite historical records merely to reflect a later interpretation or current state.

When correcting a historical defect:

1. preserve the original bytes or sealed representation;
2. identify the originating commit or record;
3. state the defect;
4. add a corrective, superseding, or projection artifact;
5. preserve the relationship between historical and current state;
6. recompute the current result under the applicable procedure.

### Experiments and admission

Submission, verification, review, merge, admission, publication, release, experiment readiness, and experiment execution are separate events unless a governing procedure explicitly binds them.

Do not combine instrumentation changes with experiment execution when the change could affect the result. Passing readiness checks does not authorize execution.

A pull request approval or merge does not by itself create repository-wide admission standing unless the applicable procedure says it does.

## Commit and pull-request scope

Use clear, descriptive commit messages and preserve relevant lineage.

When correcting a regression, reference the originating commit, record, issue, or pull request when known. A reference does not replace an explanation of the defect and correction.

Keep pull requests tightly scoped. Normally separate:

- formatting from logic;
- schema changes from unrelated documentation;
- historical repair from new features;
- experiment instrumentation from execution;
- candidate implementation from admission anchors.

Avoid rewriting admitted public history unless an explicitly approved recovery procedure requires it.

## Pull-request requirements

Every pull request must include:

### Claim

What specific change does the pull request introduce?

Describe only what the submitted diff and accompanying evidence support.

### Change classification

Declare the primary class, any secondary classes, the governing artifact, and why the classification is correct.

### Scope

Identify affected files and artifact classes, material exclusions, and surfaces intentionally left unchanged.

### Verification

Provide:

- exact candidate commit;
- environment and material tool versions;
- governing verification guide;
- exact commands;
- expected result;
- observed result;
- generated changes;
- untested or unresolved conditions.

### Boundary impact

State whether the pull request changes any claim, non-claim, exclusion, authority limitation, unresolved condition, evidence reference, schema meaning, classification behavior, or verification scope.

State `NONE` only after evaluating each category.

### Historical and admission impact

State whether the pull request modifies, corrects, supersedes, projects from, admits, publishes, or releases any prior artifact.

If it does not, state that no historical or admission-state transition is claimed.

## Independent review

Changes affecting frozen specifications, canonical fixtures, public receipts, authority boundaries, experiment results, historical records, or admission state may require independent review under the applicable procedure.

Independent review must be attributable. Machine execution may support a reviewer but does not manufacture human independence.

A review records what was inspected and recomputed. It is not automatically endorsement, certification, merge authority, or authority transfer.

## Sensitive information

Do not commit:

- credentials, tokens, or private keys;
- unapproved personal or confidential information;
- proprietary source material without authorization;
- unredacted sensitive evidence;
- third-party content the repository may not redistribute;
- local machine identifiers unless required and intentionally disclosed.

Use bounded fixtures, synthetic data, hashes, redacted references, or explicitly authorized public material.

## Conduct

Keep discussion respectful, precise, and focused on artifacts, claims, methods, and observed results.

Distinguish among defects, failed verification, evidence gaps, unresolved questions, interpretive disagreement, and allegations of intent.

A malformed or nonconforming contribution should be preserved and addressed under the applicable procedure without unsupported attribution of motive.

## Contribution acknowledgment

By submitting a contribution, you acknowledge that:

- it may be publicly inspected and recomputed;
- acceptance is governed by applicable repository procedures;
- historical versions may be retained for evidentiary continuity;
- accepted material may remain publicly attributable according to repository records;
- admission does not imply endorsement, certification, substantive correctness, or authority transfer.