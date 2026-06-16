# CBC v0.2 / CCE v0.2 Release Notes

## Status

Release note: `CBC_CCE_v0_2_RELEASE_NOTES`

Related tags:

- `claim-boundary-contract-v0.2`
- `claim-consumption-events-v0.2`

Related commits:

- `3f9a97c` — Add claim boundary contract v0.2 hardening artifacts
- `1c9efa1` — Add claim consumption events v0.2 hardening artifacts

## Summary

This release hardens Fork’s claim-boundary and downstream claim-consumption posture.

Claim Boundary Contract v0.2 records what an upstream artifact claims, what it does not claim, what verification scope applies, and which upstream claims are received, relied on, or rejected.

Claim Consumption Events v0.2 records how downstream systems, reviewers, policy layers, or evidence layers consume those bounded claims without silently inheriting claims the upstream artifact did not make.

Together, CBC v0.2 and CCE v0.2 strengthen Fork’s evidence-boundary architecture by separating source-side claim definition from downstream reliance behavior.

## Core doctrine

No silent claim inheritance.

A downstream workflow may consume an upstream artifact, but it should not automatically convert that artifact into a stronger claim.

Examples:

- A benchmark pass does not become deployment readiness.
- A blocked runtime event does not become legal sufficiency.
- A human review record does not become correctness.
- A policy-associated artifact does not become compliance.
- A high-assurance source does not become self-certifying truth.

CBC v0.2 defines the upstream claim boundary.

CCE v0.2 records how that claim boundary is preserved, narrowed, rejected, or explicitly expanded downstream.

## Artifact set

### Claim Boundary Contract v0.2

Added:

- `docs/CLAIM_BOUNDARY_CONTRACT_v0_2.md`
- `schemas/claim_boundary_contract_v0_2.schema.json`
- `examples/claim_boundary_contract_v0_2/runtime_blocked_tool_call.json`
- `examples/claim_boundary_contract_v0_2/eval_benchmark_pass.json`
- `tests/test_claim_boundary_contract_v0_2.py`

### Claim Consumption Events v0.2

Added:

- `docs/CLAIM_CONSUMPTION_EVENTS_v0_2.md`
- `schemas/claim_consumption_events_v0_2.schema.json`
- `examples/claim_consumption_events_v0_2/preserved_runtime_blocked_tool_call.json`
- `examples/claim_consumption_events_v0_2/expanded_eval_benchmark_pass.json`
- `tests/test_claim_consumption_events_v0_2.py`

## CBC v0.2 hardening

CBC v0.2 adds hardened source-side claim-boundary structure, including:

- explicit claim-boundary versioning;
- structured upstream claim receipt;
- relational handling of received, relied-on, and rejected upstream claims;
- stronger non-claim preservation;
- clearer verification-scope boundaries;
- examples for runtime blocked-tool-call records and evaluation benchmark-pass records;
- tests that exercise schema validity and claim-boundary behavior.

CBC v0.2 remains bounded to claim-boundary structure. It does not assert source truth, legal sufficiency, compliance sufficiency, deployment readiness, or runtime enforcement.

## CCE v0.2 hardening

CCE v0.2 adds downstream consumption structure, including:

- explicit consumed claim IDs;
- relied and rejected claim sets;
- preservation of upstream non-claims;
- boundary effects: `PRESERVED`, `NARROWED`, and `EXPANDED`;
- expansion gating with reason, authorizing party, new claim reference, and additional evidence references;
- source assurance profiles with limitations;
- unresolved unknown tracking;
- required CCE-level non-claims;
- relational tests beyond JSON Schema shape validation.

CCE v0.2 remains bounded to downstream reliance records. It does not enforce runtime behavior, certify compliance, approve deployment, assert source completeness, or assert source truth.

## Boundary effects

CCE v0.2 recognizes three downstream effects.

### `PRESERVED`

The downstream consumer relies on the upstream claim without adding, weakening, or converting its scope.

### `NARROWED`

The downstream consumer relies on a more limited version of the upstream claim and records the narrowing reason.

### `EXPANDED`

The downstream consumer adds a new or stronger downstream claim and records:

- expansion reason;
- authorizing party;
- new claim reference;
- additional evidence references;
- downstream output claim IDs.

Expansion is explicit rather than inherited.

## Source assurance posture

CCE v0.2 may record source assurance profiles such as:

- software workflow log;
- policy-engine output;
- human review record;
- hardware-anchored receipt;
- vendor artifact;
- evaluation result.

Source assurance is treated as bounded input metadata. It may contribute to the evidentiary posture of a record, but it does not become self-certifying truth inside Fork’s evidence boundary.

The test suite deliberately rejects absolute assurance language such as `UNFALSIFIABLE_PHYSICAL_TRUTH`.

## Validation posture

The v0.2 validation posture combines JSON Schema checks with relational tests.

The schemas validate object shape.[web:8][web:16]

The tests add checks for relationship integrity, including:

- relied claims must refer to consumed claims;
- rejected claims must refer to consumed claims;
- a claim cannot be both relied on and rejected;
- duplicate consumed claim IDs are rejected;
- non-claims attached to relied claims must remain preserved;
- `EXPANDED` boundary effects require explicit expansion support;
- `NARROWED` boundary effects require a narrowing reason;
- `PRESERVED` boundary effects cannot smuggle new downstream claims;
- reliance on `FAIL`, `NOT_CHECKED`, or `INDETERMINATE` claims requires unresolved unknowns;
- required CCE non-claims must remain present.

## Test result

Validated locally with:

```powershell
python -m pytest tests/test_claim_boundary_contract_v0_2.py tests/test_claim_consumption_events_v0_2.py
```

Expected result:

- `42 passed`

## Relationship to Fork

Fork remains out-of-band evidence-boundary infrastructure.

This release does not turn Fork into a runtime controller, legal authority, compliance certifier, policy engine, or source-of-truth system.

The release strengthens Fork’s ability to preserve how claims and non-claims move across AI-assisted workflow handoffs, so later reviewers can inspect what was claimed, what was not claimed, what was relied on, what was rejected, what was expanded, what remains unknown, and what can still be structurally verified.

## Release significance

CBC v0.2 and CCE v0.2 together form a clearer two-part boundary model:

- CBC v0.2 defines the source-side claim boundary.
- CCE v0.2 records downstream claim consumption.

That pairing helps prevent transitive overclaiming across AI-assisted workflows.

A record can now preserve not only that an artifact existed or structurally verified, but also how its claims were later consumed without silently converting bounded evidence into broader conclusions.
