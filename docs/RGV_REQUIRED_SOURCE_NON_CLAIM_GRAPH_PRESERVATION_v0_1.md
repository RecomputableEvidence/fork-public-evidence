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

## Structured expansion basis requirements

For prohibited semantic expansion, a new claim node must carry structured non-Fork authority and evidence references.

A bare string, placeholder, local dummy value, empty object, or non-Fork-looking label is not sufficient to establish a structurally valid external evidence basis.

Fork does not validate the substantive adequacy of external evidence. It only requires that the downstream expansion declare external authority and evidence in a structured, inspectable form.

Structural compliance of an expansion node does not mean Fork endorses the quality, correctness, admissibility, lawfulness, completeness, or sufficiency of the downstream claim.
## Expansion basis restriction

Fork/RGV PASS may be referenced as structural evidence only.

It cannot be the sole authority basis or sole evidence basis for truth, factual-basis confirmation, wholeness, completeness, admissibility, lawfulness, compliance, safety, correctness, institutional approval, or runtime authorization.

If a new claim node expands beyond Fork/RGV PASS semantics, its authority basis and evidence basis must not be reducible to the Fork/RGV PASS result itself.

A new claim node may reference an RGV PASS as one structural input, but it must also provide external non-Fork authority or evidence for the expanded claim.
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

## Metadata traversal bounds

Structured metadata containers are recursively inspected within bounded traversal limits.

If a structured metadata container exceeds the permitted traversal depth or value count, the checker fails closed rather than silently accepting the graph.

This is a structural traversal-safety rule. It is not natural-language understanding and does not evaluate arbitrary human prose.
## Structured metadata alias handling

The checker treats known machine-readable metadata containers as part of the graph-composition surface.

Structured fields such as `metadata`, `extensions`, `custom_downstream_extensions`, `consumption_context`, `legal_assessment`, `factual_status`, `clearance_level`, and `assumed_status` may not be used to contradict the required source non-claim boundary.

Localized display labels may be used for human presentation, but they do not replace, satisfy, weaken, or rename the six canonical v0.1 required source non-claim identifiers.

This checker does not perform NLP over arbitrary human prose. It performs bounded structural alias detection over known machine-readable fields and enum-like values.

## Authority chain restriction

A new claim node may not hide Fork/RGV PASS behind an intermediate authority node.

If the authority basis for a prohibited semantic expansion roots back to Fork/RGV PASS, the expansion fails graph-preservation validation.

Fork/RGV PASS may be a structural reference. It may not become the root authority for truth, factual-basis confirmation, wholeness, completeness, admissibility, lawfulness, compliance, safety, correctness, institutional approval, or runtime authorization.

## INDETERMINATE negative-signal restriction

`INDETERMINATE` carries no positive or negative content valence.

It may not be used as PASS, provisional PASS, source-truth support, factual support, or as a negative content signal such as unreliability, falsity, suspiciousness, weak evidence, or incomplete truth verification.
## INDETERMINATE and FAIL downstream support

`INDETERMINATE` may not be used as support for source truth, factual-basis confirmation, wholeness, completeness, admissibility, lawfulness, compliance, safety, correctness, institutional approval, or runtime authorization.

`FAIL` may not be interpreted as source falsity, unlawfulness, inadmissibility, incompleteness, or factual unsupportedness.
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