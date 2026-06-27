# Fork Surface Maturity Register v0.1

**Document ID:** `FORK_SURFACE_MATURITY_REGISTER_v0_1`
**Status:** Draft v0.1
**Intended path:** `docs/FORK_SURFACE_MATURITY_REGISTER_v0_1.md`
**Companion document:** `docs/FORK_EXECUTABLE_EVIDENCE_SURFACE_MAP_v0_1.md`
**Boundary posture:** Preservation without inheritance.
**Branch caveat:** This register records branch-visible maturity only. A surface is only classified at a given maturity level when the corresponding documents, schemas, tools, fixtures, reports, or independent execution records are present in the branch or release being evaluated.

---

## 1. Purpose

This register classifies the maturity of Fork evidence surfaces.

The companion Surface Map names the executable evidence surfaces and defines what each surface can and cannot establish.

This register answers a narrower question:

> What maturity level does each named surface visibly reach in the current repository branch?

The register is not a release certificate. It is a branch-local maturity inventory.

It exists to prevent a named surface from being mistaken for a completed, checker-backed, fixture-backed, report-backed, or independently reproduced evidence surface when the branch does not yet contain the corresponding artifacts.

---

## 2. Controlling rule

A surface may only be classified at the highest level supported by branch-visible evidence.

Narrative discussion does not imply implementation.

A checker file does not imply fixture coverage.

Fixture coverage does not imply receipt-backed execution.

Receipt-backed execution does not imply independent reproduction.

Independent reproduction does not expand the claim beyond the surface's declared boundary.

---

## 3. Maturity levels

This register uses the same evidence-surface depth model as the Surface Map, with maturity labels added for branch review.

| Level | Maturity label | Requirement | What it supports | What it does not support |
|---|---|---|---|---|
| M0 / EES-0 | Narrative or unobserved | Surface is described conceptually or not visibly present in branch inventory | Orientation, doctrine, future work | Executable evidence claim |
| M1 / EES-1 | Structured artifact | Surface has parseable structured artifacts or declared record shapes | Artifact inspection | Checker-backed conformance |
| M2 / EES-2 | Schema-constrained | Surface has schema constraints or equivalent structural requirements | Schema validation | Behavioral checking or fixture coverage |
| M3 / EES-3 | Checker-backed | Surface has deterministic checker, validator, replay script, or policy evaluator | Bounded machine result | Fixture coverage or executed receipt |
| M4 / EES-4 | Fixture-backed | Surface has positive and negative examples or tests | Demonstrated expected behavior | Preserved execution receipt |
| M5 / EES-5 | Receipt-backed | Surface has reports, release records, or validation outputs tied to execution | Recomputable review of a run | Independent reproduction |
| M6 / EES-6 | Independently reproduced | Surface has clean-room or independent execution evidence | Stronger provenance and reproducibility | Endorsement, certification, approval, truth, compliance, or legal sufficiency |

The maturity level is evidentiary, not normative.

A higher maturity level means the branch preserves more executable support for the bounded surface result. It does not broaden the claim.

---

## 4. Current branch maturity register

The following classifications are based on branch-visible repository inventory and should be updated whenever files, tests, tools, reports, or external reproduction evidence change.

