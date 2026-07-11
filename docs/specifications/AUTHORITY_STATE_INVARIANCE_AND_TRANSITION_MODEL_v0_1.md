# Authority State Invariance and Transition Model v0.1

Status: implemented structural specification module
Classification: recomputable evidence model; not a policy engine, truth engine, compliance oracle, or execution gate
Version: v0.1

## 1. Canonical module claim

> **Fork preserves recorded validity, authority, and reliance as separate, recomputable state histories. It exposes structural misalignment among them without deciding truth, granting permission, blocking execution, assigning answerability, determining compliance, or imposing consequences.**

Narrower authority-accretion claim:

> **Fork makes implicit authority accretion recomputably detectable as a misalignment between observed reliance and the recorded validity, authority, and permitted-use state.**

## 2. Scope

This module defines structural event records and deterministic checks for authority accretion through reuse. It records state transitions and observed reliance. It does not determine whether a claim is true, whether an authority basis is legally sufficient, whether a governance profile is correct, or whether an action should proceed.

Fork is out-of-band, read-only, and fail-open. A checker finding records a structural result. It performs no permit, deny, block, approve, waive, escalate, revoke, or execute action.

## 3. Independent state histories

### 3.1 Recorded validity state

Validity state records evidentiary currency under declared conditions. It does not assert truth.

Canonical states:

- `CURRENT`
- `EXPIRED`
- `SUPERSEDED`
- `UNRESOLVED`

Only a validity-state transition event may change recorded validity.

Canonical transition types:

- `REVALIDATED_CURRENT`
- `MARKED_EXPIRED`
- `MARKED_SUPERSEDED`
- `MARKED_UNRESOLVED`

A revalidation event records that an assessment occurred and the resulting validity state. Revalidation does not grant or expand authority.

### 3.2 Recorded authority state

Authority state records the explicit scope within which use has been authorized, the basis asserted for that authority, and its applicable context. Fork preserves the declaration; it does not determine that the declaration is legally or institutionally sufficient.

Canonical authority statuses:

- `NONE`
- `ACTIVE`
- `EXPIRED`
- `REVOKED`
- `SUPERSEDED`

Only an authority-transition event may change authority.

Canonical transition types:

- `GRANTED`
- `NARROWED`
- `EXPIRED`
- `REVOKED`
- `SUPERSEDED`

### 3.3 Reliance history

A reliance event records how a claim was actually used. It changes neither validity nor authority.

Canonical reliance classes:

- `INFORMATIONAL_REFERENCE`
- `ANALYTICAL_INPUT`
- `DECISION_SUPPORT`
- `EXECUTION_JUSTIFICATION`

These classes describe use. Fork does not define a universal risk hierarchy or decide which authority is sufficient for a class.

## 4. State invariants

Authority invariance:

```text
A(t+1) = A(t)
unless an explicit authority-transition event changes authority.
```

Validity invariance:

```text
V(t+1) = V(t)
unless an explicit validity-state transition event changes validity.
```

No-implication rules:

```text
Reuse does not imply a change in authority.
Reuse does not imply a change in validity.
A validity change does not imply an authority change.
Repeated citation does not constitute independent validation.
Preservation does not create continuing legitimacy.
```

## 5. Normative invariants

- **ASI-001 — Reliance validity invariance.** A reliance event MUST NOT change recorded validity.
- **ASI-002 — Reliance authority invariance.** A reliance event MUST NOT change recorded authority.
- **ASI-003 — Explicit validity transition.** A validity change MUST be represented by a validity-state transition event.
- **ASI-004 — Explicit authority transition.** An authority change MUST be represented by an authority-transition event.
- **ASI-005 — Revalidation separation.** A validity-state transition MUST NOT grant, expand, or silently refresh authority.
- **ASI-006 — Permitted-reliance compatibility.** Observed reliance MUST be evaluated against the claim's recorded permitted-reliance classes and contexts.
- **ASI-007 — Authority-scope compatibility.** Observed reliance MUST be evaluated against the current recorded authority status, classes, and contexts.
- **ASI-008 — Unresolved governance evaluation.** Missing, inaccessible, or out-of-scope governance context MUST remain `NOT_EVALUABLE` and MUST NOT be converted to satisfaction or failure.
- **ASI-009 — Lineage independence.** Repeated derivations or references resolving to the same root MUST NOT be counted as independent validation.
- **ASI-010 — Non-claim survival.** Loss of a material non-claim MUST be surfaced as structural misalignment.
- **ASI-011 — Component inspectability.** Validity, permitted-reliance, authority, governance-profile, non-claim, and lineage results MUST remain individually inspectable.
- **ASI-012 — No enforcement.** Fork MUST record `fork_enforcement_action: NONE` and MUST NOT perform permit, deny, block, approval, escalation, or execution actions.

