# Fork Research Program v0.1

## Evidence-Governed Validation Package

**Instantiated:** 2026-08-06  
**Author and change authority:** Ryan Feller, individual capacity  
**ORCID:** 0009-0000-7863-5792  
**Conceptual phase:** `CLOSED`  
**Program phase:** `EMPIRICAL_VALIDATION`  
**Admitted evaluation:** `BLOCKED_PENDING_REPOSITORY_BINDING`

This package instantiates the closure of Fork's conceptual-development phase. It establishes the procedural governance contract, freezes the provisional model entering testing, and creates the initial operational surfaces needed to begin evidence-governed evaluation.

It does not report empirical validation, independent reproduction, conformance, production readiness, legal validity, compliance, or institutional acceptance.

## Controlling artifacts

| Artifact | Function | Standing |
| --- | --- | --- |
| `FORK_RFC_0_v0.1.md` | Governs how the model may change | `PROVISIONAL_GOVERNANCE_SPECIFICATION` |
| `FORK_CANDIDATE_MODEL_v0.1_FREEZE_RECORD.md` | Identifies what enters empirical testing | `PROVISIONAL_RESEARCH_BASELINE` |
| `baseline_manifest_v0.1.yaml` | Binds the standalone artifact set by digest | `STANDALONE_BINDING_COMPLETE`; repository binding unresolved |
| `schemas/classification-event-v0.1.schema.yaml` | Makes classifications attributable events | Provisional schema |
| `schemas/transformation-case-v0.1.schema.yaml` | Defines corpus case submission | Provisional schema |
| `schemas/failure-ledger-entry-v0.1.schema.yaml` | Separates observation, diagnosis, and disposition | Provisional schema |
| `schemas/negative-result-entry-v0.1.schema.yaml` | Preserves compression and rejection evidence | Provisional schema |
| `procedures/independent-challenge-procedure-v0.1.md` | Declares minimum independent-challenge requirements | Provisional procedure |
| `corpus/fixture-manifest-v0.1.yaml` | Binds admitted fixtures | Empty at instantiation |
| `corpus/validation-corpus-manifest-v0.1.yaml` | Opens the first empirical corpus | Empty at instantiation |

## Resolved classification-event status

`classification_event` is included in Candidate Model v0.1 as a provisional **evaluation-record type**. It records how an evaluator classified a transformation under a declared procedure, profile, evidence basis, scope, and time.

It is not:

- an intrinsic property of the transformation;
- an automatic conformance finding;
- a truth determination;
- an authority transfer; or
- a majority-vote resolution mechanism.

## Current binding boundary

The package's files can be bound to one another by SHA-256. Repository identity, commit SHA, and tree digest cannot be truthfully populated until the package is admitted to a repository. Consequently:

```yaml
canonical_binding:
  standalone_artifact_binding: COMPLETE
  repository_binding: UNRESOLVED_PENDING_REPOSITORY_ADMISSION
  admitted_evaluation: BLOCKED
```

The generated `SHA256SUMS` file records the exact standalone bytes. After repository admission, `baseline_manifest_v0.1.yaml` must be completed in a successor binding action without rewriting the already identified source artifacts.

## Next authorized sequence

1. Admit this package to the intended repository.
2. Record repository identity, commit SHA, and tree digest.
3. Verify all artifact hashes.
4. Open corpus case admission under the frozen baseline.
5. Populate ledgers only from preserved cases, reproductions, diagnoses, and governance actions.
6. Consider model change only through RFC 0.

