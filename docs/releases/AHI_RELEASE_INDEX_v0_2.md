# AHI Release Index v0.2

## Status

Current public AHI proof-surface endpoint:

```text
ahi-sim-v0.1.9
ahi-viewer-v0.1.6
ahi-viewer-v0.2.1
```

This index reflects the Scenario 08 release state.

## Core thesis

Fork is isolating a neglected governance primitive:

```text
transition state between independently accountable systems
```

The AHI proof surface tests whether bounded evidence records preserve claim scope, authority context, non-inheritance, and revalidation requirements as artifacts move across systems.

Fork does not approve, certify, score, authorize, determine compliance, determine admissibility, establish legal sufficiency, decide acceptance, or judge correctness.

## Current release family

| Release | Tag | Scope |
|---|---|---|
| AHI Simulation | `ahi-sim-v0.1.9` | Scenario 08 stale validity / authority revocation boundary |
| Viewer v0.1 | `ahi-viewer-v0.1.6` | Scenario 08 support in the canonical scenario bundle |
| Viewer v0.2 | `ahi-viewer-v0.2.1` | Scenario 08 support in comparison mode |
| Release Index | `ahi-release-index-v0.2` | This release-index refresh |

## Proof-surface progression

| Scenario | Focus | Failure mode |
|---:|---|---|
| 01 | Baseline unbounded handoff | Unbounded downstream reliance |
| 02 | Fork-preserved handoff | Preserved claim boundary |
| 03 | Scope expansion attempt | `SCOPE_EXPANSION_ATTEMPT` |
| 04 | Authority leakage attempt | `AUTHORITY_LEAKAGE_ATTEMPT` |
| 05 | Policy-reference laundering / non-claim suppression | `POLICY_REFERENCE_LAUNDERING_ATTEMPT` |
| 06 | Multi-system distributed handoff | `UNSUPPORTED_DISTRIBUTED_AUTHORITY_INHERITANCE` |
| 07 | External authority bridge | `EXTERNAL_AUTHORITY_BRIDGE_ATTEMPT` |
| 08 | Stale validity / authority revocation boundary | `STALE_VALIDITY_RELIANCE_ATTEMPT` |

## Scenario 08 invariant

```text
Prior validity does not imply current validity.
Prior authority does not imply current authority.
Prior evidence does not imply current evidence sufficiency.
```

Scenario 08 adds temporal non-inheritance coverage. A record, claim, policy reference, evidence basis, role, or authority state that was valid earlier does not automatically remain valid after expiry, revocation, supersession, narrowing, or changed context.

Fork records the stale-validity reliance attempt and preserves required current revalidation. It does not decide whether current reliance is allowed.

## Viewer surfaces

### Viewer v0.1

Viewer v0.1 presents the canonical scenario bundle and now includes Scenario 08.

Expected scenario count:

```text
8
```

### Viewer v0.2

Viewer v0.2 comparison mode now includes the Scenario 07 -> Scenario 08 comparison pair:

```text
PAIR-S07-S08
```

This pair distinguishes external authority non-transfer from temporal validity non-inheritance.

## Local verification

See:

- `docs/releases/AHI_VERIFICATION_MATRIX_v0_2.md`
- `docs/releases/AHI_LOCAL_VERIFICATION_GUIDE_v0_2.md`

## Non-authority boundary

This release index is an inspectability and verification routing document only.

It does not convert any Fork artifact, viewer, checker, release tag, or scenario result into approval, certification, authorization, compliance determination, legal sufficiency, external acceptance, execution eligibility, or correctness.
