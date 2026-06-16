# Claim Consumption Events v0.2

## Status

Version: `CCE_v0_2`

Claim Consumption Events record how downstream systems, reviewers, policy layers, or evidence layers consume upstream claim-boundary artifacts.

CCE v0.2 is downstream of Claim Boundary Contract v0.2. CBC defines what a source artifact claims and does not claim. CCE records how that bounded claim is later relied on, rejected, narrowed, or explicitly expanded.

## Core rule

No silent claim inheritance.

A downstream consumer may rely on an upstream claim, but it must preserve the relevant non-claims and verification scope. If the downstream consumer adds a stronger or different claim, the CCE record must identify that expansion, the reason for it, the new claim reference, the authorizing party, and the additional evidence references used for the expansion.

## Boundary effects

CCE v0.2 recognizes three boundary effects:

- `PRESERVED` — the downstream consumer relies on the upstream claim without adding, weakening, or converting its scope.
- `NARROWED` — the downstream consumer relies on a more limited version of the upstream claim and records the narrowing reason.
- `EXPANDED` — the downstream consumer adds a new or stronger downstream claim and records the expansion reason, authorizing party, new claim reference, and additional evidence.

## Required non-claims

Every CCE v0.2 record includes non-claims stating that the record does not assert:

- source truth;
- legal, contractual, regulatory, or compliance sufficiency;
- runtime enforcement or authorization;
- source completeness.

## Source assurance

CCE v0.2 may record the assurance profile of an upstream source, including software logs, policy engine outputs, human review records, hardware-anchored receipts, vendor artifacts, or evaluation results.

Source assurance is input metadata. It is not self-certifying truth.

A higher-assurance source may contribute stronger evidence of a bounded condition, but the CCE record still preserves the claim, verification method, assumptions, and non-claims attached to that source.

## Relationship to Fork

Fork remains an out-of-band evidence-boundary layer.

CCE v0.2 does not enforce runtime behavior, approve deployment, certify compliance, or assert source truth. It preserves how claims are consumed across handoffs so later reviewers can inspect reliance, rejection, narrowing, expansion, unresolved unknowns, and evidence references without collapsing those roles into one layer.

## v0.2 hardening

CCE v0.2 adds:

- explicit consumed claim IDs;
- relied and rejected claim sets;
- non-claim preservation checks;
- expansion gating;
- source assurance profiles with limitations;
- unresolved unknown tracking;
- required CCE non-claims;
- relational validation tests beyond JSON Schema shape validation.

## Validation posture

The JSON Schema validates object structure.

The test suite adds relational checks:

- relied and rejected claims must refer to consumed claims;
- relied and rejected sets must not overlap;
- duplicate consumed claim IDs are rejected;
- non-claims attached to relied claims must be preserved;
- expansions require explicit reason, new claim reference, authorizing party, and additional evidence;
- reliance on `FAIL`, `NOT_CHECKED`, or `INDETERMINATE` claims requires unresolved unknowns;
- CCE required non-claims must remain present.
