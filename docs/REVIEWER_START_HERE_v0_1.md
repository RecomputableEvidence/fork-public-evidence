# Fork Reviewer Start Here v0.1

## Purpose

This guide is the entry point for external review of Fork's public repository. It exists to reduce misinterpretation by giving reviewers one reading path, one technical validation path, one package index, and one non-claim boundary.

## One-sentence description

Fork is read-only evidence-boundary infrastructure for AI-assisted workflows: it preserves bounded records of what was observable and captured so later reviewers can inspect the record without inheriting claims the record did not establish.

## What to read first

### Ten-minute orientation

1. Root `README.md`
2. `docs/FORK_NON_CLAIM_BOUNDARY_v0_1.md`
3. `docs/FORK_OPERATIONAL_BOUNDARY_MAP_v0_1.md`

### Thirty-minute reviewer path

1. Root `README.md`
2. `docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md`
3. `docs/FORK_OPERATIONAL_BOUNDARY_MAP_v0_1.md`
4. `release_packages/FORK_PUBLIC_DOCTRINE_PACKET_v0_1/README.md`
5. `release_packages/FORK_TECHNICAL_VALIDATION_PACKET_v0_1/README.md`
6. `docs/VERIFICATION_COMMANDS_v0_1.md`

## Technical validation path

1. `release_packages/FORK_TECHNICAL_VALIDATION_PACKET_v0_1/VERIFICATION_INSTRUCTIONS.md`
2. `release_packages/FORK_TECHNICAL_VALIDATION_PACKET_v0_1/TECHNICAL_VALIDATION_MAP.md`
3. `technical-disclosure/README_VERIFY_PUBLIC_DISCLOSURE_v0_1_1.md`
4. `tools/`, `schemas/`, `examples/`, and `tests/`

## Pilot discovery path

Use this path only when a serious prospect asks how a bounded workflow would be evaluated for possible pilot scoping.

1. `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/README.md`
2. `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/EVIDENCE_BOUNDARY_WORKSHEET.md`
3. `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/SOURCE_SYSTEM_INVENTORY.md`
4. `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/SECURITY_AND_DATA_HANDLING_QUESTIONS.md`
5. `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/CLAIMS_AND_NON_CLAIMS.md`

## Reviewer posture

Review Fork as an evidence-boundary system, not as a general AI governance platform.

A valid review should distinguish:

- what the artifact preserves;
- what the verifier checks;
- what the package claims;
- what the package expressly does not claim;
- whether the artifact is released public material or branch-specific experimental work.

## Correct interpretation of verification

A successful verification result means the checked artifact satisfied the declared structural condition for that verifier.

It does not mean the underlying workflow was correct, lawful, compliant, complete, independently witnessed, safe, or production-ready.

## Common misreadings to avoid

Do not treat Fork as:

- a policy engine;
- a workflow controller;
- an AI-output truth validator;
- a legal-admissibility system;
- a compliance certification system;
- a production deployment claim;
- a substitute for client-specific source-system analysis;
- a basis for automatic runtime blocking or authorization.

## External review rule

When citing Fork externally, cite the smallest bounded artifact that supports the statement.

Do not cite the whole repository as support for a claim that only one package, checker, or branch artifact addresses.
