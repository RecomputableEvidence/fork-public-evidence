# CBC / CCE v0.2.1 Precision Patch Notes

## Status

Release note: `CBC_CCE_v0_2_1_PRECISION_PATCH_NOTES`

Expected tags:

- `claim-boundary-contract-v0.2.1`
- `claim-consumption-events-v0.2.1`
- `cbc-cce-v0.2.1-precision-patch`

## Summary

This patch responds to independent review notes on CBC v0.2 and CCE v0.2.

The v0.2 architecture remains sound. v0.2.1 tightens the perimeter against semantic leakage, edge/node confusion, benchmark-pass overreading, and unresolved expansion pointers.

## Primary corrections

1. CCE expansion examples are renamed as edges, not resulting claim states.
2. Benchmark examples are framed as benchmark execution records, not governance approvals.
3. Runtime blocked-tool-call examples explicitly reject malicious-intent, legal, compliance, and policy-correctness inheritance.
4. Policy association is explicitly non-certifying.
5. CCE expansion requires a new claim-boundary pointer and records whether that pointer is locally resolved, external, unresolved, or not applicable.
6. Locally resolved expansion pointers are checked against local CBC artifacts.
7. Source non-claim IDs are matched against local CBC non-claims when the source CBC is resolvable.
8. Partial verification scopes remain available as bounded partial states, but full `PASS` remains restricted to `RECORD_INTEGRITY_AND_BOUNDARY_STRUCTURE_ONLY`.

## Canonical doctrine

A CBC defines a source-side claim boundary.

A CCE records a downstream consumption edge.

A CCE never holds an expanded claim. It records the vector of expansion and terminates at the explicit reference pointer of the newly generated CBC.

Pointer resolution is itself a verification condition, not an assumed fact.

## Validation

Expected local validation:

```powershell
python -m pytest tests/test_claim_boundary_contract_v0_2_1.py tests/test_claim_consumption_events_v0_2_1.py
```

Expected result:

```text
48 passed
```
