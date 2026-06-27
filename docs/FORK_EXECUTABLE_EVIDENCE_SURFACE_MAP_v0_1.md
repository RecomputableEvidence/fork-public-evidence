# Fork Executable Evidence Surface Map v0.1

**Document ID:** `FORK_EXECUTABLE_EVIDENCE_SURFACE_MAP_v0_1`
**Status:** Draft v0.1
**Intended path:** `docs/FORK_EXECUTABLE_EVIDENCE_SURFACE_MAP_v0_1.md`
**Applies to:** Fork public evidence repository surfaces that produce, consume, validate, or preserve machine-checkable evidence artifacts.
**Boundary posture:** Preservation without inheritance.
**Branch caveat:** This map describes surfaces present or emerging in the Fork public evidence repository family. A surface is only in force for a given branch or release when the corresponding files, schemas, tools, fixtures, and reports are present in that branch or release.

---

## 1. Purpose

This document maps the executable evidence surfaces in Fork.

An **executable evidence surface** is any repository surface where a governance-relevant assertion is not merely described in prose, but is represented in a structured artifact that can be checked, replayed, recomputed, validated, rejected, or inspected by deterministic tooling.

This map exists to distinguish:

1. Narrative doctrine.
2. Structured evidence artifacts.
3. Machine-checkable schemas.
4. Executable checkers.
5. Test fixtures and conformance examples.
6. Execution receipts, reports, and validation outputs.
7. Boundary records consumed by downstream systems.

The map does not expand the meaning of any underlying artifact. It records where executable evidence exists, what each surface can establish, and what each surface explicitly does not establish.

---

## 2. Core rule

Fork evidence surfaces preserve claims, non-claims, evidence references, structural verification results, and boundary conditions.

They do not silently transfer authority, compliance, legal sufficiency, safety, truth, approval, endorsement, interoperability recognition, runtime permission, or institutional acceptance from one artifact, system, reviewer, or context to another.

A surface may preserve that a claim was made.

A surface may preserve that a checker produced a bounded result.

A surface may preserve that a transition was inspectable.

A surface may not convert those facts into broader authority unless a new claim boundary explicitly establishes that authority in the new context.

---

## 3. Definitions

### 3.1 Executable evidence surface

A repository surface that satisfies all of the following conditions:

- It has a defined input artifact or input class.
- It has a declared checker, validator, policy rule, replay function, or deterministic inspection procedure.
- It emits a bounded output token, report, receipt, pass/fail state, violation list, or structured determination.
- It declares or inherits a non-expansion boundary.
- Its result can be rerun, inspected, or compared against preserved evidence.

### 3.2 Narrative surface

A document surface that explains doctrine, semantics, intended use, limitations, or operating posture, but does not itself produce a machine-checkable result.

Narrative surfaces may guide interpretation. They do not by themselves establish executable evidence.

### 3.3 Structural determination

A bounded result showing that an artifact satisfies declared structural rules.

A structural determination is not a legal, safety, compliance, truth, endorsement, or operational approval determination.

### 3.4 Inspectability determination

A bounded result showing whether a transition or handoff preserved enough declared information for downstream inspection.

An inspectability determination is not a policy consequence, validity certification, or approval decision.

### 3.5 Expansion authority gap

A recorded condition where an artifact, mapping, or transition attempts to expand a claim beyond its declared boundary without supplying a new authority reference and evidence reference sufficient to support the expanded claim as a new claim.

Recording an expansion authority gap does not prove misconduct, invalidity, or illegality. It preserves the fact that the expansion was not structurally established within Fork's boundary rules.

---

## 4. Surface levels

Fork distinguishes evidence surfaces by executable depth.

| Level | Name | Description | Example output |
|---|---|---|---|
| EES-0 | Narrative only | Doctrine, explanation, or design notes with no direct executable result | Markdown guidance |
| EES-1 | Structured artifact | JSON, YAML, Markdown front matter, manifest, or sidecar that can be parsed | Claim boundary object |
| EES-2 | Schema-constrained artifact | Structured artifact validated against a schema | Schema validation result |
| EES-3 | Checker-constrained artifact | Artifact evaluated by a deterministic checker | `STRUCTURAL_PASS`, `NOT_INSPECTABLE`, violation list |
| EES-4 | Fixture-backed checker | Checker result covered by positive and negative fixtures | Test suite result |
| EES-5 | Receipt-backed execution | Executed result preserved with command, commit, checker version, and report metadata | Validation report, execution artifact |
| EES-6 | Independently reproducible evidence | Receipt-backed execution reproduced by an independent evaluator or clean-room run | Independent execution artifact |

