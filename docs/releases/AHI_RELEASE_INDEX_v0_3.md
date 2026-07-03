# AHI Release Index v0.3

## Current release position

| Surface | Current tag | Scope |
|---|---:|---|
| AHI simulation proof surface | `ahi-sim-v0.1.10` | Scenarios 01–09 |
| AHI viewer v0.1 | `ahi-viewer-v0.1.7` | Scenario-bundle viewer with nine scenarios |
| AHI viewer v0.2 | `ahi-viewer-v0.2.2` | Canonical comparison-pair viewer including Scenario 08 ↔ Scenario 09 |
| Release index | `ahi-release-index-v0.3` | Post-Scenario-09 release map |
| Reviewer packet | `ahi-reviewer-packet-v0.1` | Reviewer-facing proof-surface orientation |

## Category statement

Fork preserves transition-state evidence for AI-assisted institutional workflows.

It records what crossed a boundary, what did not cross, what remained unsupported, what required revalidation, and what later reliance attempted to inherit.

Fork does not approve, certify, score, authorize, determine compliance, determine admissibility, establish legal sufficiency, decide acceptance, judge correctness, determine negligence, or determine excuse.

## Scenario coverage

| Scenario | Title | Primary boundary |
|---:|---|---|
| 01 | Baseline Unbounded Handoff | Unbounded downstream reliance |
| 02 | Fork-Preserved Handoff | Bounded preservation |
| 03 | Scope Expansion Attempt | Claim-scope expansion |
| 04 | Authority Leakage Attempt | Authority-context leakage |
| 05 | Policy Reference Laundering / Non-Claim Suppression | Policy/non-claim laundering |
| 06 | Multi-System Distributed Handoff | Distributed authority inheritance |
| 07 | External Authority Bridge | External authority borrowing |
| 08 | Stale Validity / Authority Revocation Boundary | Temporal validity non-inheritance |
| 09 | Revocation Visibility / Split-State Boundary | Visibility, consumption, and split-state propagation |

## Latest scenario invariant

```text
recorded_in_A does not imply visible_in_B
visible_in_B does not imply consumed_by_C
not_visible_locally does not imply still_valid_currently
```

Failure mode:

```text
REVOCATION_VISIBILITY_GAP
```

## Reviewer entry points

1. `docs/reviewer/FORK_AHI_REVIEWER_PACKET_v0_1.md`
2. `docs/reviewer/AHI_PROOF_SURFACE_MAP_v0_1.md`
3. `docs/releases/AHI_SCENARIO_LADDER_v0_3.md`
4. `docs/releases/AHI_LOCAL_VERIFICATION_GUIDE_v0_3.md`
