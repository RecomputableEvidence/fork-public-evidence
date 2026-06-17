# Required Source Non-Claims v0.1

## Status

Candidate required non-claim bundle for Fork and RGV verification results.

This document defines the mandatory source non-claim bundle used to prevent silent inheritance of source truth, factual confirmation, wholeness, completeness, admissibility, or lawfulness from Fork structural verification.

## Doctrine

Non-claims are inference constraints, not disclaimers.

Fork does not merely preserve what was claimed. It preserves the limits on what may be inferred from the claim.

A Fork/RGV PASS is valid only inside the inference boundary carried by its required non-claims.

## Required source non-claim bundle

The following non-claim identifiers are mandatory whenever a Fork/RGV result, packet, graph bundle, receipt, or downstream consumption record references source material, upstream records, external attestations, human statements, model outputs, system logs, or referenced evidence.

- `SOURCE_TRUTH_NOT_CLAIMED`
- `FACTUAL_BASIS_NOT_CONFIRMED`
- `WHOLENESS_NOT_ASSERTED`
- `COMPLETENESS_NOT_STATED`
- `ADMISSIBILITY_NOT_INFERRED`
- `LAWFULNESS_NOT_IMPLIED`

## Canonical statements

### SOURCE_TRUTH_NOT_CLAIMED

Fork does not assert that any source artifact, upstream record, external attestation, human statement, model output, system log, or referenced evidence is factually true.

### FACTUAL_BASIS_NOT_CONFIRMED

Fork does not independently confirm the factual basis underlying any source claim, upstream record, external attestation, human statement, model output, system log, or referenced evidence.

### WHOLENESS_NOT_ASSERTED

Fork does not assert that the preserved record represents the whole factual, operational, legal, or institutional context.

### COMPLETENESS_NOT_STATED

Fork does not state that all relevant evidence, records, sources, reviews, approvals, risks, omissions, or dependencies have been captured.

### ADMISSIBILITY_NOT_INFERRED

Fork structural verification does not imply legal admissibility, self-authentication, business-records status, or satisfaction of evidentiary rules.

### LAWFULNESS_NOT_IMPLIED

Fork does not imply that any source action, workflow, output, decision, deployment, review, approval, reliance, or downstream use was lawful.

## Enforcement semantics

A Fork/RGV result may pass required-source-non-claim verification only when the mandatory non-claim bundle is present and intact.

The following are verification defects:

- a required source non-claim is missing;
- a required source non-claim identifier is duplicated;
- a required source non-claim statement is empty;
- a record asserts source truth while carrying the required non-claim bundle;
- a record asserts factual basis confirmation while carrying the required non-claim bundle;
- a record asserts wholeness while carrying the required non-claim bundle;
- a record asserts completeness while carrying the required non-claim bundle;
- a record infers admissibility while carrying the required non-claim bundle;
- a record implies lawfulness while carrying the required non-claim bundle.

If a downstream system wants to expand meaning beyond the required source non-claim bundle, it must introduce a new claim node with explicit authority, evidence basis, and boundary declarations. The new claim does not inherit Fork structural authority.

## Non-claim inheritance rule

Required source non-claims must travel with downstream consumption unless a downstream record explicitly rejects the source artifact or creates a new bounded claim with independent authority and evidence.

Dropping, narrowing, contradicting, or ignoring required source non-claims is an unauthorized inference expansion.

## Checker scope

`tools/check_required_source_non_claims_v0_1.py` validates deterministic bundle presence and basic contradiction rules only.

It does not verify source truth, factual basis, wholeness, completeness, admissibility, lawfulness, legal sufficiency, compliance, safety, correctness, institutional authority, or runtime authorization.

## Locked line

Fork verifies boundary fidelity, not SOURCE_TRUTH.