These levels are not product maturity scores. They are evidence-surface classifications.

A higher level does not expand the claim. It only increases the inspectability and recomputability of the bounded result.

---

## 5. Named and branch-conditional evidence surfaces

The following surfaces are named Fork evidence surfaces. A surface is executable in a given branch only when the corresponding files, schemas, tools, fixtures, and reports are present in that branch. Surfaces without branch-visible implementation remain candidate, narrative, or specification-level surfaces as classified by the companion maturity register.

### 5.1 Claim Boundary Contract surface

**Surface ID:** `EES-CBC`
**Primary function:** Records the boundary of a claim and its declared non-claims.
**Surface class:** Structured artifact, schema, checker, examples, tests.

| Field | Value |
|---|---|
| Input artifacts | Claim boundary sidecars, release artifacts, receipts, examples |
| Executable mechanism | Claim boundary schema and checker |
| Typical output | Structural conformance result |
| Establishes | Presence and structural validity of declared claim boundary fields |
| Does not establish | Truth, legal sufficiency, compliance, approval, safety, authority transfer |
| Expansion rule | Downstream use may narrow; expansion requires a new claim boundary |

The Claim Boundary Contract surface is the primary executable boundary primitive. It prevents a preserved claim from being read as broader than the scope, subject, evidence, and non-claims declared in the artifact.

---

### 5.2 Artifact claim boundary enforcement surface

**Surface ID:** `EES-ARTIFACT-CBC`
**Primary function:** Requires governed artifacts to carry a passing claim boundary.
**Surface class:** Checker, release guard, fixture-backed enforcement.

| Field | Value |
|---|---|
| Input artifacts | Release packets, receipts, reports, governed evidence artifacts |
| Executable mechanism | Artifact-level claim boundary checker |
| Typical output | Acceptance or rejection based on boundary presence and structure |
| Establishes | The artifact declares a bounded claim boundary in the required form |
| Does not establish | That the artifact's substantive claim is correct or externally accepted |
| Expansion rule | Missing boundary blocks structural acceptance; it does not decide legal consequence |

This surface makes the claim boundary operational rather than merely advisory.

---

### 5.3 Claim Boundary Binding surface

**Surface ID:** `EES-CBB`
**Primary function:** Binds claim profiles to declared evidence scopes.
**Surface class:** Binding artifact, checker, profile registry.

| Field | Value |
|---|---|
| Input artifacts | Claim profiles, evidence receipts, boundary contracts |
| Executable mechanism | Binding checker |
| Typical output | Bound profile result or structural rejection |
| Establishes | That a specific profile is structurally bound to an artifact under declared scope |
| Does not establish | That the profile is sufficient for external governance, legal, audit, or compliance use |
| Expansion rule | Profile binding cannot be read as certification outside its declared verification scope |

The binding surface supports profile-specific evidence use while preserving non-inheritance of authority.

---

### 5.4 Claim Consumption Event surface

**Surface ID:** `EES-CCE`
**Primary function:** Records downstream reliance on prior claims without allowing silent expansion.
**Surface class:** Structured event, schema, checker, fixture-backed examples.

| Field | Value |
|---|---|
| Input artifacts | Downstream reliance records, preserved non-claims, relied claims |
| Executable mechanism | Claim Consumption Event checker |
| Typical output | Preserved, narrowed, expanded, or rejected consumption state |
| Establishes | How a downstream consumer represented reliance on an upstream claim |
| Does not establish | That the reliance was appropriate, lawful, sufficient, or approved |
| Expansion rule | `EXPANDED` consumption requires a new claim boundary reference |

The CCE surface is the executable defense against claim inheritance through reuse, citation, or downstream integration.

---

### 5.5 Relational Graph Verifier surface

**Surface ID:** `EES-RGV`
**Primary function:** Checks graph-level relationships among artifacts, claims, references, and unresolved pointers.
**Surface class:** Graph verifier, pointer checker, fixture-backed tests.

