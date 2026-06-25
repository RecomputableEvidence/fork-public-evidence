# Fork Public Evidence

## Suggested Reading Path

For a first review, read the artifacts in this order:

1. **README** what Fork establishes and does not establish.
2. **[Reading Guide: From Reconstructive Fidelity to Recomputable Evidence](docs/READING_GUIDE_RECONSTRUCTIVE_FIDELITY_TO_RECOMPUTABLE_EVIDENCE.md)**  how the reconstructive-fidelity doctrine maps to Fork's executable evidence posture.
3. **[Fork Operational Boundary Map v0.1](docs/FORK_OPERATIONAL_BOUNDARY_MAP_v0_1.md)** - defines Fork's production boundary as a read-only evidence hand-off layer between upstream authority/execution mechanisms and downstream audit, legal, compliance, risk, security, remediation, and reporting functions.
4. **White Paper: _Reconstructive Fidelity in the Age of AI_**  the broader governance and evidentiary doctrine.
5. **v0.7 Release Notes**  the narrow recomputability receipt-binding milestone.
6. **Local Verification Script**  run `technical-disclosure/verify_public_disclosure.py` to inspect the public disclosure verification surface.
7. **Schemas, examples, tests, and tools**  review the executable evidence constraints in `schemas/`, `examples/`, `tests/`, and `tools/`.

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
- [Fork Client Intake Readiness Statement v0.1](docs/FORK_CLIENT_INTAKE_READINESS_STATEMENT_v0_1.md) - public readiness boundary stating that Fork is ready for qualified client intake and evidence-boundary mapping, not generic production onboarding.
- [Synthetic Vendor Diligence Client Discovery Return v0.1](examples/client_discovery_return/vendor_diligence_synthetic_v0_1/README.md) - synthetic completed client discovery return example demonstrating a REVIEWABLE intake classification without real client data.

Fork restricts what any artifact in the evidentiary chain may be treated as proving, for the purpose of authorized action.


Public evidence, technical disclosure, and canonical publication materials for Fork™s work on reconstructive fidelity in AI-assisted workflows.

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

Public availability permits inspection and verification of the disclosed artifacts. It does not grant a license to Fork™s undisclosed implementation, trademarks, proprietary architecture, or controlled operating materials.

## AI Governance Mapping System v0.1

Fork now includes an architecture scaffold for placing AI-governance systems before integration or artifact handoff.

The mapping system is not a product claim, standard, legal determination, compliance certification, or adoption claim. It is a doctrine layer for claim-safe AI governance composition.

Core artifacts:

* [AI Governance Mapping System v0.1](docs/AI_GOVERNANCE_MAPPING_SYSTEM_v0_1.md)
* [Claim Boundary Placement Layer v0.1](docs/CLAIM_BOUNDARY_PLACEMENT_LAYER_v0_1.md)
* [AI Governance System Mapping Record Template v0.1](docs/AI_GOVERNANCE_SYSTEM_MAPPING_RECORD_TEMPLATE_v0_1.md)
* [Fork System Mapping Record v0.1](examples/ai_governance_system_mapping/FORK_SYSTEM_MAPPING_RECORD_v0_1.md)

Core rule:

> AI governance cannot be made safe merely by connecting systems. It requires claim-boundary placement before handoff. Otherwise interoperability becomes silent claim inheritance.

Remote verification:

* [Third-Party Remote Mapping Verification v0.1](docs/THIRD_PARTY_REMOTE_MAPPING_VERIFICATION_v0_1.md)

### AI Governance Mapping Record Schema and Checker v0.1

Fork now includes a machine-readable schema and checker for AI Governance System Mapping Records.

Core artifacts:

* [AI Governance Mapping Record Schema and Checker v0.1](docs/AI_GOVERNANCE_MAPPING_RECORD_SCHEMA_AND_CHECKER_v0_1.md)
* [Mapping record JSON Schema v0.1](schemas/ai_governance_system_mapping_record_v0_1.schema.json)
* [Mapping record checker v0.1](tools/check_ai_governance_mapping_record_v0_1.py)
* [Mapping record examples](examples/ai_governance_system_mapping/records/)

The checker classifies records as PASS, FAIL, or INDETERMINATE while preserving explicit non-claims, prohibited claim inheritance, unknowns, authority boundaries, and re-verification requirements.
### Checker Doctrine Alignment Review v0.1

Fork now includes a semantic alignment review for the AI Governance Mapping Record checker.

Core artifacts:

* [Checker Doctrine Alignment Review v0.1](docs/CHECKER_DOCTRINE_ALIGNMENT_REVIEW_v0_1.md)
* [Machine-readable alignment receipt v0.1](output/semantic_alignment_reviews/CHECKER_DOCTRINE_ALIGNMENT_REVIEW_v0_1.json)

The review concludes that the v0.1 checker is aligned with Fork doctrine as a bounded declaration-based claim-boundary checker, while preserving explicit gaps for v0.2 hardening.
### AI Governance Mapping Record Checker Hardening v0.2

