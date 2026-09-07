# PROOF-005 CAD v0.2.3 — F3-only type-strictness correction successor

## Status

`CORRECTION_SUCCESSOR_CANDIDATE_NOT_ADMITTED`

This directory defines a narrowly bounded additive successor to frozen PROOF-005 CAD v0.2.2 exact head:

`9e3cdd2fb6d67f9abd6233ce673341bd817d6338`

The governed construction basis is:

`preservation/clean-continuance-v0.1@0c60bbdd2b7c50e1758968464485fac0dfbf008d`

The completed executable exterior return for v0.2.2 was preserved through PR #131 with reviewer disposition:

`EXTERIOR_RECOMPUTATION_CONFORMING_WITH_QUALIFICATIONS`

## Bounded residual addressed

This successor addresses only preserved finding **F3**:

`OBSERVED_NON_ESCALATING_JSON_TYPE_STRICTNESS_GAP`

The v0.2.2 exterior reviewer demonstrated that Python equality permits JSON values with different literal types to compare equal after parsing, including:

- `provider_calls: false` where the governed value is integer `0`;
- `admission: 0` where the governed value is boolean `false`.

The observed substitutions did not establish an escalating authority, admission, readiness, proof, execution, or model-standing path. They did establish that value-only Python equality is not sufficient to prove exact JSON representation/type conformance on the governed control-effect surface.

## v0.2.3 correction

`tools/check_fork_cad_candidate_v0_2_3.py` runs the complete v0.2.2 candidate validation first and then adds one invariant:

> Each of the thirteen governed `CONTROL_EFFECTS_v0_2.json` fields must match both the exact expected parsed JSON type and the exact expected value.

Mechanically, the new boundary requires the equivalent of:

```python
if type(actual) is not type(expected):
    reject
if actual != expected:
    reject
```

The exact-type comparison deliberately avoids Python's `bool`/`int` equality collapse.

The thirteen governed fields are unchanged from v0.2.2. `record_id` remains schema-declared and informational; it is explicitly outside the F3 governed-value set.

## Focused regression surface

The v0.2.3 suite requires:

- the repository candidate to pass;
- the governed field inventory to remain exactly thirteen fields excluding `record_id`;
- reproduction that frozen v0.2.2 accepts `provider_calls: false` for integer `0`;
- reproduction that frozen v0.2.2 accepts integer `0` for each governed boolean `false` field;
- v0.2.3 rejection of those same substitutions;
- rejection of Python-equal `0.0` substitutions on the relevant integer/boolean fields;
- canonical integer/boolean types to pass;
- genuinely escalated values to remain rejected;
- `record_id` to remain informational;
- the complete v0.2.2 predecessor candidate to remain conforming before the F3 layer is applied.

All v0.2, v0.2.1, and v0.2.2 checker/test surfaces are carried forward unchanged.

## Explicit exclusions

This successor does **not** change or resolve:

- F2 / Unicode invisible-character `source_refs` semantics;
- source existence, provenance, chronology, or evidentiary sufficiency;
- source-grounding completeness;
- PROOF-005 admission or proof-packaging admission;
- model standing;
- provider-call or Pair-001 authorization;
- pilot or production readiness;
- compliance or legal sufficiency;
- branch-protection settings;
- a generalized Correction-and-Successor Protocol.

The U+200B/F2 behavior is intentionally preserved as a separate hardening/inadequacy question rather than folded into this correction.

## Standing ceiling

A green v0.2.3 candidate establishes at most:

`CORRECTION_SUCCESSOR_CANDIDATE_READY_FOR_EXACT_HEAD_REVIEW`

It does not establish exterior recomputation, admission, independent validation, or merge authority.

## Required next sequence

1. exact-head CI;
2. bounded construction-assisted exact-head review;
3. freeze the exact v0.2.3 coordinate;
4. delta-bounded exterior recomputation reproducing F3 on v0.2.2 and demonstrating closure on v0.2.3;
5. preserve that exterior return append-only;
6. separately determine merge/admission disposition.

No step inherits authorization or standing from another.