## 6. Structural-misalignment evaluation

For a reliance event, Fork preserves separate component results:

- `C_V`: current recorded validity is compatible with the accepted validity states declared for the use;
- `C_R`: observed reliance is compatible with the claim's permitted-reliance class and context;
- `C_A`: observed reliance is compatible with current recorded authority status, class, and context;
- `G`: external governance-profile evaluation, one of `SATISFIED`, `NOT_SATISFIED`, or `NOT_EVALUABLE`;
- `C_N`: source non-claims survive in the observed representation;
- `C_L`: lineage independence declarations match the preserved roots and validation records.

The aggregate structural result is:

```text
M = not C_V
    or not C_R
    or not C_A
    or G == NOT_SATISFIED
    or not C_N
    or not C_L
```

`NOT_EVALUABLE` does not create governance-profile misalignment by itself. Component results MUST remain visible even when `M` is emitted.

Structural misalignment is an evidence property. Compliance remains an external interpretation unless an external profile explicitly defines and authorizes that determination.

## 7. First-class event families

### 7.1 `validity_state_transition_event`

Records an explicit transition in evidentiary currency. It may change validity and MUST NOT change authority.

### 7.2 `authority_transition_event`

Records an explicit grant, narrowing, expiration, revocation, or supersession of authority. It may change authority and MUST NOT change validity.

### 7.3 `reliance_event`

Records observed use, context, source non-claims, lineage, and any declared governance profile. It changes neither validity nor authority.

### 7.4 `reliance_authority_misalignment_event`

Records deterministic compatibility results and lineage indicators. It is a specialized failed claim-consumption record, not an enforcement event.

## 8. Non-claim survival

A downstream representation can expand effective scope without changing the positive sentence. Removing uncertainty, exclusions, temporal limits, or explicit non-authority statements may make a claim appear more definitive than its source boundary.

The checker therefore compares `source_non_claims` with `observed_non_claims`. Missing source non-claims produce `NON_CLAIM_LOSS` and the `NON_CLAIM_SURVIVAL` misalignment dimension.

## 9. Lineage indicators

Let:

- `D` = derivation depth;
- `V_c` = independent validation count;
- `R` = apparent supporting-reference count;
- `R_i` = independently validated root count.

The checker emits:

```text
DVG = D - V_c
DVR = D / max(1, V_c)
PCI_count = R - R_i
PCI_ratio = R / max(1, R_i)
```

These are descriptive lineage-pressure indicators only. They are not truth, legitimacy, compliance, or risk scores.

`validation_chain_depth` is preserved separately from `independent_validation_count`. Sequential depth and independent validation count MUST NOT be treated as equivalent.

## 10. External governance profiles

An external governance profile may declare required reliance classes, authority statuses, validity states, and contexts. Fork may recompute whether the preserved event satisfies the declared profile. Fork does not determine that the profile is legally sufficient, institutionally valid, or appropriate.

Governance evaluation states:

- `SATISFIED`
- `NOT_SATISFIED`
- `NOT_EVALUABLE`

`NOT_EVALUABLE` MUST NOT be interpreted as either compliance or noncompliance.

## 11. Checker output boundary

A passing checker result establishes only that governed fixtures satisfy this module's schemas and structural invariants under the checker version recorded in the output.

It does not establish:

- source truth or completeness;
- legal or regulatory compliance;
- authority-basis sufficiency;
- institutional permission;
- answerability or liability;
- safe execution;
- production readiness;
- endorsement or certification.

## 12. Relationship to Cross-System Claim Handoff v0.1

This module does not alter the primary Cross-System Claim Handoff v0.1 hypothesis or baseline corpus. Authority accretion may be classified as an optional unsupported-inheritance subtype when observed, but repeated temporal reuse belongs to a later experiment.

## 13. Deferred experiment

`HISTORICAL_AUTHORITY_ACCRETION_EXPERIMENT_DRAFT_v0_1.md` is a deferred draft. Baseline execution is prohibited until the Experimental Extension Protocol admits it through preregistration, corpus freeze, receiver registration, and baseline-protection requirements.