| Field | Value |
|---|---|
| Input artifacts | Artifact relationship graphs, pointer bundles, evidence references |
| Executable mechanism | Relational Graph Verifier |
| Typical output | Graph conformance result, unresolved pointer bundle, exit code |
| Establishes | Structural relationship integrity among declared graph elements |
| Does not establish | Semantic truth, authority transfer, external interoperability, or sufficiency of dependencies |
| Expansion rule | Edges preserve declared relation types only; relation does not imply permission |

The RGV surface prevents relationship structure from being mistaken for inherited authority.

---

### 5.6 CCEC Governance Interoperability Profile surface

**Surface ID:** `EES-CCEC`
**Primary function:** Maps Fork evidence into external governance, risk, compliance, audit, or register contexts without creating compliance-oracle behavior.
**Surface class:** Profile, checker, prohibited mapping set, examples, tests.

| Field | Value |
|---|---|
| Input artifacts | CCEC mapping records, GRC references, audit evidence references |
| Executable mechanism | CCEC profile checker |
| Typical output | Structural mapping result or prohibited mapping rejection |
| Establishes | Whether a mapping preserves Fork's boundary constraints |
| Does not establish | Compliance, audit acceptance, risk score correctness, control satisfaction, host-system conformance |
| Expansion rule | Mapping may reference evidence; it may not convert evidence into external authority |

This surface protects Fork from becoming a compliance oracle, scoring engine, routing authority, or host-system policy layer.

---

### 5.7 System Mapping Receipt surface

**Surface ID:** `EES-SMR`
**Primary function:** Records how a system maps, narrows, preserves, expands, or leaves unresolved claim/evidence relationships.
**Surface class:** Receipt, schema, checker, examples, tests.

| Field | Value |
|---|---|
| Input artifacts | System mapping receipts, mapped claims, authority references, evidence references |
| Executable mechanism | SMR checker |
| Typical output | `PRESERVED`, `NARROWED`, `EXPANDED`, `UNRESOLVED`, or `MIXED` mapping classification |
| Establishes | The declared structural mapping state and any recorded authority gap |
| Does not establish | System safety, system correctness, runtime permission, governance approval, external validation |
| Expansion rule | `EXPANDED` mapping requires declared authority and evidence references |

The SMR surface records mapping behavior without absorbing the mapped system's authority or proof obligations.

---

### 5.8 Boundary-Crossing Evidence Inspectability surface

**Surface ID:** `EES-BCEI`
**Primary function:** Makes handoffs inspectable across system, evidence, claim, or governance boundaries.
**Surface class:** Inspection layer, invalid-flag taxonomy, handoff record.

| Field | Value |
|---|---|
| Input artifacts | Boundary-crossing handoff records and evidence transfer records |
| Executable mechanism | Inspectability checks and invalid flag detection |
| Typical output | Handoff inspectability state and invalid flags |
| Establishes | Whether handoff evidence preserves declared boundary information |
| Does not establish | That the handoff is accepted, safe, compliant, authorized, or institutionally valid |
| Expansion rule | Authority borrowing attempts are recorded; they are not normalized |

This surface preserves cross-boundary visibility without permitting authority borrowing.

---

### 5.9 Boundary Delta Record surface

**Surface ID:** `EES-BDR`
**Primary function:** Records and inspects semantic or structural deltas when evidence crosses a boundary.
**Surface class:** Delta record, schema, checker, positive and negative fixtures, validation report.

| Field | Value |
|---|---|
| Input artifacts | Boundary Delta Records, transition descriptors, evidence references |
| Executable mechanism | BDR checker |
| Typical output | `INSPECTABLE` or `NOT_INSPECTABLE`, with derived flags |
| Establishes | Whether the boundary transition preserved enough information for inspection under BDR rules |
| Does not establish | Policy consequence, validity, legal sufficiency, safety, compliance, truth, or approval |
| Expansion rule | Scope generalization, non-claim dropping, evidence suppression, and recomputation-to-truth are detectable invalid patterns |

The BDR surface is an inspectability surface. It is not a governance decision surface.

---

### 5.10 Governance Layer Manifest surface

**Surface ID:** `EES-GLM`
**Primary function:** Declares Fork's governance-layer posture in a machine-readable manifest.
**Surface class:** Manifest, local checker, examples.

| Field | Value |
|---|---|
| Input artifacts | `.well-known/governance-layer-manifest.json`, GLM examples, manifest metadata |
| Executable mechanism | Local GLM declaration checker |
| Typical output | Bounded structural pass or declaration error |
| Establishes | Structural declaration of Fork's governance-layer boundary posture |
| Does not establish | GLM approval, EVIDE compatibility, endorsement, compliance, runtime control, truth certification, or external registry acceptance |
| Expansion rule | Manifest declaration cannot be read as external recognition unless separately granted by the relevant external authority |

