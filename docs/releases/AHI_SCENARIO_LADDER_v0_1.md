# AHI Scenario Ladder v0.1

## Purpose

The AHI scenario ladder shows how the simulation surface progresses from a baseline unbounded handoff to increasingly explicit boundary-failure modes.

Each scenario adds one governance failure mode without allowing Fork to become an authority layer.

## Ladder

### Scenario 01 â€” Baseline unbounded handoff

Shows the baseline problem: AI-assisted work can move downstream without enough boundary state for later reconstruction.

Primary lesson:

```text
Without explicit boundary records, downstream reliance can inherit more than the upstream artifact actually supports.
```

### Scenario 02 â€” Fork-preserved handoff

Introduces artifact-backed preservation.

Artifact family:

- Boundary Delta Record
- Claim Boundary Contract
- Claim Consumption Event
- System Mapping Receipt
- Unsupported inheritance event
- Authority/policy context
- Non-claims panel

Primary lesson:

```text
Fork can preserve what crossed, what did not cross, and what must not be inferred.
```

### Scenario 03 â€” Scope expansion attempt

Tests downstream expansion of a bounded claim.

Primary lesson:

```text
A bounded claim cannot silently become a broader claim merely because it moved downstream.
```

### Scenario 04 â€” Authority leakage attempt

Tests whether authority context is improperly inherited.

Primary lesson:

```text
Authority possessed and authority exercised are not the same claim.
```

### Scenario 05 â€” Policy-reference laundering / non-claim suppression

Tests the failure where a policy reference is treated as policy satisfaction, or limitations disappear downstream.

Primary lesson:

```text
Citing a policy does not establish that the policy was satisfied.
```

### Scenario 06 â€” Multi-system distributed handoff

Tests distributed authority inheritance across multiple independently accountable systems.

Primary lesson:

```text
Individually bounded systems can still create governance failure at the transition between them.
```

Scenario 06 has two major release steps:

- `ahi-sim-v0.1.6`: structural simulation
- `ahi-sim-v0.1.7`: semantic invariant verification

### Scenario 07 â€” External authority bridge

Tests the external boundary where an internal Fork-preserved record is provided to an external reviewer, auditor, regulator, customer, board, insurer, legal process, or other authority-bearing context.

Primary lesson:

```text
Inspectability does not establish external admissibility, compliance, approval, legal sufficiency, acceptance, or execution eligibility.
```

## Scenario progression

```text
01: Unbounded handoff baseline
02: Boundary preservation
03: Scope expansion detection
04: Authority leakage detection
05: Policy-reference laundering / non-claim suppression
06: Distributed authority non-inheritance
07: External authority bridge non-inheritance
```

## Strategic meaning

The ladder demonstrates that Fork is not a policy engine, runtime control system, compliance oracle, approval system, or legal authority.

Fork preserves bounded evidence and transition state so later reviewers can reconstruct what was claimed, what was not claimed, what was relied on, what was unsupported, and what required revalidation.