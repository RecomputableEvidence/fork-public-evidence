# UEM v0.1 Epoch 010 CRII — Admission Merge Receipt

**Date:** 2026-09-17  
**Admission PR:** `#149`  
**Admission head:** `442e047956039fde610788ec6dc28feb70233aa5`  
**Merge commit:** `61ce462e131c3c2687abd1d7744cd9ffaf238552`  
**Repository path:** [`admissions/UEM-v0.1/EPOCH-010-CRII`](../../admissions/UEM-v0.1/EPOCH-010-CRII/)  
**Disposition:** `REPOSITORY_ADMITTED_WITH_BOUNDED_CRII_EPOCH_010_PASS`

## Merge gate

The admission branch changed only the bounded UEM Epoch 010 admission surface and one existing CI workflow step. Before merge, the following pull-request workflows completed successfully:

- `Fork Admission Gate` — including the UEM Epoch 010 bounded admission verifier;
- `Fork Evidence CI` — including governed-text, invariant, definition-boundary, provenance-tier, and meta-evidence checks;
- `Fork Proof-Surface Integration` — including Ubuntu, Windows, PowerShell, CSH instrumentation, and full regression surfaces.

The merge was performed only after all three workflows reported success.

## Admitted standing

```text
UEM_CRII_1_0_EPOCH_010
research_state                  = CLOSED_FOR_EPOCH_010_SCOPE
disposition                     = BOUNDED_CANONICAL_RESULT_IDENTITY_INTERCHANGE_PASS
verifier_receipt_replay         = PASS_REPRODUCED_BYTE_FOR_BYTE
fixture_population              = 16
validation_distribution         = 4_ACCEPT__12_REJECT
receipt_status                  = PASS
```

The reproduced receipt binds the exact admitted executor-result bytes, the closed CRII rule registry, sealed expectations, verifier source/tests, and pre-exposure freeze manifest. The independent closeout assessment reports that replaying the frozen verifier against the exact executor results reproduced the published PASS receipt byte-for-byte.

## Material boundary

```text
TERMINAL_NATIVE_RECORDS_ADMITTED
!= ORIGINAL_16_FIXTURE_EXECUTOR_HANDOFF_BYTE_ADMITTED
!= COMPLETE_CLOSEOUT_ZIP_BYTE_ADMITTED
!= FROZEN_VERIFIER_BUNDLE_BYTE_ADMITTED
!= INDEPENDENT_REPRODUCTION_BINDING_ZIP_BYTE_ADMITTED
```

Those larger predecessor and support objects remain content-addressed by their recorded SHA-256 identities rather than being bulk-admitted through this event.

## Evidentiary boundary

```text
BOUNDED_CRII_EPOCH_010_PASS
!= UNIVERSAL_UEM_CORRECTNESS

CANONICAL_RESULT_IDENTITY_INTERCHANGE_PASS
!= SEMANTIC_CORRECTNESS_OF_UNDERLYING_CLAIMS

VERIFIER_RECEIPT_REPLAY_PASS
!= INDEPENDENT_EXECUTOR_FROM_FIXTURES_REPRODUCTION

MANIFEST_BOUND_PRE_EXPOSURE_RECORD
!= TRUSTED_TIMESTAMP_PROOF_OF_PRE_EXPOSURE_CHRONOLOGY

EPOCH_010_PASS
!= INDEPENDENT_SURFACE_GENERALIZATION
!= EPOCH_011_GENERALIZATION

REPOSITORY_ADMITTED
!= GOVERNANCE_ADOPTED
!= PRODUCTION_AUTHORIZED
```

The closeout archive does not contain the original executor handoff / 16-fixture corpus needed to independently rerun the executor from the original input population. The pre-exposure verifier freeze is cryptographically bound by its manifest, but the chronology is not independently established here by a trusted timestamp or external log.

## Observed contract edge

The frozen verifier contract permits additional rule IDs when they belong to the closed registry. The actual Epoch 010 executor results do not exercise an `ACCEPT` row with additional registered violations: all four observed `ACCEPT` rows have empty `violated_rule_ids`. A stronger invariant of `ACCEPT => zero violations` would require separately scoped successor specification/testing if desired.

## Closure

There is no remaining evidence gate inside the exact bounded Epoch 010 CRII result admitted here. Fresh executor-from-fixture reproduction, stronger chronology proof, stricter ACCEPT semantics, independent-surface generalization, or later UEM epochs are separately identified successor work and must not mutate this frozen admission.

This receipt records the completed repository admission event. It does not retroactively alter the pre-merge admission candidate or any predecessor UEM epoch.
