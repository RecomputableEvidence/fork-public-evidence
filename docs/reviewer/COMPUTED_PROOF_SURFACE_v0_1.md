# Computed Proof Surface v0.1

## Status

Reviewer-facing consolidation layer.

## Purpose

Computed Proof Surface v0.1 explains the current boundary between authored fixtures, computed derivations, reconstructed state, preserved evidence context, and explicit non-conclusions.

It is not a new authority layer. It is a map of the current Fork public evidence surface.

## Why this layer exists

Fork's public surface now contains both fixture-declared scenarios and at least one computed derivation path.

Without a consolidation layer, a reviewer has to infer which artifacts are illustrative, which are structurally checked, which are derived from independent state inputs, and which conclusions remain outside Fork's boundary.

Computed Proof Surface v0.1 makes those distinctions explicit.

## Four evidence modes

### 1. Fixture-declared records

Fixture-declared records are authored scenario artifacts. They demonstrate bounded governance failure modes and expected structural relationships.

Current examples include:

```text
Scenario 01 - baseline unbounded handoff
Scenario 02 - Fork preserved handoff
Scenario 03 - scope expansion attempt
Scenario 04 - authority leakage attempt
Scenario 05 - policy-reference laundering / non-claim suppression
Scenario 06 - multi-system distributed handoff
Scenario 07 - external authority bridge
Scenario 08 - stale validity / authority revocation
Scenario 09 - revocation visibility / split-state
```

A fixture-declared record can be checked for shape, required fields, bounded language, and consistency with the declared scenario contract.

A fixture-declared record does not by itself prove that a real workflow was valid, complete, or acceptable for action.

### 2. Structurally checked records

Structurally checked records pass bounded checker logic. The checker can verify that required fields exist, scenario identities align, JSON parses, referenced artifacts exist, prohibited overclaim language is absent, and declared non-inheritance posture is present.

Structural checking supports reviewer reconstruction.

Structural checking does not decide the external consequence of the underlying event.

### 3. Computed derivation records

Computed derivation records are produced from independent state inputs.

Current computed example:

```text
computed_scenario_09
```

The computed Scenario 09 derivation uses:

```text
System A current revocation state
System B visibility and sync state
System C downstream consumption attempt
freshness policy
```

The derivation computes whether the supplied fixture states exhibit:

```text
REVOCATION_VISIBILITY_GAP
SPLIT_STATE_CONSUMPTION_GAP
CURRENT_REVALIDATION_REQUIRED
```

or:

```text
NO_COMPUTED_GAP_RECORDED
```

This is the first current public surface where the result is derived from state divergence rather than only declared by the scenario fixture.

### 4. Reconstructed reviewer surface

The reconstructed reviewer surface is the combined view a reviewer can use to understand:

```text
what was claimed
what was not claimed
what evidence was referenced
what state changed
what transition was attempted
what downstream interpretation was unsupported
what revalidation remained required
which checks were structural
which outputs were computed
```

This reconstructed surface helps preserve transition context without absorbing responsibility for external determinations.

## Current layer map

```text
Primitive layer:
  BDR, CBC, CCE, SMR, ESAL, transition-state concepts

Scenario layer:
  Scenarios 01-09

Viewer layer:
  AHI viewer v0.1
  AHI viewer v0.2

Computed layer:
  Computed Scenario 09 revocation split-state derivation

Reviewer layer:
  Computed Proof Surface v0.1
```

## What is preserved

Fork preserves evidence boundary context, including:

```text
claim scope
non-claims
authority context as represented in the artifact
evidence references
unsupported inheritance attempts
transition state
visibility gaps
sync gaps
revalidation requirements
structural verification results
computed derivation results
```

## What is reconstructed

Fork supports reconstruction of:

```text
which artifact was produced
which boundary record applied
which downstream consumption event occurred
which unsupported inference was recorded
which state inputs were supplied
which deterministic derivation result was produced
which non-claims remained attached
```

## What is computed

At this stage, Fork computes one public derivation class:

```text
Scenario 09 revocation visibility / split-state divergence
```

The computation is intentionally bounded. It computes state divergence under supplied fixture policy. It does not determine whether a real institution should take, stop, permit, or reject any action.

## What remains fixture-based

The following remain primarily fixture-declared and structurally checked:

```text
Scenario 01
Scenario 02
Scenario 03
Scenario 04
Scenario 05
Scenario 06
Scenario 07
Scenario 08
Scenario 09 base fixture artifacts
```

They are still useful because they encode the failure taxonomy and the bounded record semantics. But the strongest current computed path is Scenario 09.

## Non-conclusions

Computed Proof Surface v0.1 does not conclude:

```text
truth of the underlying claim
external validity of the underlying claim
legal sufficiency
compliance status
safety status
fault allocation
approval status
execution eligibility
business suitability
policy correctness
regulatory adequacy
```

Those questions remain with the host institution, reviewer, auditor, regulator, court, or other accountable authority.

## Reviewer reading rule

When reviewing Fork, treat passing checks as evidence of bounded structural consistency and derivation reproducibility inside the declared fixture scope.

Do not treat a passing Fork check as external approval, final adjudication, or permission to rely.

## Current reviewer value

The current public surface is most useful for evaluating whether Fork can:

```text
preserve non-inheritance boundaries
make unsupported downstream expansion visible
separate record integrity from external determination
distinguish fixture-declared results from computed results
derive a split-state gap from independent state inputs
support later reconstruction without becoming the authority
```

## Recommended next technical step

The next technical step after this consolidation is Scenario 10:

```text
Resolution / Synchronization Boundary
```

Scenario 10 should answer:

```text
What observable evidence closes a previously detected gap?
```

That would complete the first lifecycle:

```text
validity established
validity changes
visibility diverges
gap detected
synchronization occurs
new boundary record supports renewed downstream reliance review
```
