# AHI Proof Surface Map v0.1

## One-sentence orientation

The AHI proof surface shows how Fork preserves boundary and transition-state evidence when AI-assisted artifacts move between contexts that may otherwise inherit more than the source record supports.

## What the proof surface is

The proof surface is a reviewer-operable casebook.

It contains scenarios, artifacts, checkers, and viewer bundles that make boundary failures inspectable.

It is not a runtime control system, compliance engine, legal oracle, policy engine, model monitor, or approval layer.

## What Fork preserves

Fork can preserve:

- claim scope;
- non-claims;
- authority context;
- evidence references;
- unsupported downstream inheritance;
- transition state;
- revalidation requirements;
- split-state visibility and consumption gaps;
- deterministic reconstruction support.

## What Fork does not decide

Fork does not decide truth, legal sufficiency, compliance, admissibility, approval, authorization, safety, correctness, negligence, excuse, external acceptance, or execution eligibility.

## Scenario map

```text
01 Baseline unbounded handoff
02 Fork-preserved handoff
03 Scope expansion attempt
04 Authority leakage attempt
05 Policy-reference laundering / non-claim suppression
06 Multi-system distributed handoff
07 External authority bridge
08 Stale validity / authority revocation
09 Revocation visibility / split-state boundary
```

## Boundary families

| Family | Scenarios | Question |
|---|---:|---|
| Handoff baseline | 01–02 | Did the handoff preserve what was and was not claimed? |
| Claim promotion | 03 | Was a bounded claim expanded downstream? |
| Authority promotion | 04, 06, 07 | Was authority borrowed, distributed, or externally inferred? |
| Policy/non-claim laundering | 05 | Were limitations hidden behind policy references? |
| Temporal validity | 08 | Was prior validity treated as current validity? |
| Split-state propagation | 09 | Was a validity change treated as globally visible, consumed, or operative without evidence? |

## Why Scenario 08 and Scenario 09 matter together

```text
Scenario 08: prior validity does not imply current validity
Scenario 09: a current validity change does not automatically propagate across systems
```

Together, they isolate a common governance gap:

```text
temporal state changed, but downstream reliance treats either old state or partial state as sufficient.
```