Fork now includes a v0.2 hardening layer for AI Governance Mapping Record checking.

Core artifacts:

* [AI Governance Mapping Record Checker Hardening v0.2](docs/AI_GOVERNANCE_MAPPING_RECORD_CHECKER_HARDENING_v0_2.md)
* [Mapping record JSON Schema v0.2](schemas/ai_governance_system_mapping_record_v0_2.schema.json)
* [Mapping record checker v0.2](tools/check_ai_governance_mapping_record_v0_2.py)
* [Mapping record v0.2 examples](examples/ai_governance_system_mapping/records_v0_2/)
* [Mapping record v0.2 checks](output/ai_governance_mapping_record_checks_v0_2/)

The v0.2 checker adds schema-equivalent validation, ID-reference integrity across safe handoffs, paraphrased claim-inheritance guards, active unresolved unknown handling, and normalized result output for cross-environment comparison.

### AI Governance Mapping Record Checker Hardening v0.2.1

Fork now includes a precision hardening patch for the AI Governance Mapping Record checker.

Core artifacts:

* [AI Governance Mapping Record Checker Hardening v0.2.1](docs/AI_GOVERNANCE_MAPPING_RECORD_CHECKER_HARDENING_v0_2_1.md)
* [Mapping record JSON Schema v0.2.1](schemas/ai_governance_system_mapping_record_v0_2_1.schema.json)
* [Mapping record checker v0.2.1](tools/check_ai_governance_mapping_record_v0_2_1.py)
* [Mapping record v0.2.1 fixtures](examples/ai_governance_system_mapping/records_v0_2_1/)

v0.2.1 adds duplicate-ID detection, safe-handoff self-reference detection, combined failure-mode coverage, schema version mismatch handling, missing schema behavior, malformed JSON tests, and Unicode-aware lexical restricted-claim matching while preserving Fork's non-claim posture.

<!-- FORK_AI_GOVERNANCE_MAPPING_RECORD_V0_2_2 -->

## AI Governance Mapping Record checker hardening v0.2.2

Fork v0.2.2 is a final stabilization patch for the AI Governance Mapping Record checker. It adds static error codes, local multi-hop safe-handoff cycle detection inside one record, parser-boundary fixtures, performance smoke coverage, normalized output comparison guidance, and overclaim-language regression coverage.

This remains a bounded evidence-boundary checker. It does not claim legal admissibility, compliance satisfaction, audit sufficiency, AI output correctness, decision correctness, source completeness, runtime control, policy authority, institutional authority, graph-wide cycle immunity, external artifact verification, or semantic intent understanding.

## AI Governance System Placement Profile v0.1 schema and fixtures

This repository includes an initial schema and fixture set for the AI Governance Mapping Record: System Placement Profile v0.1.

This is a doctrine-to-schema bridge, not a checker or runtime feature.

Artifacts:

- `docs/AI_GOVERNANCE_SYSTEM_PLACEMENT_PROFILE_v0_1.md`
- `docs/AI_GOVERNANCE_SYSTEM_PLACEMENT_PROFILE_SCHEMA_AND_FIXTURES_v0_1.md`
- `schemas/ai_governance_system_placement_profile_v0_1.schema.json`
- `examples/ai_governance_system_placement_profile/records_v0_1/`
- `tests/test_ai_governance_system_placement_profile_schema_fixtures_v0_1.py`

Boundary:

- no semantic claim truth validation;
- no legal or compliance sufficiency claim;
- no audit sufficiency claim;
- no runtime enforcement;
- no institutional authority;
- no cross-record graph validation.

## AI Governance System Placement Profile checker v0.1

This checkpoint adds a bounded checker for `AI Governance Mapping Record: System Placement Profile v0.1` records.

Artifacts:

- `tools/check_ai_governance_system_placement_profile_v0_1.py`
- `tests/test_ai_governance_system_placement_profile_checker_v0_1.py`
- `docs/AI_GOVERNANCE_SYSTEM_PLACEMENT_PROFILE_CHECKER_v0_1.md`
- `output/ai_governance_system_placement_profile_checks_v0_1/*.json`

The checker validates structure, local references, explicit claim/non-claim boundaries, restricted authority leakage, duplicate IDs, declared unresolved unknowns, and normalized outputs.

It does not validate semantic truth, legal sufficiency, compliance sufficiency, audit sufficiency, model safety, runtime behavior, external artifact existence, cross-record graph validity, or institutional authority.

## AI Governance System Placement Profile Checker hardening v0.1.1

The Placement Profile checker line includes a v0.1.1 precision hardening patch.

Artifacts:

- `tools/check_ai_governance_system_placement_profile_v0_1_1.py`
- `tests/test_ai_governance_system_placement_profile_checker_v0_1_1.py`
- `docs/AI_GOVERNANCE_SYSTEM_PLACEMENT_PROFILE_CHECKER_HARDENING_v0_1_1.md`
- `docs/AI_GOVERNANCE_SYSTEM_PLACEMENT_PROFILE_NORMALIZED_OUTPUT_COMPARISON_GUIDE_v0_1_1.md`
- `examples/ai_governance_system_placement_profile/records_v0_1_1/INVALID_UNICODE_RESTRICTED_CLAIM_BYPASS_v0_1_1.json`
- `output/ai_governance_system_placement_profile_checks_v0_1_1/`

