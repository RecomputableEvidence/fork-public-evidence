# Claim Consumption Event Contract v0.1

## Status

Controlled pilot structural contract.

This document defines a Claim Consumption Event, or CCE, for recording how a receiving actor, system, workflow, or institution consumes a claim-bounded artifact.

A Claim Consumption Event is not an approval record. It is not a truth finding. It is not a compliance certification. It is not a legal sufficiency determination. It is a bounded structural record of local reliance behavior.

## Purpose

A Claim Boundary Contract describes what an originating artifact claims, does not claim, and leaves unresolved.

A Claim Consumption Event describes what a downstream receiver did with that bounded artifact.

The central question is:

> When evidence travels, did authority silently travel with it?

CCE v0.1 makes the receiving-side boundary inspectable by recording:

- which source artifact was consumed;
- which claims were relied on;
- which non-claims remained preserved;
- which unresolved gaps remained unresolved;
- whether the receiving workflow preserved, narrowed, expanded, rejected, or could not determine the original boundary;
- who owned the local reliance decision;
- what the record explicitly does not validate.

## Relationship to Claim Boundary Contracts

CBC answers:

> What did the source artifact claim, not claim, and leave unresolved?

CCE answers:

> What did the receiving context treat that source artifact as sufficient for?

CCE does not replace CBC. It depends on CBC-style bounded claims and adds a downstream consumption record.

## Boundary effects

A CCE must declare exactly one `boundary_effect`.

### PRESERVED

The receiving context relied on the source artifact without expanding the source claim.

### NARROWED

The receiving context relied on less than the source artifact made available.

### EXPANDED

The receiving context treated the source artifact as supporting more than the source artifact claimed.

Expansion is not automatically invalid as an observed event. However, it must be explicit. A CCE with `boundary_effect: "EXPANDED"` must include a `new_claim_reference` identifying the new claim, the expansion reason, and the accountable owner for the expansion.

The checker does not validate whether the expansion was correct. It only verifies that the expansion was not silent.

### REJECTED

The receiving context declined to rely on the source artifact.

### INDETERMINATE

The record does not contain enough information to determine how the receiving context consumed the source artifact.

## Required structural invariants

A valid Claim Consumption Event must:

1. identify the source artifact;
2. identify the receiving actor, system, workflow, or institution;
3. identify the local decision owner;
4. preserve source non-claims;
5. preserve unresolved gaps or explicitly state that no unresolved gaps were present in the event record;
6. declare a boundary effect;
7. describe the local reliance decision;
8. include machine-readable limitations;
9. avoid fields that collapse the event into approval, truth, safety, compliance, or legal sufficiency.

## Non-transitivity rule

A source artifact's supported claim does not automatically become a receiving workflow's authority.

A valid CCE may record local reliance. It does not prove that the local reliance was correct, safe, compliant, legally sufficient, authorized, or institutionally adequate.

## Checker scope

`tools/check_claim_consumption_event.py` performs structural validation only.

It checks:

- JSON parseability;
- schema conformance;
- required non-claim limitations;
- explicit handling of expanded boundaries;
- local decision-owner presence;
- reliance-action consistency;
- forbidden oracle field names.

It does not check:

- whether the source artifact is true;
- whether the receiving decision was correct;
- whether reliance was compliant;
- whether reliance was safe;
- whether reliance was legally sufficient;
- whether the decision owner had valid authority;
- whether policy requirements were actually satisfied.

## Canonical summary

Evidence may travel.

Non-claims should travel with it.

Reliance remains local.

A Claim Consumption Event records that local reliance boundary without converting the record into an approval, compliance, safety, truth, or legal sufficiency oracle.
