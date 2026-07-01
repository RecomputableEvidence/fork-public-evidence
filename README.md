# Fork Public Evidence

> **Boundary note:** This repository provides a bounded, read-only evidence disclosure and verification surface. It does not certify legal admissibility, production readiness, security posture, SOC 2, ISO, HIPAA, regulatory compliance, customer deployment, commercial pilot approval, AI-output correctness, source completeness, or institutional authority.

**Recomputable Evidence for AI-assisted workflows.**

Fork is evidence-boundary infrastructure for AI-assisted workflows. It preserves a reviewer-operable record of what was requested, what AI produced, what humans reviewed or changed, what evidence was referenced, what was explicitly not claimed, and whether the sealed packet still verifies later.

Fork preserves the evidence boundary around AI-assisted institutional work.

Fork does **not** certify truth, compliance, safety, legal sufficiency, model quality, vendor approval, production readiness, source completeness, or institutional authority. It preserves what the record can legitimately be said to establish, and what it explicitly does not establish.

Fork is not a runtime control plane, policy engine, compliance oracle, audit function, legal determination system, AI-output correctness validator, production-deployment claim, or authority-transfer mechanism.

## What Fork is

Fork is designed to preserve the evidence boundary around AI-assisted institutional work.

It provides reviewer-facing artifacts for AI-assisted workflows, including:

- Evidence Card
- Boundary Map
- Verification Receipt
- Review Packet
- Non-Claim Panel

Fork helps reviewers answer:

> When an AI-assisted output became a basis for action, what exactly did the organization rely on, what was explicitly not established, and does that record still verify?

## What Fork is not

Fork is not:

- an AI governance platform;
- a compliance automation system;
- a model monitoring or observability tool;
- a runtime policy engine;
- an explainability or truth-certification system;
- a replacement for GRC, legal judgment, audit judgment, risk acceptance, or governance programs.

Fork does not:

- certify legal sufficiency;
- establish regulatory compliance;
- declare vendor approval;
- prove model correctness;
- guarantee safety;
- validate AI-output correctness;
- establish source completeness;
- transfer authority from one record to another.

Fork's doctrine is:

> Preservation without inheritance.

## Golden workflow

The current golden workflow is:

> AI-assisted vendor-risk recommendation Ã¢â€ â€™ internal decision memo Ã¢â€ â€™ downstream reliance attempt.

This workflow demonstrates the moment an AI-assisted artifact becomes eligible for institutional reliance and the downstream risk that a bounded record may be silently expanded into a broader claim.

See:

- `examples/vendor-risk/`

## Reviewer artifacts

Reviewer-facing artifacts are defined under:

- `docs/reviewer-artifacts/`

The current artifact set includes:

- Fork Evidence Card
- Fork Boundary Map
- Fork Verification Receipt
- Fork Review Packet
- Fork Non-Claim Panel

Every Fork packet exposes a required section titled:

> **Not Established by This Record**

## Pilot

The current buyer-facing pilot is:

> One bounded AI-assisted workflow. One sealed evidence packet. One verification path. One reviewer-facing closeout report.

See:

- `docs/pilots/FORK_RELIANCE_EVIDENCE_PILOT_v0_1.md`

## Proof surface

Technical and proof-layer materials live under:

- `docs/proof/`

The proof surface may document schemas, checkers, fixtures, receipts, reproducibility materials, and boundary discipline. These mechanisms support the reviewer-facing product surface but should not be required for a reviewer to understand what Fork preserves.

## Start here
Start with [REVIEWER_QUICK_START_v0_1.md](REVIEWER_QUICK_START_v0_1.md) for the shortest reproducible reviewer path.

The canonical reviewer entry point is:

```text
docs/REVIEWER_START_HERE_v0_1.md
```

Use the root `README.md` as a short orientation only. Use `docs/REVIEWER_START_HERE_v0_1.md` as the authoritative reading path for external review.

### Minimum first-review path

- `docs/REVIEWER_START_HERE_v0_1.md` - canonical reviewer entry point.
- `docs/FORK_NON_CLAIM_BOUNDARY_v0_1.md` - complete non-claim boundary.
- `docs/VERIFICATION_COMMANDS_v0_1.md` - bounded technical verification commands.
- `docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md` - stable package map.
- `docs/EXPERIMENTAL_BRANCH_WORK_v0_1.md` - boundary for branch, internal, legacy, and non-release materials.