| Surface ID | Surface name | Branch-visible evidence | Highest visible maturity | Current determination | Required next step |
|---|---|---|---|---|---|
| `EES-CBC` | Claim Boundary Contract | Docs, checker, examples, tests | M4 / EES-4 | Fixture-backed executable surface | Add or bind current validation receipt if promoting to M5 |
| `EES-ARTIFACT-CBC` | Artifact claim boundary enforcement | Enforcement doc, checker, examples, tests | M4 / EES-4 | Fixture-backed executable enforcement surface | Add release/report receipt if promoting to M5 |
| `EES-CBB` | Claim Boundary Binding | Binding doc, binding tool, tests | M4 / EES-4 | Fixture-backed binding surface when tests cover binding behavior | Add explicit example inventory and receipt if promoting to M5 |
| `EES-CCE` | Claim Consumption Event | Docs, checker, examples, tests | M4 / EES-4 | Fixture-backed executable consumption surface | Add current validation report if promoting to M5 |
| `EES-RGV` | Relational Graph Verifier | Docs, checkers, examples, tests | M4 / EES-4 | Fixture-backed graph/non-claim preservation surface | Add report-backed execution if promoting to M5 |
| `EES-CCEC` | CCEC Governance Interoperability Profile | Docs, checker, examples, tests | M4 / EES-4 | Fixture-backed governance-interoperability mapping surface | Add report-backed execution if promoting to M5 |
| `EES-SMR` | System Mapping Receipt | Docs, checker, examples, simulations, tests | M4 / EES-4 | Fixture-backed system mapping surface | Bind simulation outputs to validation report if promoting to M5 |
| `EES-BCEI` | Boundary-Crossing Evidence Inspectability Layer | Doc, checker, examples, tests | M4 / EES-4 | Fixture-backed inspectability surface | Add execution receipt or report if promoting to M5 |
| `EES-BDR` | Boundary Delta Record | Doc, checker, examples, tests; BDR/ESAL handoff report present | M5 / EES-5 for handoff path; M4 / EES-4 for base BDR unless separately receipt-bound | Report-backed for BDR/ESAL handoff; fixture-backed for base BDR surface unless a base BDR report is cited | Separate base BDR validation report from BDR/ESAL handoff report if needed |
| `EES-GLM` | Governance Layer Manifest | Manifest-related checker/tests visible in branch inventory; GLM declaration posture depends on manifest files present in evaluated branch | M4 / EES-4 when manifest files and tests are present | Declaration-checker-backed surface; no external recognition implied | Keep external registry, approval, compatibility, and endorsement non-claims explicit |
| `EES-NIG` | Non-Inheritance Guardrails | No branch-visible guardrail policy files identified in current inventory | M0 / EES-0 | Candidate or external/specification-level surface only | Add policy files, examples, and tests before classifying as executable |
| `EES-MCS` | Minimal Claim Schema | No branch-visible minimal-claim schema file identified in current inventory | M0 / EES-0 | Candidate or specification-level surface only | Add schema, examples, and validation path before classifying as schema-backed |
| `EES-TIS` | Transition Integrity Specification | No branch-visible TIS file identified in current inventory | M0 / EES-0 | Candidate semantic-kernel surface only unless files are added | Add TIS document first; add checker/fixtures later if promoting |
| `EES-ESAL` | Event State Artifact Loop | Docs, conformance kit, PowerShell tools, reports | M5 / EES-5 | Receipt-backed conformance/replay surface | Independent reproduction required for M6 |

---

## 5. Maturity notes by surface

### 5.1 Claim Boundary Contract

The Claim Boundary Contract surface is mature enough to be treated as fixture-backed on the current branch when its documents, checker, examples, and tests are present.

Its maturity supports structural boundary conformance only.

It does not establish truth, legal sufficiency, compliance, approval, certification, safety, or authority transfer.

### 5.2 Artifact claim boundary enforcement

The artifact enforcement surface raises the Claim Boundary Contract from an optional convention to a repository enforcement layer for governed artifacts.

Its maturity supports the claim that certain artifact classes can be checked for required boundary presence and form.

It does not establish that any governed artifact's substantive claim is correct or externally accepted.

### 5.3 Claim Boundary Binding

The binding surface is mature when branch-visible binding documentation, binding tooling, and tests are present.

If explicit examples are incomplete or not clearly inventoried, the maturity should remain M4 only when tests demonstrably cover both valid and invalid binding behavior.

It does not convert a profile into certification.

### 5.4 Claim Consumption Event

The Claim Consumption Event surface is mature enough to preserve downstream reliance behavior when docs, checker, examples, and tests are present.

Its most important maturity property is expansion discipline: an expanded downstream use requires a new claim boundary reference.

It does not decide whether the downstream reliance was lawful, prudent, sufficient, or institutionally accepted.

### 5.5 Relational Graph Verifier

The RGV surface is mature when graph preservation, non-claim preservation, and result binding checks are represented by docs, tools, examples, and tests.

It supports structural relationship integrity.

It does not make graph relationships into permissions, approvals, or inherited authority.

### 5.6 CCEC Governance Interoperability Profile

The CCEC surface is mature enough to be treated as fixture-backed when its profile, checker, prohibited mappings, examples, and tests are visible.

