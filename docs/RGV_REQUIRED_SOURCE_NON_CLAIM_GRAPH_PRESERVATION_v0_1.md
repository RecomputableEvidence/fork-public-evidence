# RGV Required Source Non-Claim Graph Preservation v0.1

## Status

Candidate downstream graph-preservation enforcement layer.

This document defines how required source non-claims must be preserved when an RGV `PASS` result is consumed by downstream Claim Consumption Events (CCE) or related graph-composition artifacts.

This layer is separate from:

- the required source non-claim bundle;
- RGV PASS result-semantics binding;
- the RGV v0.4 evidentiary-weight profile contract.

## Core doctrine

Non-claims are inference constraints, not disclaimers.

Fork verifies boundary fidelity, not SOURCE_TRUTH.

A structural PASS is not semantically free-floating. When a downstream artifact consumes a Fork/RGV PASS, the required source non-claim boundary must travel with that consumption.

## Required source non-claim preservation

If a downstream CCE or graph-composition node consumes an RGV `PASS`, it must preserve the canonical v0.1 required source non-claim identifiers:

- `SOURCE_TRUTH_NOT_CLAIMED`
- `FACTUAL_BASIS_NOT_CONFIRMED`
- `WHOLENESS_NOT_ASSERTED`
- `COMPLETENESS_NOT_STATED`
- `ADMISSIBILITY_NOT_INFERRED`
- `LAWFULNESS_NOT_IMPLIED`

Dropping any required source non-claim during downstream consumption is a graph-preservation defect.

## Unauthorized inference expansion

A downstream artifact performs an unauthorized inference expansion if it consumes an RGV `PASS` and treats that PASS as establishing:

- source truth;
- factual-basis confirmation;
- wholeness;
- completeness;
- admissibility;
- lawfulness.

These expansions are prohibited unless represented as a new claim node with its own explicit authority basis, evidence basis, and non-claim boundary.

The new claim does not inherit Fork/RGV structural authority.

## INDETERMINATE posture

An `INDETERMINATE` result is not an approximate PASS.

A downstream CCE must not treat `INDETERMINATE` as `PASS`, pending PASS, partial PASS, provisional PASS, or source-truth support.

## FAIL posture

A downstream CCE must not treat `FAIL` as source falsity.

`FAIL` means the submitted structure is outside valid Fork/RGV verification semantics. It is not a determination that source material is false, unlawful, inadmissible, incomplete, or factually unsupported.

## Checker scope

`tools/check_rgv_required_source_non_claim_graph_preservation_v0_1.py` validates deterministic graph-preservation constraints over supplied local graph artifacts.

It checks whether downstream CCE-like nodes preserve required source non-claims when consuming RGV `PASS` nodes.

It detects common structural inheritance violations, including:

- dropped required source non-claims;
- direct use of RGV PASS as source truth;
- direct use of RGV PASS as factual confirmation;
- direct use of RGV PASS as wholeness or completeness;
- direct use of RGV PASS as admissibility or lawfulness;
- treating INDETERMINATE as PASS.

It does not verify source truth, factual basis, wholeness, completeness, admissibility, lawfulness, legal sufficiency, compliance, safety, correctness, institutional authority, runtime authorization, or source completeness.

It does not scan arbitrary free-text prose for semantic assertions.

## Relationship to v0.4

This graph-preservation layer does not read, require, validate, reinterpret, or mutate v0.4 evidentiary-weight profile fields.

It enforces downstream preservation of required source non-claim boundaries after an RGV result is consumed.

## Locked line

A downstream handoff is not valid if it consumes a structural PASS while dropping the limits that made that PASS bounded.