## Recommended reviewer paths

The paths below are a quick summary of `docs/REVIEWER_START_HERE_v0_1.md`. If there is any uncertainty, treat `docs/REVIEWER_START_HERE_v0_1.md` as authoritative.

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

### Executive buyer orientation path

Use this path only when an executive, advisor, technical sponsor, legal/compliance leader, audit leader, or design-partner sponsor asks why Fork matters commercially or organizationally.

This packet is an orientation surface. It does not establish pricing, procurement readiness, pilot approval, production deployment, legal sufficiency, compliance satisfaction, risk acceptance, or client-specific suitability.

1. `release_packages/FORK_EXECUTIVE_BUYER_PACKET_v0_1/README.md`
2. `release_packages/FORK_EXECUTIVE_BUYER_PACKET_v0_1/EXECUTIVE_BRIEF.md`
3. `release_packages/FORK_EXECUTIVE_BUYER_PACKET_v0_1/BUYER_PROBLEM.md`
4. `release_packages/FORK_EXECUTIVE_BUYER_PACKET_v0_1/USE_CASES.md`
5. `release_packages/FORK_EXECUTIVE_BUYER_PACKET_v0_1/CLAIMS_AND_NON_CLAIMS.md`

### Pilot discovery path

Use this path only when a serious prospect asks how a bounded workflow would be evaluated for possible pilot scoping.

This packet supports discovery and boundary scoping. It does not establish workflow suitability, commercial pilot readiness, production readiness, implementation approval, legal sufficiency, compliance satisfaction, or client-specific deployment coverage.

1. `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/README.md`
2. `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/EVIDENCE_BOUNDARY_WORKSHEET.md`
3. `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/SOURCE_SYSTEM_INVENTORY.md`
4. `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/SECURITY_AND_DATA_HANDLING_QUESTIONS.md`
5. `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/CLAIMS_AND_NON_CLAIMS.md`

## Exact local verification commands

From the repository root:

```powershell
python ./tools/check_release_package.py ./release_packages/FORK_PUBLIC_DOCTRINE_PACKET_v0_1
python ./tools/check_release_package.py ./release_packages/FORK_TECHNICAL_VALIDATION_PACKET_v0_1
```

Before checking the pilot discovery package, note: This verifies package structure and checksums only; it does not validate commercial pilot readiness.

```powershell
python ./tools/check_release_package.py ./release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1
```

To inspect the public technical disclosure verifier:

```powershell
cd ./technical-disclosure
python ./verify_public_disclosure.py
cd ..
```

For the broader repository test suite, when local dependencies are available:

```powershell
python -m pytest
```

A passing command establishes only the bounded condition declared by that command. It does not establish legal admissibility, compliance satisfaction, decision correctness, source completeness, runtime authorization, production readiness, or institutional authority.

## Released materials vs branch work

- The `main` branch is the canonical public-review surface unless a different branch is explicitly named for a bounded review.
- Tagged GitHub releases are frozen public release artifacts.
- Other branches may contain experimental, repair, localization, or development work and must not be treated as released public-review posture unless merged into `main` or explicitly referenced by a release package or review request.

See `docs/EXPERIMENTAL_BRANCH_WORK_v0_1.md` before citing any branch-specific artifact externally.

## Public release packages

The stable public/reviewer package map is maintained in:

- `docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md`

Current public package directories include:

