# Recomputability Receipt Binding v0.1

## Purpose

This document defines the v0.7 Phase 3 receipt-binding layer for recomputability gate decisions.

Phase 1 defined recomputability classes.

Phase 2 enforced the strong-gate refusal:

> NON_RECOMPUTABLE evidence cannot satisfy gates requiring STRONG_RECOMPUTATION.

Phase 3 binds that enforcement into explicit receipts.

## Core Invariant

No recomputability gate result may be emitted without exposing the class comparison that produced it.

## Receipt Fields

A recomputability gate receipt records:

- `receipt_type`
- `receipt_version`
- `artifact_recomputability_class`
- `gate_required_class`
- `gate_result`
- `reason_code`
- `claim_boundary`

## Valid Decisions

### STRONG_RECOMPUTATION artifact satisfying STRONG_RECOMPUTATION gate

Result:

- `gate_result`: `PASS`
- `reason_code`: `STRONG_RECOMPUTATION_SATISFIES_STRONG_GATE`

### NON_RECOMPUTABLE artifact satisfying occurrence-level gate

Result:

- `gate_result`: `PASS`
- `reason_code`: `NON_RECOMPUTABLE_SATISFIES_OCCURRENCE_GATE_ONLY`

Claim boundary:

> NON_RECOMPUTABLE evidence may support occurrence-level gates but not gates requiring STRONG_RECOMPUTATION.

### NON_RECOMPUTABLE artifact attempting STRONG_RECOMPUTATION gate

Result:

- `gate_result`: `FAIL`
- `reason_code`: `RECOMPUTABILITY_ESCALATION_DEFECT`

Claim boundary:

> NON_RECOMPUTABLE artifacts must not satisfy gates requiring STRONG_RECOMPUTATION.


## Gate Result Scope

This receipt type uses a narrower gate-level result model than Fork's broader evidence-preservation posture.

For recomputability gate receipts, `gate_result` is limited to `PASS` or `FAIL` because the receipt records the outcome of a specific class comparison: whether the artifact recomputability class satisfies the gate-required class.

`NOT_CHECKED` remains part of Fork's broader preservation vocabulary for evidence properties or verification surfaces that were not evaluated. It is intentionally not a valid `gate_result` for this receipt type, because an emitted recomputability gate receipt represents a class comparison that was actually performed.

## Non-Claims
This receipt-binding layer does not add new recomputability classes.

It does not broaden enforcement.

It does not claim empirical reconstruction improvement.

It does not alter the v0.7 Phase 2 release or tag.

It only serializes the recomputability class comparison that produced a gate result.

## Earned Claim After Phase 3

Fork v0.7 Phase 3 emits receipt-level evidence for recomputability gate decisions, recording the artifact class, gate requirement, result, reason code, and claim boundary for accepted or refused recomputability claims.
