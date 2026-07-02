# Fork Simulation Contracts and Interfaces v0.1

## Purpose

This document defines the contracts and interface artifacts used in Fork's governance simulation proof surface.

The purpose is to preserve and expose handoff-state behavior without turning Fork into an authority, runtime, policy, compliance, or audit system.

## Contract Artifacts

### Claim Boundary Contract

Describes the scope of claims crossing a boundary, including explicit inclusions, exclusions, and conditions.

### Boundary Delta Record

Captures changes in claim scope, authority context, evidence references, unresolved state, or downstream reliance between upstream and downstream states.

### Claim Consumption Event

Records how a downstream system consumed an upstream claim, including preserved, narrowed, expanded, unresolved, or unsupported reliance classifications.

### System Mapping Receipt

Records mapping between systems and artifacts at a boundary, including identifiers, roles, routing context, and mapping posture.

### Authority Policy Context

Documents policy references, roles, and constraints present at the time of handoff without asserting approval, applicability, compliance, or authority sufficiency.

### Non-Claims Panel

Enumerates explicit non-claims associated with the handoff.

Examples:

- not an approval;
- not a compliance certification;
- not legal sufficiency;
- not production readiness;
- not factual correctness;
- not institutional authority.

### Unsupported Inheritance Event Record

Records detected instances where downstream inference exceeded recorded claim scope, authority, evidence, or non-claims.

## Interface Discipline

Each contract is:

- bounded to a specific handoff boundary;
- inspectable;
- capable of being represented as structured data;
- designed to preserve state, not enforce runtime behavior;
- designed to avoid certifying correctness, compliance, or authority.

## Interface Questions

Every interface should answer:

1. What object crossed the boundary?
2. What claims were attached?
3. What non-claims remained attached?
4. What authority context was recorded?
5. What evidence references were preserved?
6. What unresolved state remained?
7. What downstream revalidation was required?
8. What did the downstream system do with the object?
9. Did any claim expansion occur?
10. Did any expansion have new authority or evidence?

## Prohibited Interface Drift

Simulation interfaces must not collapse:

- evidence into approval;
- policy reference into policy applicability;
- structural verification into factual correctness;
- human review into legal sufficiency;
- routing into authorization;
- auditability into compliance;
- recomputability into truth.

## Safe Interface Claim

Fork simulation interfaces preserve accountable handoff state for later inspection.

They do not decide whether the downstream reliance was justified.