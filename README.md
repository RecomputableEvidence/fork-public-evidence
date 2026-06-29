# Fork Public Evidence

**Recomputable Evidence for AI-assisted workflows.**

Fork is a bounded evidence-preservation surface for AI-assisted workflow events. It preserves what was observable and captured, what was checked, what failed or was not checked, what was referenced, and what must not be inferred from the preserved record.

Fork is not a runtime control plane, policy engine, compliance oracle, audit function, legal determination system, AI-output correctness validator, or production-deployment claim.

## Start here

For first review, use this path:

1. [`docs/REVIEWER_START_HERE_v0_1.md`](docs/REVIEWER_START_HERE_v0_1.md) — orientation for external reviewers.
2. [`docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md`](docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md) — stable map of public/reviewer packages.
3. [`docs/FORK_OPERATIONAL_BOUNDARY_MAP_v0_1.md`](docs/FORK_OPERATIONAL_BOUNDARY_MAP_v0_1.md) — Fork's read-only operational boundary.
4. [`docs/VERIFICATION_COMMANDS_v0_1.md`](docs/VERIFICATION_COMMANDS_v0_1.md) — exact commands for local verification.
5. [`docs/FORK_NON_CLAIM_BOUNDARY_v0_1.md`](docs/FORK_NON_CLAIM_BOUNDARY_v0_1.md) — what Fork artifacts must not be interpreted as proving.
6. [`docs/EXPERIMENTAL_BRANCH_WORK_v0_1.md`](docs/EXPERIMENTAL_BRANCH_WORK_v0_1.md) — distinction between released public-review materials and branch work.

## Recommended reviewer paths

### Public orientation path

Use this path when the reviewer asks: "What is Fork?"

1. Root `README.md`
2. `docs/REVIEWER_START_HERE_v0_1.md`
3. `docs/FORK_OPERATIONAL_BOUNDARY_MAP_v0_1.md`
4. `release_packages/FORK_PUBLIC_DOCTRINE_PACKET_v0_1/README.md`
5. `release_packages/FORK_PUBLIC_DOCTRINE_PACKET_v0_1/CLAIMS_AND_NON_CLAIMS.md`

### Technical validation path

Use this path when the reviewer asks: "Is this technically inspectable?"

1. `docs/VERIFICATION_COMMANDS_v0_1.md`
2. `release_packages/FORK_TECHNICAL_VALIDATION_PACKET_v0_1/README.md`
3. `release_packages/FORK_TECHNICAL_VALIDATION_PACKET_v0_1/VERIFICATION_INSTRUCTIONS.md`
4. `release_packages/FORK_TECHNICAL_VALIDATION_PACKET_v0_1/TECHNICAL_VALIDATION_MAP.md`
5. `technical-disclosure/README_VERIFY_PUBLIC_DISCLOSURE_v0_1_1.md`
6. `tools/`, `schemas/`, `examples/`, and `tests/`

### Pilot discovery path

Use this path only when a serious prospect asks how a bounded workflow would be evaluated.

1. `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/README.md`
2. `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/EVIDENCE_BOUNDARY_WORKSHEET.md`
3. `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/SOURCE_SYSTEM_INVENTORY.md`
4. `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/SECURITY_AND_DATA_HANDLING_QUESTIONS.md`
5. `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/CLAIMS_AND_NON_CLAIMS.md`

## Exact local verification commands

From the repository root:

```powershell
python .\tools\check_release_package.py .\release_packages\FORK_PUBLIC_DOCTRINE_PACKET_v0_1
python .\tools\check_release_package.py .\release_packages\FORK_TECHNICAL_VALIDATION_PACKET_v0_1
python .\tools\check_release_package.py .\release_packages\FORK_PILOT_DISCOVERY_PACKET_v0_1
```

To inspect the public technical disclosure verifier:

```powershell
cd .\technical-disclosure
python .\verify_public_disclosure.py
cd ..
```

For the broader repository test suite, when local dependencies are available:

```powershell
python -m pytest
```

A passing command establishes only the bounded condition declared by that command. It does not establish legal admissibility, compliance satisfaction, decision correctness, source completeness, runtime authorization, production readiness, or institutional authority.

## Released materials vs branch work

The `main` branch is the canonical public-review surface unless a different branch is explicitly named for a bounded review. Tagged GitHub releases are frozen public release artifacts. Other branches may contain experimental, repair, localization, or development work and must not be treated as released public-review posture unless merged into `main` or explicitly referenced by a release package or review request.

See `docs/EXPERIMENTAL_BRANCH_WORK_v0_1.md` before citing any branch-specific artifact externally.

## Public release packages

The stable public/reviewer package map is maintained in:

```text
docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md
```

Current public package directories include:

```text
release_packages/FORK_PUBLIC_DOCTRINE_PACKET_v0_1/
release_packages/FORK_EXECUTIVE_BUYER_PACKET_v0_1/
release_packages/FORK_TECHNICAL_VALIDATION_PACKET_v0_1/
release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/
release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/
release_packages/FORK_CLIENT_EVIDENCE_BOUNDARY_PACKET_TEMPLATE_v0_1/
```

## Canonical white paper

**Reconstructive Fidelity in the Age of AI**  
*The Invariant Distance Principle and Why Governance Requires Evidence That Survives Institutional Change*

- Canonical article: `https://RecomputableEvidence.github.io/fork-public-evidence/`
- Repository copy: `white-paper/Reconstructive_Fidelity_in_the_Age_of_AI_v1_0.md`

## Public technical disclosure

Release: **Fork Public Technical Disclosure v0.1.1**

Outer ZIP SHA-256:

```text
1361dd12b1f249372f240cb5226cac289319bc6da4ce219ea47538a0716c1410
```

The disclosure contains a deterministic synthetic workflow fixture, selected schemas, an included verifier, granular gate results, explicit non-claims, and a detached outer-ZIP receipt.

## What the public disclosure establishes

- Declared workflow-member eligibility and packet membership.
- SHA-256 member-digest recomputation.
- Canonical manifest-digest recomputation.
- Public test-key HMAC binding recomputation.
- Persisted-artifact verification.
- Granular `PASS / FAIL / NOT_CHECKED` preservation.
- Mechanical semantic-authority non-promotion checks.
- Explicit timestamp disclosure boundaries.

## What the public disclosure does not establish

- Source truth or source completeness.
- Public signer identity or non-repudiation.
- Legal admissibility.
- Compliance or ethical correctness.
- Third-party verifier independence.
- Live institutional deployment.
- Production readiness.
- Runtime control or workflow blocking authority.
- AI-output correctness.
- Decision correctness.

## Copyright

Copyright © 2026 Ryan Feller. All rights reserved.

Public availability permits inspection and verification of the disclosed artifacts. It does not grant a license to Fork's undisclosed implementation, trademarks, proprietary architecture, or controlled operating materials.
