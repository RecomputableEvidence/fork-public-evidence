# Boundary-Crossing Evidence Inspectability Layer v0.1

Status: Experimental
Scope: Structural handoff inspectability only

## Purpose

The Boundary-Crossing Evidence Inspectability Layer is a Fork-local layer for making multi-system governance handoffs inspectable without allowing any participant to silently borrow authority from another participant.

It preserves issuer-native artifacts, maps them into Fork-normalized handoff records, checks whether claims and non-claims remain visible, rejects authority-transfer attempts, and reports what is structurally inspectable, unresolved, or invalid.

## Core supported claim

Fork can make boundary-crossing evidence inspectable by preserving native upstream artifacts, normalizing their declared evidence boundaries, checking claim and non-claim preservation, recomputing declared integrity material where possible, and reporting boundary failures without becoming the authority of any upstream system.

## Required non-claims

This layer does not claim:

- approval;
- authorization;
- certification;
- compliance;
- compatibility recognition;
- endorsement;
- EVIDE compatibility;
- GLM compatibility;
- interoperability recognition;
- legal sufficiency;
- provenance recognition;
- risk acceptance;
- runtime control;
- safety;
- SC governance validation;
- truth;
- causality validation;
- admissibility validation.

## What the layer receives

The layer receives issuer-native artifacts. Examples include a governance boundary declaration, an execution continuity packet, a registry event, a seal event, an audit receipt, or another governance-adjacent artifact.

The native artifact remains attributable to its issuer. Fork does not rewrite the issuer's authority domain. Fork only records what was emitted, what was claimed, what was not claimed, what references were provided, what could be structurally checked, and what remained unresolved.

## What the layer emits

The layer emits a Fork-normalized handoff record with:

- source artifact identifiers;
- issuer systems;
- authority domains;
- preserved claims;
- preserved non-claims;
- authority-transfer flags;
- public-attribution constraints;
- recomputation status;
- unresolved references;
- structural result kind;
- do-not-map-to tokens.

## Positive result meaning

`BOUNDARY_CROSSING_EVIDENCE_INSPECTABLE` means only that the submitted bundle satisfied this layer's structural handoff checks.

It does not mean the upstream systems were correct, safe, compliant, endorsed, compatible, authorized, admissible, legally sufficient, interoperable, or true.

## Failure result meaning

A failure means the handoff bundle is not structurally inspectable under this layer's v0.1 contract. The failure may result from an authority-borrowing attempt, dropped non-claim, public-attribution leak, undeclared unresolved reference, recomputation overclaim, invalid review state, invalid recomputation state, duplicate JSON key, UTF-8 BOM, or missing required boundary field.

## Design rule

The layer treats recomputation as integrity evidence, not truth evidence.

A digest match can support a statement that the recomputed subject matches the declared digest under the declared method. It does not support a statement that the upstream governance, causality, safety, compliance, legal sufficiency, approval, or substantive truth of the underlying event was validated.

## Demonstrator path

The v0.1 demonstrator uses two upstream artifact classes:

1. A declarative governance boundary artifact.
2. An execution-continuity artifact.

Fork preserves each native artifact class, maps each into a bounded handoff record, checks whether non-authority boundaries remain intact, and reports whether the multi-system handoff is structurally inspectable.
