# Governed Handoff Cadence Harness v0.1

## Standing

`DETERMINISTIC_SIMULATION_CANDIDATE_NOT_ADMITTED`

This surface models a bounded enterprise cadence in which upstream governance, Fork as an out-of-band evidence sidecar, and downstream governance exchange claim-bearing records without transferring authority, inheriting standing, importing endorsement, or promoting referenced evidence.

It is a successor composition layer above the existing Cross-System Claim Handoff work. It does not replace CSH, modify Pair-001, authorize provider calls, or represent a production integration.

## Why this surface exists

Existing CSH surfaces classify individual receiver outputs, evidence-chain integrity, pair comparability, reviewer boundaries, authority-inheritance flags, non-claim loss, reference promotion, and representation degradation.

The missing enterprise-facing proof surface is a repeated, role-separated cadence:

1. freeze the route, roles, policy, canonical claim bundle, and non-claims;
2. upstream governance emits under its own local authority;
3. Fork records ingress when available and preserves an observation gap when unavailable;
4. downstream governance ingests without importing upstream authority or standing;
5. downstream governance exercises only its preexisting local authority;
6. Fork records egress without approving the downstream result;
7. upstream reconciles without endorsement inheritance;
8. the harness closes the cadence without conferring authority or admission.

## Architectural correction to the initial idea

The harness does **not** require every stage to have no authority effect. Upstream and downstream governance models may exercise authority inside their own preexisting domains. The enforced invariant is narrower and stronger:

> No authority crosses the exchange boundary, and no participant acquires authority from another participant, Fork, an acknowledgment, a receipt, or an evidence reference.

This distinction prevents the harness from accidentally disabling legitimate local governance while still rejecting authority transfer and inheritance.

## Redundancy strategy

The cadence defines the following once:

- canonical claim bundle;
- exchange policy;
- non-claim set.

Every stage carries exact digest references plus an explicit claim delta. Full claim and policy prose is not recopied into each stage. This reduces accidental divergence while retaining safety boundaries at every handoff.

## Implemented proof surfaces

- deterministic canonicalization and digest-bound event lineage;
- fixed eight-stage state machine;
- local-authority versus transferred-authority semantics;
- read-only, out-of-band, fail-open Fork stages;
- explicit permissible narrowing;
- exact unresolved-item preservation;
- semantic-regression checker;
- deterministic fixture builder;
- a digest-bound generated 13-case fixture corpus containing three valid profiles and ten adversarial fixtures;
- unit tests that keep expected outcomes outside fixture bytes;
- claim-to-proof map;
- staged progression gates through exterior recomputation, shadow adapters, bounded pilot, and longitudinal replay.

## Run locally

```bash
python tools/build_ghch_fixtures_v0_1.py --output-root /tmp/ghch-fixtures
python -m unittest tests/test_ghch_cadence_v0_1.py
python tools/check_ghch_cadence_v0_1.py \
  /tmp/ghch-fixtures/valid/clean_round_trip.json
```

Expected clean result:

```text
GHCH_CADENCE_CONFORMS_PRESERVED
```

## Non-claims

This surface does not establish enterprise interoperability, production readiness, compliance, legal sufficiency, model correctness, governance-model equivalence, authority transfer, provider execution, Pair-001 execution, admission, or a change to `main`.

## Review order

1. Review the protocol and invariant sections in this README together with `GHCH-CONTROL-PLANE.json`.
2. Inspect `ghch_common_v0_1.py` for canonicalization and builder separation.
3. Inspect the checker for semantic enforcement independent of fixture expectations.
4. Run the fixture builder and compare bytes.
5. Run the unit tests.
6. Adversarially mutate a valid fixture, recompute its internal hashes, and confirm semantic rejection.
7. Review the `next_stage_gates` section in `GHCH-CONTROL-PLANE.json` before proposing any live adapter or enterprise workflow.


---

# Governed Handoff Cadence Protocol v0.1

## 1. Objective

The cadence tests whether a claim-bearing exchange can traverse upstream governance, Fork, and downstream governance while preserving provenance, scope, non-claims, unresolved items, and lineage without transferring authority or inheriting standing.

The protocol is deterministic and simulated. No network, model, provider, production system, or institutional decision is invoked.

## 2. Roles

| Participant | Role | Authority domain |
|---|---|---|
| `HARNESS-001` | Simulation harness | None |
| `UPSTREAM-001` | Upstream governance | Upstream local only |
| `FORK-001` | Fork evidence sidecar | None |
| `DOWNSTREAM-001` | Downstream governance | Downstream local only |

Fork records declared and observed evidence boundaries. It does not approve, authorize, rank, or execute either governance model.

## 3. Canonical objects

Three objects are defined once and referenced by digest at every stage:

1. **Claim bundle** — claims, standing, scope, and evidence references.
2. **Exchange policy** — prohibited authority/standing/endorsement inheritance and Fork mode.
3. **Non-claim set** — required exclusions and non-effects.

A stage may carry a `claim_delta`, but it may not silently reproduce or rewrite the canonical objects.

## 4. Fixed cadence