Its maturity supports boundary-preserving mapping into host governance contexts.

It does not establish host-system conformance, audit acceptance, control satisfaction, compliance, or risk-score correctness.

### 5.7 System Mapping Receipt

The SMR surface is mature when docs, checker, examples, simulations, and tests are present.

Its maturity supports declared mapping-state classification.

It does not establish system safety, runtime permission, governance approval, external validation, or correctness of the mapped system.

### 5.8 Boundary-Crossing Evidence Inspectability Layer

The BCEI surface is mature when the branch contains its document, checker, examples, and tests.

Its maturity supports detection of inspectability failures and authority-borrowing attempts.

It does not determine the policy consequence of a failed or successful handoff.

### 5.9 Boundary Delta Record

The BDR surface should be classified carefully.

Base BDR maturity is fixture-backed when the branch contains BDR documentation, checker, examples, and tests.

BDR/ESAL handoff maturity may be receipt-backed when a specific handoff validation report is present.

These should not be collapsed into one claim.

A BDR result of `INSPECTABLE` does not mean valid, compliant, lawful, safe, approved, or true.

### 5.10 Governance Layer Manifest

The GLM surface is a declaration-checker-backed surface when manifest files, local declaration checker, digest tooling, and tests are present in the evaluated branch.

Its maturity supports structural declaration of Fork's governance-layer posture.

It does not establish external approval, EVIDE compatibility, GLM registry acceptance, endorsement, interoperability recognition, runtime control, or truth certification.

### 5.11 Non-Inheritance Guardrails

The Non-Inheritance Guardrails surface should remain M0 in this register unless guardrail policy files, inputs, and tests are present in the evaluated branch.

Discussion of guardrails is not enough to classify the surface as executable.

If OPA/Rego policy files are later added with test inputs, this surface may be promoted to M3 or M4.

### 5.12 Minimal Claim Schema

The Minimal Claim Schema surface should remain M0 unless a specific schema file, example objects, and validation path are present in the evaluated branch.

A claim-schema concept is not equivalent to a branch-visible schema-backed surface.

If added, it should start at M2 and only rise to M3/M4 when checker and fixture coverage exist.

### 5.13 Transition Integrity Specification

TIS should remain M0 unless a branch-visible TIS document is present.

If a TIS document is added without tooling, it should be classified as M1 at most.

If a transition validator is later added, maturity should be raised only to the level supported by schemas, checkers, fixtures, and receipts.

### 5.14 Event State Artifact Loop

ESAL is mature enough to be classified as receipt-backed when docs, conformance kit, replay/conformance tools, and reports are present.

Its maturity supports branch-visible replay or conformance evidence.

It does not establish external policy correctness, runtime authorization, legal consequence, or institutional acceptance.

---

## 6. Promotion rules

A surface may be promoted only when the branch contains the artifacts required for the target level.

### 6.1 Promotion to M1

Requires at least one branch-visible document or structured artifact defining the surface.

### 6.2 Promotion to M2

Requires a schema, formal record shape, or equivalent machine-checkable structural constraint.

### 6.3 Promotion to M3

Requires a deterministic checker, validator, replay script, or policy evaluator.

### 6.4 Promotion to M4

Requires positive and negative fixtures, tests, or examples that demonstrate expected acceptance and rejection behavior.

### 6.5 Promotion to M5

Requires a preserved execution receipt, validation report, release record, or conformance report tied to the surface.

A report should identify the command, tool, inputs, output token, commit or version, and limitations.

### 6.6 Promotion to M6

Requires independent reproduction, clean-room execution, or third-party replay evidence.

Reviewer comments alone are not sufficient.

Independent reproduction does not imply endorsement unless endorsement is separately and explicitly granted.

---

## 7. Demotion rules

A surface should be demoted when any of the following occurs:

- A checker is removed.
- Tests are removed or no longer cover the stated surface behavior.
- Examples no longer correspond to checker expectations.
- Output tokens change semantics without updated boundary documentation.
- Reports become stale relative to changed checker behavior.
- Branch inventory no longer contains the files used to support the prior maturity level.
- A maturity claim depends on private discussion, reviewer observation, or external association without explicit written recognition.