The GLM surface is a declaration surface. It does not create interoperability recognition by itself.

---

### 5.11 Non-Inheritance Guardrails surface

**Surface ID:** `EES-NIG`
**Primary function:** Encodes non-inheritance constraints as executable policy checks.
**Surface class:** OPA/Rego policy, gate wrapper, test input surface.

| Field | Value |
|---|---|
| Input artifacts | Execution requests, claim sidecars, scope conditions, evidence references |
| Executable mechanism | Non-inheritance guardrail policy evaluation |
| Typical output | Allow/deny or violation set |
| Establishes | Whether a proposed use violates encoded non-inheritance rules |
| Does not establish | That allowed use is legally sufficient, safe, compliant, approved, or substantively correct |
| Expansion rule | Scope expansion, semantic compression, and transitive assumption are denied unless independently established |

This surface can be used by a host system as a gate, but Fork itself remains out-of-band unless explicitly integrated by that host.

---

### 5.12 Minimal Claim Schema surface

**Surface ID:** `EES-MCS`
**Primary function:** Provides a minimal structured form for claims that can be validated and attached to artifacts.
**Surface class:** JSON Schema, claim sidecar, examples.

| Field | Value |
|---|---|
| Input artifacts | Minimal claim objects and sidecars |
| Executable mechanism | JSON Schema validation |
| Typical output | Schema-valid or schema-invalid claim object |
| Establishes | Presence and shape of minimal claim fields |
| Does not establish | Claim truth, evidentiary sufficiency, legal admissibility, or authority inheritance |
| Expansion rule | A claim object must carry its own subject, scope, evidence references, exclusions, validity bounds, and provenance |

The Minimal Claim Schema is a low-level claim representation surface. It is not a certification surface.

---

### 5.13 Transition Integrity Specification surface

**Surface ID:** `EES-TIS`
**Primary function:** Defines validity transitions as governed events rather than inherited properties.
**Surface class:** Semantic specification, transition tuple model, validator candidate surface.

| Field | Value |
|---|---|
| Input artifacts | Transition descriptions, property/context pairs, mechanisms, evidence, verification records |
| Executable mechanism | Specification-level validation rules; executable checker when implemented |
| Typical output | Transition admissibility findings when backed by tooling |
| Establishes | Whether a transition is represented with required semantic components |
| Does not establish | That the transition is institutionally accepted, legally binding, or externally authoritative |
| Expansion rule | Properties do not become valid in a new context through continuity, association, lineage, ownership, or inheritance alone |

Until backed by a specific checker and fixture set, TIS remains primarily a semantic kernel and EES-0/EES-1 design surface. Implemented validators may raise it to EES-3 or above.

---

### 5.14 Event State Artifact Loop surface

**Surface ID:** `EES-ESAL`
**Primary function:** Tests whether event histories reduce to consistent governance state fingerprints under replay.
**Surface class:** State model, canonicalization procedure, replay/conformance candidate, report surface.

| Field | Value |
|---|---|
| Input artifacts | Event logs, BDR-created events, execution events, state model definitions |
| Executable mechanism | Canonicalization, reduction, replay, fingerprint comparison |
| Typical output | Conformance report, state fingerprint, violation list |
| Establishes | Whether the same event log produces the same governance state fingerprint under declared replay rules |
| Does not establish | External truth, policy correctness, runtime authorization, or legal consequence |
| Expansion rule | Authority, constraints, obligations, lineage, validity, and violations may only change under declared event semantics |

ESAL is the surface for recomputable governance-state behavior. It preserves replay equivalence; it does not decide external adequacy.

---

## 6. Cross-surface boundary matrix

