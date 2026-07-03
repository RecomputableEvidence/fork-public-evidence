# AHI Scenario Ladder v0.2

## Purpose

This ladder explains the conceptual progression from basic unbounded handoff to temporal validity non-inheritance.

## Ladder

### Scenario 01 â€” Baseline Unbounded Handoff

Shows the uncontrolled baseline: an AI-assisted artifact moves downstream without explicit boundary state.

Risk:

```text
unbounded reliance
```

### Scenario 02 â€” Fork-Preserved Handoff

Shows the bounded contrast: Fork preserves claim boundary, non-claims, and inspectable transition context.

Result:

```text
bounded inspectability
```

### Scenario 03 â€” Scope Expansion Attempt

Tests whether a downstream actor expands a bounded claim into a broader claim.

Failure mode:

```text
SCOPE_EXPANSION_ATTEMPT
```

### Scenario 04 â€” Authority Leakage Attempt

Tests whether authority context leaks beyond the scope in which authority was exercised.

Failure mode:

```text
AUTHORITY_LEAKAGE_ATTEMPT
```

### Scenario 05 â€” Policy-Reference Laundering / Non-Claim Suppression

Tests whether a policy reference is laundered into a policy-satisfaction claim, or non-claims are suppressed downstream.

Failure mode:

```text
POLICY_REFERENCE_LAUNDERING_ATTEMPT
```

### Scenario 06 â€” Multi-System Distributed Handoff

Tests whether distributed systems silently inherit authority across multiple transitions.

Failure mode:

```text
UNSUPPORTED_DISTRIBUTED_AUTHORITY_INHERITANCE
```

### Scenario 07 â€” External Authority Bridge

Tests whether internal inspectability is converted into external authority, admissibility, compliance, acceptance, legal sufficiency, or execution eligibility.

Failure mode:

```text
EXTERNAL_AUTHORITY_BRIDGE_ATTEMPT
```

### Scenario 08 â€” Stale Validity / Authority Revocation Boundary

Tests whether prior validity, prior authority, prior evidence, prior policy version, or prior role context is reused as if it remained current after expiry, revocation, supersession, narrowing, or changed context.

Failure mode:

```text
STALE_VALIDITY_RELIANCE_ATTEMPT
```

Invariant:

```text
Prior validity does not imply current validity.
```

## What the ladder shows

The proof surface now covers six major downstream reliance hazards:

1. scope expansion;
2. authority leakage;
3. policy-reference laundering;
4. distributed authority inheritance;
5. external authority bridge;
6. stale validity / authority revocation.

## Boundary discipline

Each scenario preserves the same discipline:

Fork records bounded transition state. Fork does not become the authority, policy engine, runtime controller, compliance oracle, legal sufficiency oracle, truth oracle, or acceptance authority.
