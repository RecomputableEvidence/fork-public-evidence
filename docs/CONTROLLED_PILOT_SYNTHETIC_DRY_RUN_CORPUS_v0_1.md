# Controlled Pilot Synthetic Dry-Run Corpus v0.1

**SYNTHETIC ONLY — STRUCTURAL EVIDENCE-BOUNDARY CORPUS; NOT AUTHORIZATION, NOT CLINICAL REVIEW, NOT LEGAL SUFFICIENCY, NOT HIPAA COMPLIANCE, NOT PRODUCTION READINESS, AND NOT A STATUTORY REVIEW PROCESS.**


## Purpose

This corpus provides synthetic JSONL batch exports for exercising the Fork controlled-pilot dry-run path without using real institutional data.

The corpus is designed to demonstrate the controlled-pilot spine after the machine seam, stakeholder orientation layer, and orientation lexicon hardening releases.

It is synthetic only.

It does not use live institutional data, PHI, PII, real patients, real members, real providers, real payers, real claims, real medical records, real authorization requests, real appeal records, real source-system exports, or real live-ingestion authorization workflows.

## Scope

The corpus models a synthetic prior-authorization denial plus internal appeals review workflow.

The modeled workflow exists only as test data. It is not a real utilization-management workflow, clinical workflow, claims workflow, payer workflow, provider workflow, patient record, appeal record, or source-system integration.

## Synthetic classes

The corpus includes three synthetic classes.

### Class A — Bounded preservation

Class A records represent bounded structural preservation.

Expected result:

```text
BOUNDARY_PRESERVED
```

Class A does not mean the denial was medically correct, legally sufficient, compliant, complete, fair, clinically appropriate, or authorized for live ingestion.

### Class B — Indeterminate unresolved pointer

Class B records represent a bounded packet with an unresolved synthetic pointer.

Expected result:

```text
POINTER_UNRESOLVED
```

Class B does not mean the underlying workflow is invalid or valid. It means the synthetic packet intentionally includes unresolved pointer state.

### Class C — Invalid boundary expansion

Class C records represent attempted downstream expansion of a bounded structural record into claims Fork does not make.

Expected result:

```text
EXPANSION_DETECTED
```

Class C demonstrates the overclaim pattern the controlled-pilot stack is designed to surface.

## Non-claims

This corpus does not claim:

- medical correctness;
- legal sufficiency;
- regulatory compliance;
- HIPAA compliance;
- clinical appropriateness;
- utilization-management sufficiency;
- source truth;
- source completeness;
- production readiness;
- live-ingestion authorization;
- real-world prior-authorization fidelity;
- real institutional workflow fidelity.

## Boundary

This corpus may be used to demonstrate packet generation, receipt binding, dry-run review, orientation acknowledgment, and structural verification paths.

It must not be used as real institutional data, real medical data, real payer data, real provider data, real patient data, real member data, or evidence that any live workflow is authorized.


## v0.1.1 Structural Outcome Hardening Note

This corpus includes the machine-readable non-claim `does_not_claim_statutory_review_process`.

This corpus does not represent, simulate, validate, or recommend any statutory prior-authorization, adverse-benefit-determination, utilization-management, or internal-appeals process.

Fork outcome labels in this corpus are structural evidence-boundary labels only:

- `BOUNDARY_PRESERVED` means the bounded structural evidence boundary was preserved.
- `POINTER_UNRESOLVED` means an evidence pointer remains unresolved and must not be collapsed into preservation.
- `EXPANSION_DETECTED` means a downstream record attempted to expand beyond the bounded evidence claim.

These labels do not indicate claim approval, denial, clinical sufficiency, utilization-management sufficiency, legal sufficiency, HIPAA compliance, operational authorization, or production readiness.