- `release_packages/FORK_PUBLIC_DOCTRINE_PACKET_v0_1/`
- `release_packages/FORK_EXECUTIVE_BUYER_PACKET_v0_1/`
- `release_packages/FORK_TECHNICAL_VALIDATION_PACKET_v0_1/`
- `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/`
- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/`
- `release_packages/FORK_CLIENT_EVIDENCE_BOUNDARY_PACKET_TEMPLATE_v0_1/`

## Canonical white paper

**Reconstructive Fidelity in the Age of AI**  
_The Invariant Distance Principle and Why Governance Requires Evidence That Survives Institutional Change_

- Canonical article: <https://RecomputableEvidence.github.io/fork-public-evidence/>
- Repository copy: `white-paper/Reconstructive_Fidelity_in_the_Age_of_AI_v1_0.md`

Citation metadata in `CITATION.cff` supports formal attribution of this repository and cited public disclosure materials. It does not establish peer-reviewed publication, academic endorsement, certification, or institutional validation.

## Public technical disclosure

Release: **Fork Public Technical Disclosure v0.1.1**

Outer ZIP SHA-256:

```text
1361dd12b1f249372f240cb5226cac289319bc6da4ce219ea47538a0716c1410
```

The disclosure contains a deterministic synthetic workflow fixture, selected schemas, an included verifier, granular gate results, explicit non-claims, and a detached outer-ZIP receipt.

### What the public disclosure establishes

- Declared workflow-member eligibility and packet membership.
- SHA-256 member-digest recomputation.
- Canonical manifest-digest recomputation.
- Public test-key HMAC binding recomputation.
- Persisted-artifact verification.
- Granular PASS / FAIL / NOT_CHECKED preservation.
- Mechanical semantic-authority non-promotion checks.
- Explicit timestamp disclosure boundaries.

### What the public disclosure does not establish

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

For the complete non-claim boundary, see `docs/FORK_NON_CLAIM_BOUNDARY_v0_1.md`.

<!-- FORK_PUBLIC_PRESENCE_ROUTING_START -->

## Public presence and workflow-inlet routing

Fork routes by evidence-boundary input, not by buyer persona.

A reviewer, advisor, enterprise sponsor, legal/compliance leader, audit leader, risk leader, technical sponsor, source-system owner, GRC owner, AI governance lead, or co-integration partner may all enter through the same public surface.

The correct inlet depends on what the visitor can provide.

### Public review input

Use:

- REVIEWER_QUICK_START_v0_1.md
- docs/REVIEWER_START_HERE_v0_1.md
- docs/FORK_NON_CLAIM_BOUNDARY_v0_1.md
- docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md

### Candidate workflow input

Start with:

- 
elease_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/

### Client-side workflow/source-system input

Complete:

- 
elease_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/

### Fork-authored evidence-boundary output

Fork may draft:

- 
elease_packages/FORK_CLIENT_EVIDENCE_BOUNDARY_PACKET_TEMPLATE_v0_1/

only after reviewing a completed Client Discovery Return Packet.

### Sidecar bridge specification

A sidecar bridge follows an accepted evidence boundary. It is not assumed from public review alone.

### Bounded workflow PoV

A PoV may be scoped only around one accepted bounded workflow.

For the canonical routing cadence, see:

- docs/FORK_INLET_ROUTING_AND_ONBOARDING_CADENCE_v0_1.md

This routing does not establish production readiness, customer deployment, procurement approval, legal sufficiency, compliance satisfaction, audit sufficiency, source completeness, security approval, risk acceptance, workflow suitability, commercial pilot approval, AI-output correctness, decision correctness, or institutional authority.

## Enterprise discovery and bounded workflow PoV

Fork can be evaluated only around a bounded AI-assisted workflow whose evidence boundary has been described, reviewed, and accepted for scoping.

The governing sequence is:

1. Public repo orientation.
2. Workflow-inlet routing.
3. Client Discovery Return Packet.
4. Fork review of returned workflow/source-system facts.
5. Client Evidence Boundary Packet draft, if responsible.
6. Client review of the proposed evidence boundary.
7. Sidecar bridge specification candidate, if the boundary is accepted.
8. Bounded workflow PoV scope, if commercially and operationally appropriate.

The Client Discovery Return Packet is the inbound mapping record.

The Client Evidence Boundary Packet is the Fork-authored boundary draft.

The sidecar bridge is downstream of the accepted boundary.

The institution owns the action. Fork preserves the bounded evidence record.

For bounded technical review, design-partner discussion, or enterprise discovery, contact Ryan Feller via LinkedIn.

This routing does not establish a binding quote, procurement approval, production readiness, customer deployment, commercial pilot approval, legal sufficiency, security certification, compliance satisfaction, audit sufficiency, risk acceptance, workflow suitability, source-system access approval, implementation approval, or sidecar bridge approval.

<!-- FORK_PUBLIC_PRESENCE_ROUTING_END -->

## Copyright
CopyrightÃ‚Â© 2026 Ryan Feller. All rights reserved.

Public availability permits inspection and verification of the disclosed artifacts. It does not grant a license to Fork's undisclosed implementation, trademarks, proprietary architecture, unpublished implementation code, internal tooling, operating procedures, or delivery materials not included in this public release.