This patch hardens parser-boundary behavior, Unicode-aware restricted-claim bypass detection, exit-code documentation, performance smoke coverage, overclaim-language regression coverage, normalized output comparison guidance, and missing-schema/path edge cases.

This remains a structural and boundary checker. It is not semantic validation, legal sufficiency, compliance sufficiency, audit sufficiency, runtime enforcement, external artifact resolution, cross-record graph validation, or institutional authority.

### AI Governance System Placement Profile Structural Execution Receipts v0.2 design addendum

The v0.2 receipt design addendum clarifies that the primary artifact name is Structural Execution Receipt, with Checker Hash Receipt as technical shorthand. It separates normalized-output hash comparison from full source recompute verification and preserves the hash scope NORMALIZED_CHECKER_OUTPUT_ONLY.

This is a design addendum only. It is not a schema, checker, implementation, runtime feature, or authority expansion.

### AI Governance System Placement Profile Structural Execution Receipts v0.2 implementation

Adds a bounded checker/output extension for Structural Execution Receipt artifacts.

- Adds 	ools/check_ai_governance_system_placement_profile_v0_2.py.
- Adds --emit-receipt for SHA-256 receipts over normalized checker outputs.
- Adds --verify-receipt for normalized-output hash comparison.
- Adds --full-recompute for source profile + schema + checker rerun before receipt comparison.
- Keeps hash scope limited to NORMALIZED_CHECKER_OUTPUT_ONLY.
- Uses SHA-256 only.
- Does not change the Placement Profile schema.
- Does not validate semantic truth, legal sufficiency, compliance sufficiency, audit sufficiency, model safety, runtime behavior, external artifacts, cross-record graphs, or institutional authority.


# Fork Transition Localization (v0.1)

This repository defines and exercises the Transition Localization discipline: a method for analyzing how authority over property claims moves between artifact states and contexts.

## Artifact Structure

- `docs/TRANSITION_LOCALIZATION_INVARIANTS_v0_1.md`  
  Defines the invariant grammar for Transition Localization. This is the normative dependency for all downstream artifacts.

- `docs/CASEBOOK_TRANSITION_LOCALIZATION_v0_1.md`  
  Specifies the casebook procedure: how to apply the invariants to concrete transitions (establishment ? transition ? mechanism ? determination ? classification).

- `docs/cases/CASE_001_AI_SAFETY_FINE_TUNE.md`  
  First calibration case: AI safety evaluation ? fine-tuned derivative model.
  - Purpose: test whether reviewers can separate disagreement about the artifact from agreement about the authority path.
  - Outcome: Class D (Unlocalized transfer path) for this specific transition, without judging whether the fine-tuned model is safe.

- `docs/cases/CASE_001_REVIEW_WORKSHEET.md`  
  Reviewer worksheet for Case 001.
  - Captures establishment localization, transition definition, boundary inventory, assumptions, mechanism identification, determination path, classification, and confidence per stage.

- `docs/cases/CASE_001_VARIANCE_REPORT.md`  
  Template for summarizing reviewer variance on Case 001.
  - Distinguishes observational variance (seeing different facts) from procedural variance (applying rules differently) and taxonomic variance (mapping determination to A/B/C/D).

## Calibration vs Validation

- **Calibration (Case 001)**  
  - Question: Can reviewers execute the procedure consistently on a structurally simple transition?  
  - Metrics: agreement on establishment, transition, boundaries, mechanism identification, determination path, classification; plus confidence per stage.

- **Validation (Cases 002�003 and beyond)**  
  - Question: Does the procedure remain stable when transitions are genuinely ambiguous and domain intuitions conflict?  
  - Metrics: agreement under competing intuitions, partial mechanisms, contested scope, overlapping boundary types.

## Empirical Claim (Target for v0.1)

The initial empirical goal is:

> Independent reviewers applying the same Transition Localization procedure are able to reproduce establishment localization, transition determination, and classification outcomes for the same transition scenario.

This claim is modest by design. It does not assert that classifications are objectively correct or that artifacts are safe or unsafe. It asserts that the authority-path analysis is reproducible across reviewers.

Further cases (e.g., cloud certification ? workload claims, medical validation ? configuration drift) will extend this evidence across domains.

## Transition Localization Measurement Layer

The repository now includes reviewer calibration artifacts:

- `docs/cases/CASE_001_REVIEW_WORKSHEET.md`
- `docs/cases/CASE_001_VARIANCE_REPORT.md`

These capture independent application of the Transition Localization procedure.

Measurement focuses on:

- establishment localization,
- transition definition,
- boundary inventory,
- me- determination path,
- classification reproducibility.

The goal is procedural measurement, not artifact judgment.
