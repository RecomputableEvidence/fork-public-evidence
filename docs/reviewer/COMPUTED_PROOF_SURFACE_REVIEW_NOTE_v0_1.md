# Computed Proof Surface Review Note v0.1

## Short reviewer note

Fork's public surface now contains both fixture-declared governance scenarios and a computed derivation path.

Computed Proof Surface v0.1 is a consolidation layer. It tells reviewers which parts of the surface are authored fixtures, which parts are structurally checked, which parts are derived from independent state inputs, and which conclusions Fork intentionally refuses to make.

## The important change

The computed Scenario 09 work moves one failure mode from declared scenario output to deterministic derivation.

The checker now derives a revocation visibility / split-state gap from:

```text
System A current revocation state
System B visibility and sync state
System C downstream consumption attempt
freshness policy
```

That does not make Fork an approval system. It means Fork can show how a specific gap classification was produced from supplied state inputs.

## Bounded claim

The bounded claim is:

```text
Fork can preserve and compute selected governance-state divergence records in a way that supports later reviewer reconstruction.
```

The claim is not:

```text
Fork decides the external consequence of the underlying event.
```

## Current maturity read

This is still a reference implementation, not a production platform.

However, the public surface has moved beyond pure concept documentation. It now contains:

```text
scenario taxonomy
boundary artifacts
viewer surfaces
bounded checkers
computed state divergence
explicit non-conclusions
```

That is enough to support design-partner review of the architectural category.

## Recommended reviewer question

The strongest reviewer question now is:

```text
Can Fork show what evidence closes a detected gap without silently converting closure into approval?
```

That is the reason Scenario 10 should be a Resolution / Synchronization Boundary rather than another failure-only scenario.
