# Continuity Boundary Object Profile v0.1

## Status

Draft profile.

This profile defines a neutral boundary object for carrying structured evidence of an asserted continuity path across independently governed systems.

It is not specific to any one upstream governance system, control layer, attestation layer, preservation layer, or verification layer.

## Purpose

A Continuity Boundary Object, or CBO, is the minimal structured record needed for evidence of an asserted continuity path to cross a system boundary without transferring authority.

The CBO supports artifact-first collaboration between independently bounded systems. It allows one system to emit structured evidence and another system to preserve, recompute, compare, or reference that evidence without inheriting the emitting system's authority.

## Core Distinction

The CBO is not causality itself.

The CBO is structured evidence of an asserted causal, procedural, governance, or execution-continuity path.

An upstream system may assert that certain decisions, invariants, controls, states, or transitions occurred within its authority domain.

A downstream preservation or recomputation system may preserve and verify the emitted evidence boundary.

The downstream system does not thereby verify the truth, admissibility, legality, safety, compliance, authorization, approval, or causal correctness of the upstream assertion.

## Canonical Boundary Line

An upstream system may govern what may occur.

Fork may preserve what may later be structurally demonstrated.

The Continuity Boundary Object carries the minimum structured evidence needed for those two statements to remain connected without either system speaking for the other.

## Authority Separation Rule

Each participating system remains authoritative only over its own declared boundary.

The emitting system is responsible for the claims it makes about its own decisions, invariants, controls, states, and transitions.

The receiving system is responsible only for what it preserves, recomputes, compares, reports, or declines to infer.

No system may silently inherit another system's authority through the CBO.

## Required Semantics

A valid CBO profile preserves these semantics:

- `authority_transfer` is false.
- `upstream_authority_inherited_by_receiver` is false.
- `receiver_verifies_upstream_governance` is false.
- `causality_crosses_boundary` is false.
- upstream claims remain distinguishable from downstream preservation claims.
- non-claims remain attached to the continuity object.
- unresolved references remain visible.
- evidence preservation does not become approval, authorization, compliance, safety, admissibility, risk acceptance, or causal proof.

## Minimal Object Sections

A CBO should include:

1. profile identity;
2. issuer system boundary;
3. receiver system boundary;
4. continuity object semantics;
5. upstream asserted events;
6. emitted evidence references;
7. downstream preservation boundary;
8. non-claims;
9. consumer constraints;
10. integrity metadata;
11. unresolveds;
12. expected boundary result.

## Fork Interpretation

When Fork preserves or evaluates a CBO, Fork may report:

- whether the CBO record is structurally valid;
- whether referenced evidence is present or missing;
- whether declared digests recompute, if digest metadata is in scope;
- whether preserved artifacts match later artifacts;
- whether upstream claims and non-claims remain distinguishable;
- whether unresolved pointers remain unresolved;
- whether downstream consumers dropped non-claims or expanded claims.

Fork does not report:

- whether the upstream governance decision was valid;
- whether the upstream control caused the event;
- whether the asserted causal path is true;
- whether the action was legally sufficient;
- whether the action was compliant;
- whether the action was safe;
- whether the action was institutionally approved;
- whether the evidence is admissible.

## Upstream Interpretation

An upstream system may use a CBO to expose:

- what decision it asserts it made;
- what invariants it asserts applied;
- what admission or control state it asserts existed;
- what execution transition it asserts occurred;
- what evidence it emitted for downstream preservation.

The upstream system does not need to expose proprietary internals unless it chooses to. It only needs to emit enough structured evidence for the downstream continuity boundary to remain inspectable.

## Boundary Failure Modes

A CBO should be treated as boundary-risky if:

- the receiver is asked to verify upstream authority;
- causal language is converted into proof language;
- non-claims are dropped;
- unresolved references are hidden;
- digest or seal metadata is asserted but not recomputable;
- the object is used as approval or compliance evidence without separate authority;
- downstream systems treat preservation as authorization;
- upstream systems treat downstream recomputation as validation of governance correctness.

## Design Principle

The CBO makes continuity inspectable without making authority transferable.

The purpose is not to collapse governance and evidence into one system.

The purpose is to let independently bounded systems participate in a shared continuity record while preserving separate claims, non-claims, and verification limits.
