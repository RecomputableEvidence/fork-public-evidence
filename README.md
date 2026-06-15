# Fork Public Evidence

## Suggested Reading Path

For a first review, read the artifacts in this order:

1. **README** — what Fork establishes and does not establish.
2. **[Reading Guide: From Reconstructive Fidelity to Recomputable Evidence](docs/READING_GUIDE_RECONSTRUCTIVE_FIDELITY_TO_RECOMPUTABLE_EVIDENCE.md)** — how the reconstructive-fidelity doctrine maps to Fork's executable evidence posture.
3. **[Fork Operational Boundary Map v0.1](docs/FORK_OPERATIONAL_BOUNDARY_MAP_v0_1.md)** - defines Fork's production boundary as a read-only evidence hand-off layer between upstream authority/execution mechanisms and downstream audit, legal, compliance, risk, security, remediation, and reporting functions.
4. **White Paper: _Reconstructive Fidelity in the Age of AI_** — the broader governance and evidentiary doctrine.
5. **v0.7 Release Notes** — the narrow recomputability receipt-binding milestone.
6. **Local Verification Script** — run `technical-disclosure/verify_public_disclosure.py` to inspect the public disclosure verification surface.
7. **Schemas, examples, tests, and tools** — review the executable evidence constraints in `schemas/`, `examples/`, `tests/`, and `tools/`.

This reading path is intended to prevent two common misreadings: treating Fork as only a theoretical governance paper, or treating the repository as a broad product-readiness claim. Fork's current public posture is narrower: bounded evidence preservation, explicit non-claims, and test-backed controls against specific forms of evidentiary overclaim.

## Release package planning

- [Fork Release Package Ladder v0.1](docs/FORK_RELEASE_PACKAGE_LADDER_v0_1.md) - defines bounded package types for public doctrine, executive buyer review, technical validation, pilot discovery, pilot-ready implementation, and client-specific evidence-boundary delivery.
- [Fork Release Package Send Guide v0.1](docs/FORK_RELEASE_PACKAGE_SEND_GUIDE_v0_1.md) - operating guide for selecting the smallest bounded package that truthfully answers a recipient's stage, role, and disclosure need.
- [Fork Discovery Intake Frame v0.1](docs/FORK_DISCOVERY_INTAKE_FRAME_v0_1.md) - internal intake guide for classifying qualified inbound conversations, mapping client-specific workflows, and preserving the boundary that the sidecar bridge is discovered rather than assumed.
- [Fork Public Doctrine Packet v0.1](release_packages/FORK_PUBLIC_DOCTRINE_PACKET_v0_1/README.md) - public doctrine orientation package for early reviewers, AI governance/legal/audit/compliance/risk/security readers, and initial category review.
- [Fork Executive Buyer Packet v0.1](release_packages/FORK_EXECUTIVE_BUYER_PACKET_v0_1/README.md) - executive orientation package for GC/CLO/CCO/CRO, audit leadership, legal operations, governance, risk, compliance, security, and pilot-sponsor review.
- [Fork Technical Validation Packet v0.1](release_packages/FORK_TECHNICAL_VALIDATION_PACKET_v0_1/README.md) - technical validation orientation package for reviewers inspecting Fork's public packet, manifest, checksum, schema, and verification posture.
- [Fork Pilot Discovery Packet v0.1](release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/README.md) - pilot discovery scaffold for evaluating whether a defined AI-assisted workflow is suitable for bounded, read-only evidence preservation.
- [Fork Client Discovery Return Packet Template v0.1](release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/README.md) - client-completable return packet for mapping a candidate workflow, source systems, access/export model, evidence artifacts, ownership, and non-claims before any client-specific evidence boundary or sidecar bridge is scoped.
- [Fork Client Evidence Boundary Packet Template v0.1](release_packages/FORK_CLIENT_EVIDENCE_BOUNDARY_PACKET_TEMPLATE_v0_1/README.md) - Fork-drafted boundary packet template for translating a completed client discovery return into workflow scope, source-system boundaries, evidence artifacts, non-claims, blockers, and candidate sidecar bridge requirements.

Fork restricts what any artifact in the evidentiary chain may be treated as proving, for the purpose of authorized action.


Public evidence, technical disclosure, and canonical publication materials for Fork’s work on reconstructive fidelity in AI-assisted workflows.

## Canonical white paper

**Reconstructive Fidelity in the Age of AI**  
*The Invariant Distance Principle and Why Governance Requires Evidence That Survives Institutional Change*

- Canonical article: https://RecomputableEvidence.github.io/fork-public-evidence/
- Repository copy: https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/white-paper/Reconstructive_Fidelity_in_the_Age_of_AI_v1_0.md
- Technical disclosure release: https://github.com/RecomputableEvidence/fork-public-evidence/releases/tag/fork-public-disclosure-v0.1.1

## Public technical disclosure

Release: **Fork Public Technical Disclosure v0.1.1**

Outer ZIP SHA-256:

```text
1361dd12b1f249372f240cb5226cac289319bc6da4ce219ea47538a0716c1410
```

The disclosure contains a deterministic synthetic workflow fixture, selected schemas, an included verifier, granular gate results, explicit non-claims, and a detached outer-ZIP receipt.

## Established by the public disclosure

- Declared workflow-member eligibility and packet membership
- SHA-256 member-digest recomputation
- Canonical manifest-digest recomputation
- Public test-key HMAC binding recomputation
- Persisted-artifact verification
- Granular `PASS / FAIL / NOT_CHECKED` preservation
- No aggregate trust, validity, compliance, or admissibility verdict
- Mechanical semantic-authority non-promotion checks
- Explicit timestamp disclosure boundaries

## Not established

- Source truth or completeness
- Public signer identity or non-repudiation
- Legal admissibility
- Compliance or ethical correctness
- Third-party verifier independence
- Live institutional deployment
- Production readiness

## Local verification

See:

```text
technical-disclosure/README_VERIFY_PUBLIC_DISCLOSURE_v0_1_1.md
```

Then run:

```powershell
cd technical-disclosure
python .\verify_public_disclosure.py
```

## Release assets

The exact frozen ZIP and detached SHA-256 receipt are available in:

```text
receipts/
```

and through the tagged GitHub Release.

## Copyright

Copyright © 2026 Ryan Feller. All rights reserved.

Public availability permits inspection and verification of the disclosed artifacts. It does not grant a license to Fork’s undisclosed implementation, trademarks, proprietary architecture, or controlled operating materials.