| Surface | Preserves evidence | Checks structure | Detects expansion | Emits bounded result | Blocks runtime action | Establishes external authority |
|---|---:|---:|---:|---:|---:|---:|
| CBC | Yes | Yes | Yes | Yes | No | No |
| Artifact CBC | Yes | Yes | Yes | Yes | No | No |
| CBB | Yes | Yes | Yes | Yes | No | No |
| CCE | Yes | Yes | Yes | Yes | No | No |
| RGV | Yes | Yes | Partial | Yes | No | No |
| CCEC | Yes | Yes | Yes | Yes | No | No |
| SMR | Yes | Yes | Yes | Yes | No | No |
| BCEI | Yes | Yes | Yes | Yes | No | No |
| BDR | Yes | Yes | Yes | Yes | No | No |
| GLM | Yes | Yes | Yes | Yes | No | No |
| NIG | Indirect | Yes | Yes | Yes | Host-dependent | No |
| MCS | Yes | Yes | Partial | Yes | No | No |
| TIS | Conceptual until implemented | Partial | Yes | Partial | No | No |
| ESAL | Yes | Yes | Partial | Yes | No | No |

`Host-dependent` means the surface can be used by a host system to block or route behavior, but Fork does not itself provide runtime control unless separately integrated into that host's execution path.

---

## 7. Standard surface record format

Every new executable evidence surface SHOULD be documented using the following record shape.

```yaml
surface_id: EES-EXAMPLE
surface_name: Example Surface
version: v0.1
surface_level: EES-3
input_artifacts:
  - example_input.json
executable_mechanism:
  - tools/check_example.py
schemas:
  - schema/example.schema.json
fixtures:
  positive:
    - examples/example_valid.json
  negative:
    - examples/example_invalid.json
outputs:
  allowed_tokens:
    - STRUCTURAL_PASS
    - STRUCTURAL_FAIL
bounded_claim:
  establishes:
    - Structural conformance to the declared schema and checker rules.
  does_not_establish:
    - Truth
    - Legal sufficiency
    - Compliance
    - Safety
    - Approval
    - Authority transfer
expansion_rule:
  - Any expanded claim requires a new claim boundary contract.
receipt_requirements:
  - command
  - commit
  - checker_version
  - input_artifact_digest
  - output_token
  - limitations
```

This record shape is descriptive, not itself authoritative unless adopted by a checker or schema.

---

## 8. Evidence receipt requirements

An execution receipt or validation report SHOULD include:

1. Repository name or source location.
2. Branch name.
3. Commit digest.
4. Tool or checker name.
5. Tool or checker version.
6. Command executed.
7. Input artifact paths.
8. Output artifact paths.
9. Output token or result state.
10. Test count when applicable.
11. Fixture classes covered.
12. Known limitations.
13. Reviewer or executor provenance, when available.
14. Timestamp.
15. Non-claim boundary.

A receipt that omits these elements may still preserve useful evidence, but its replay and review value is reduced.

---

## 9. Standard non-claims for executable evidence surfaces

Unless a surface explicitly declares a narrower or more specific non-claim set, Fork executable evidence surfaces do not establish any of the following:

- Legal admissibility.
- Legal sufficiency.
- Regulatory compliance.
- Control satisfaction.
- Audit acceptance.
- Safety certification.
- Security certification.
- Model correctness.
- Output truth.
- Human-review adequacy.
- Institutional approval.
- External endorsement.
- Compatibility recognition.
- Runtime authorization.
- Runtime prevention.
- Deployment readiness.
- Business fitness.
- Identity verification beyond declared identifiers.
- Authority transfer.
- Claim inheritance.

These non-claims are not defects. They are part of Fork's evidence boundary.

---

## 10. Surface interaction rules

### 10.1 Evidence preservation does not imply claim expansion

A downstream surface may cite an upstream receipt, checker result, or artifact.

That citation preserves the upstream evidence reference. It does not import the upstream authority or expand the upstream claim.

### 10.2 Structural pass does not imply semantic pass

A checker result may show that an artifact structurally conforms to Fork rules.

It does not establish that the artifact's substantive assertion is true, sufficient, safe, compliant, approved, or externally accepted.

### 10.3 Inspectable does not imply valid

A BDR or boundary-crossing record may be inspectable.

Inspectability means the transition preserved enough declared information for review. It does not mean the transition is correct or allowed.

### 10.4 Host use does not convert Fork into a host policy authority

A host system may use Fork evidence, guardrails, or checker outputs in its own gates.

That host decision is the host's decision. Fork preserves evidence and boundary structure; it does not become the host's policy authority by being referenced.

### 10.5 Reviewer observation does not imply endorsement

A reviewer may inspect, comment on, reproduce, or discuss a Fork artifact.

Those actions do not create endorsement, approval, compatibility recognition, institutional association, or external validation unless separately and explicitly granted by that reviewer or institution.

---

## 11. Failure and gap taxonomy