Demotion is not failure. It is boundary hygiene.

---

## 8. Gap tokens

The following gap tokens should be used when recording maturity limitations.

| Gap token | Meaning |
|---|---|
| `NOT_BRANCH_VISIBLE` | The surface is not visible in the evaluated branch inventory |
| `NARRATIVE_ONLY` | The surface is described but has no structured artifact, checker, or test path |
| `STRUCTURE_WITHOUT_SCHEMA` | Structured artifacts exist but no schema or equivalent constraints are visible |
| `SCHEMA_WITHOUT_CHECKER` | Schema exists but no deterministic checker or validation path is visible |
| `CHECKER_WITHOUT_FIXTURES` | Checker exists but positive/negative fixture coverage is not visible |
| `FIXTURES_WITHOUT_RECEIPT` | Fixtures/tests exist but no execution receipt or report is preserved |
| `REPORT_WITHOUT_COMMAND` | Report exists but does not preserve command or replay method |
| `REPORT_WITHOUT_COMMIT` | Report exists but is not bound to commit or equivalent version reference |
| `REPORT_WITHOUT_LIMITATIONS` | Report exists but does not preserve bounded non-claims or limitations |
| `INDEPENDENCE_UNESTABLISHED` | Execution evidence exists but independent reproduction is not established |
| `EXTERNAL_RECOGNITION_UNESTABLISHED` | External registry, compatibility, approval, or endorsement is not established |
| `HOST_CONFORMANCE_UNESTABLISHED` | Fork boundary structure exists but host-system conformance is not established |
| `SURFACE_COLLAPSE_RISK` | Two related surfaces risk being collapsed into one maturity claim |
| `AUTHORITY_EXPANSION_RISK` | Maturity wording risks implying authority beyond the declared boundary |

Gap tokens are records of evidence posture. They are not substantive invalidity findings.

---

## 9. Release-gate use

A release gate may use this register to decide whether a surface can be cited as:

- Narrative only.
- Structured.
- Schema-backed.
- Checker-backed.
- Fixture-backed.
- Receipt-backed.
- Independently reproduced.

A release gate should not cite this register as proof of:

- Legal admissibility.
- Legal sufficiency.
- Regulatory compliance.
- Safety certification.
- Security certification.
- Audit acceptance.
- Host-system conformance.
- Runtime control.
- Runtime authorization.
- Institutional approval.
- External endorsement.
- Truth verification.
- Universal interoperability.

The register is a maturity boundary document.

---

## 10. Recommended commit discipline

When committing this register with the Surface Map, the commit should preserve the distinction between the two artifacts.

Recommended commit scope:

```text
docs: add Fork executable evidence surface map and maturity register
```

Recommended commit body:

```text
Add a branch-local maturity register companion to the executable evidence surface map.

The surface map names Fork executable evidence surfaces and their bounded claims.
The maturity register classifies each surface by branch-visible evidence level.

No external authority, compliance, approval, truth, runtime-control, interoperability, or endorsement claims are introduced.
```

Do not include generated caches, local execution byproducts, or unrelated report mutations in the same commit.

---

## 11. v0.1 determination

The current branch appears to contain multiple fixture-backed executable evidence surfaces and at least two receipt-backed/conformance-backed paths.

The strongest branch-visible maturity appears around:

- Claim Boundary Contract.
- Artifact claim boundary enforcement.
- Claim Consumption Events.
- CCEC Governance Interoperability.
- System Mapping Receipt.
- Boundary-Crossing Evidence Inspectability.
- Boundary Delta Record.
- Relational Graph Verifier.
- Event State Artifact Loop.

The weakest or least branch-visible maturity appears around:

- Transition Integrity Specification.
- Minimal Claim Schema.
- Non-Inheritance Guardrails.

Those weaker surfaces may remain important doctrinally or architecturally, but they should not be represented as branch-executable surfaces until branch-visible files support that classification.

---

## 12. Summary boundary

This register answers:

> What evidence-surface maturity is visible in this branch?

It does not answer:

> Are the underlying governance decisions legally sufficient, compliant, safe, true, approved, externally recognized, or authorized for deployment?

That boundary remains controlling.

Preservation without inheritance remains the governing rule.
