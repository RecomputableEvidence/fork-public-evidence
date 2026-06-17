# RGV Required Source Non-Claim Result Binding v0.1

## Status

Candidate result-semantics binding for RGV verification outputs.

This document binds the required source non-claim bundle to RGV `PASS` semantics without reopening the RGV v0.4 evidentiary-weight profile contract.

## Core doctrine

Non-claims are inference constraints, not disclaimers.

Fork verifies boundary fidelity, not SOURCE_TRUTH.

A Fork/RGV `PASS` is valid only inside the inference boundary carried by its required source non-claims.

## Relationship to prior artifacts

This binding depends on the required source non-claim bundle defined in:

`docs/REQUIRED_SOURCE_NON_CLAIMS_v0_1.md`

This binding does not modify:

- `schemas/rgv_evidentiary_weight_profile_v0_4.schema.json`
- `docs/RGV_v0_4_EVIDENTIARY_WEIGHT_HARDENING_PROFILE.md`
- the v0.4 evidentiary-weight profile contract

It is a separate result-semantics layer.

## Required source non-claims on RGV PASS

Every RGV `PASS` result that references source material, upstream records, external attestations, human statements, model outputs, system logs, or referenced evidence must carry the following required non-claim identifiers:

- `SOURCE_TRUTH_NOT_CLAIMED`
- `FACTUAL_BASIS_NOT_CONFIRMED`
- `WHOLENESS_NOT_ASSERTED`
- `COMPLETENESS_NOT_STATED`
- `ADMISSIBILITY_NOT_INFERRED`
- `LAWFULNESS_NOT_IMPLIED`

These may be carried in `result_non_claims` or in a dedicated `required_source_non_claims` field. In either case, they must be present and intact for a `PASS` result to remain inside its valid inference boundary.

## Invalid result semantics

An RGV `PASS` result is invalid if it:

- omits any required source non-claim;
- duplicates a required source non-claim identifier;
- carries an empty statement for a required source non-claim;
- asserts source truth;
- confirms factual basis;
- asserts wholeness;
- states completeness;
- infers admissibility;
- implies lawfulness;
- declares a erification_scope value that is or contains a source-truth reference.

## Expansion rule

If a downstream system needs to assert truth, factual basis, wholeness, completeness, admissibility, or lawfulness, it must introduce a new claim node with its own explicit authority basis, evidence basis, and non-claims.

That new claim node does not inherit RGV structural authority.

## INDETERMINATE posture

`INDETERMINATE` results are not RGV `PASS` results and are not required by this binding to carry the required source non-claim bundle.

Downstream consumers must not treat `INDETERMINATE` as an approximate, pending, partial, or implied `PASS`.

An `INDETERMINATE` result does not authorize source-truth inference, factual-basis confirmation, wholeness assertion, completeness statement, admissibility inference, lawfulness implication, runtime authorization, compliance reliance, or institutional approval.

## Free-text limitation

This binding checker validates structural fields and known prohibited assertion fields.

It does not scan arbitrary free-text fields such as `summary`, `notes`, `description`, or human-authored prose for implied truth assertions.

Implementers are responsible for ensuring free-text content in result records remains consistent with the required source non-claims.
## Checker scope

`tools/check_rgv_result_required_source_non_claim_binding_v0_1.py` validates deterministic RGV result-semantics constraints only.

It does not verify source truth, factual basis, wholeness, completeness, admissibility, lawfulness, legal sufficiency, compliance, safety, correctness, institutional authority, runtime authorization, or source completeness.

## Locked line

A structural PASS is not a source-truth assertion.