Fork should preserve evidence-surface gaps explicitly rather than collapsing them into generic failure.

| Gap token | Meaning |
|---|---|
| `SURFACE_ABSENT` | No executable surface exists for the claimed evidence behavior |
| `SCHEMA_ONLY` | A schema exists but no checker or execution path is present |
| `CHECKER_WITHOUT_FIXTURES` | A checker exists but lacks positive and negative fixture coverage |
| `POSITIVE_PATH_UNESTABLISHED` | Invalid cases may be detected, but valid cases are not demonstrated |
| `NEGATIVE_PATH_UNESTABLISHED` | Valid cases may pass, but invalid cases are not demonstrated |
| `RECEIPT_ABSENT` | Tooling exists, but no execution receipt or report is preserved |
| `PROVENANCE_UNESTABLISHED` | Execution or reviewer identity/method is not recorded |
| `VERSION_UNBOUND` | Result is not bound to checker version, schema version, or commit |
| `OUTPUT_TOKEN_AMBIGUOUS` | Checker result token can be misread as broader than its boundary |
| `NON_CLAIM_ABSENT` | Artifact lacks explicit non-claims |
| `AUTHORITY_EXPANSION_UNRESOLVED` | Expansion is attempted or implied without sufficient new authority binding |
| `LOCALIZATION_UNESTABLISHED` | The surface does not identify where in the transition the establishment occurred |
| `HOST_CONFORMANCE_UNESTABLISHED` | Fork structure is preserved, but host system conformance is not established |

Gap tokens are evidence records. They are not automatic policy judgments.

---

## 12. Release-gate use

A release, validation package, or external handoff MAY cite this map to describe what kind of executable evidence exists.

A release SHOULD NOT cite this map as proof that Fork provides:

- Compliance automation.
- Runtime control.
- Legal certification.
- External approval.
- Safety certification.
- Truth verification.
- Institutional endorsement.
- Universal interoperability.

A release gate SHOULD require that any cited executable surface identify:

1. The surface ID.
2. The surface version.
3. The artifact paths evaluated.
4. The checker or validator used.
5. The executed command or replay method.
6. The output token.
7. The bounded claim.
8. The non-claims.
9. Any unresolved gaps.
10. The evidence receipt or report reference.

---

## 13. Recommended repository placement

Recommended path:

```text
docs/FORK_EXECUTABLE_EVIDENCE_SURFACE_MAP_v0_1.md
```

Recommended future companion artifacts:

```text
schema/fork_executable_evidence_surface_map.schema.json
examples/executable_evidence_surface_map/example_valid_surface_record.json
examples/executable_evidence_surface_map/example_invalid_authority_expansion_surface_record.json
tools/check_executable_evidence_surface_map.py
tests/test_executable_evidence_surface_map.py
reports/FORK_EXECUTABLE_EVIDENCE_SURFACE_MAP_VALIDATION_REPORT.json
```

These companion artifacts are optional for v0.1 unless the map is promoted from narrative documentation to a checker-backed evidence surface.

---

## 14. Versioning rules

This map should be versioned when any of the following changes occur:

- A new executable evidence surface is added.
- A surface changes its output token semantics.
- A checker changes its boundary posture.
- A schema introduces or removes required non-claim fields.
- A receipt format changes replay requirements.
- A surface is promoted from narrative to checker-backed.
- A surface is deprecated or replaced.

Patch versions may be used for editorial clarifications that do not change surface semantics.

---

## 15. v0.1 determination

Fork currently contains multiple executable evidence surfaces that support recomputable, inspectable, structurally bounded evidence for AI-assisted governance workflows.

The executable surface area is strongest where schemas, checkers, fixtures, and reports are all present and bound to specific output tokens.

The executable surface area is weakest where concepts remain specification-level, narrative-only, or not yet backed by positive and negative execution fixtures.

This map does not close those gaps. It makes them visible.

---

## 16. Summary boundary

Fork's executable evidence surfaces answer this class of question:

> What was claimed, what was not claimed, what evidence was referenced, what boundary was declared, what checker or replay was executed, what bounded result was emitted, and whether the record still structurally verifies under the declared rules?

Fork's executable evidence surfaces do not answer this class of question:

> Is the underlying decision legally sufficient, compliant, safe, true, approved, institutionally accepted, or authorized for deployment?

That separation is the evidence surface boundary.

Preservation without inheritance remains the controlling rule.