| Order | Stage | Actor | Required meaning |
|---:|---|---|---|
| 1 | `PREREGISTER` | Harness | Freeze route, roles, policy, and stage order |
| 2 | `UPSTREAM_EMIT` | Upstream | Release under upstream-local authority only |
| 3 | `FORK_CAPTURE_INGRESS` | Fork | Record ingress or preserve unavailability |
| 4 | `DOWNSTREAM_INGEST` | Downstream | Receive without importing authority or standing |
| 5 | `DOWNSTREAM_LOCAL_DISPOSITION` | Downstream | Exercise downstream-local authority only |
| 6 | `FORK_CAPTURE_EGRESS` | Fork | Record egress without approval |
| 7 | `UPSTREAM_RECONCILE` | Upstream | Acknowledge or dispute without endorsement inheritance |
| 8 | `CADENCE_CLOSE` | Harness | Close simulation without admission or authority |

Each event binds the exact predecessor event ID and canonical event digest.

## 5. Local authority rule

`LOCAL_ONLY` is permitted only when:

- the actor is the upstream or downstream governance participant;
- the authority source is `PREEXISTING_LOCAL_GOVERNANCE`;
- no transfer or inheritance flag is set;
- the action remains inside that participant's declared authority domain.

A handoff cannot create, delegate, sublicense, imply, or inherit authority.

## 6. Standing rule

Downstream governance may perform `LOCAL_REASSESSMENT`. It may not inherit upstream standing.

Permissible narrowing requires:

- stage `DOWNSTREAM_LOCAL_DISPOSITION`;
- operation `NARROW`;
- an existing claim ID;
- a non-empty basis;
- reconciliation relationship `NARROWED`.

Expansion, promotion, equivalence, or silent resolution is rejected.

## 7. Fork fail-open rule

If Fork capture is unavailable:

- both Fork capture stages remain present with status `UNAVAILABLE`;
- downstream stages continue;
- the cadence closes as `COMPLETED_WITH_OBSERVATION_GAPS`;
- both capture gaps remain listed as unresolved;
- no evidence is fabricated and no workflow block is inferred.

## 8. Redundancy and gap rule

Repeated prose is not treated as stronger evidence. The canonical objects remain single-source; stage records contain exact references and deltas.

The checker rejects:

- missing or duplicated stages;
- stale or severed lineage;
- duplicate event IDs;
- non-claim loss;
- authority transfer or inheritance;
- standing or endorsement inheritance;
- evidence-reference promotion;
- unresolved resolution by assumption;
- hidden expansion;
- Fork unavailability converted into workflow blocking;
- route-order regression;
- declared versus observed mismatch.

## 9. Semantic-regression rule

Adversarial fixtures are internally rehashed after mutation wherever possible. Rejection must therefore arise from semantic enforcement, not merely stale checksums.

Fixture expectations live in the test module, not in the fixture records, and the checker never reads an oracle or expected-result file.

## 10. Version and admission boundary

v0.1 is a local deterministic harness candidate. A later version may add shadow adapters, but only after exact-head review and exterior recomputation.

No merge, CI result, or review of this candidate authorizes live execution or admission. Any admission requires a separate append-only act.


---

# Redundancy and Gap Policy v0.1

## Intentional safety repetition

The following concepts must remain inspectable at every stage through digest references:

- claim bundle identity;
- exchange-policy identity;
- non-claim-set identity;
- predecessor event identity.

Their repeated references are intentional control bindings, not redundant prose.

## Prohibited duplication

Stages must not copy the full canonical claim bundle, policy, or non-claim set. Changes are expressed only as explicit deltas.

This prevents:

- version skew between repeated copies;
- accidental omission of a non-claim;
- semantic drift hidden by similar prose;
- a downstream rewrite being mistaken for the upstream record.

## Required gaps

A missing observation must remain a gap. It must not be replaced by:

- a synthetic success receipt;
- an inferred provider result;
- an assumed acknowledgment;
- an inherited standing;
- a default approval;
- a collapsed unresolved state.

## Gap closure

A gap closes only through a successor event with a new artifact and explicit evidence basis. Replaying or restating the earlier record does not close it.

## Duplicate and replay handling

Duplicate event IDs, repeated stages, stale predecessor references, and out-of-order transitions reject the cadence. A later replay must use a new cadence ID and preserve the prior cadence as predecessor evidence.


---

# Exact-head review questions

1. Does the harness distinguish local governance authority from transferred or inherited authority correctly?
2. Can any actor obtain `LOCAL_ONLY` authority from a message, acknowledgment, evidence reference, or Fork capture?
3. Can a mutated fixture recompute all digests and still bypass a semantic invariant?
4. Does the checker ever read fixture expectations or an oracle?
5. Are claim bundle, exchange policy, and non-claim set defined once and referenced consistently?
6. Can non-claim loss be hidden by recomputing the non-claim-set digest?
7. Can a downstream expansion be mislabeled as preservation or narrowing?
8. Does Fork unavailability remain fail-open while preserving negative evidence?
9. Can route reordering, event replay, duplicate IDs, or stale predecessor references survive?
10. Can an acknowledgment be overread as endorsement, approval, or authority?
11. Does any language imply production readiness, compliance, governance equivalence, or provider authorization?
12. Are the next-stage gates strict enough to prevent a deterministic simulation from silently becoming a live enterprise pilot?
