# Fork Non-Claim Boundary v0.1

## Purpose

This document states the universal non-claim boundary for Fork's public/reviewer surface.

It is intended to prevent reviewers, prospects, advisors, integrators, downstream systems, or automation layers from treating preserved evidence as proof of claims Fork does not make.

## Core boundary

Fork preserves bounded evidence records.

Fork does not decide what the preserved record legally, clinically, ethically, commercially, operationally, or institutionally authorizes.

## Fork may support review of

Fork public artifacts may support review of:

- declared artifact membership;
- declared evidence boundaries;
- byte-level integrity checks;
- manifest and checksum relationships;
- bounded schema or checker behavior;
- explicit PASS, FAIL, NOT_CHECKED, PARTIAL, STALE_CONTEXT, OUT_OF_SCOPE, or SOURCE_UNAVAILABLE states where applicable;
- explicit non-claims and unresolved unknowns;
- whether a preserved record still matches its declared boundary.

## Fork does not establish

Fork public artifacts do not establish:

- source truth;
- source completeness;
- workflow completeness;
- AI-output correctness;
- decision correctness;
- legal admissibility;
- compliance satisfaction;
- ethical correctness;
- audit sufficiency;
- production readiness;
- client deployment;
- live institutional operation;
- public signer identity;
- non-repudiation;
- third-party verifier independence;
- append-only persistence unless separately established;
- RFC 3161 validation unless separately established;
- full replay of hidden vendor behavior;
- complete external telemetry;
- authority validity;
- remediation sufficiency;
- reporting sufficiency;
- runtime blocking authority;
- approval, waiver, authorization, or risk acceptance.

## Automation boundary

No downstream automation should map a Fork verification result directly to:

- approval;
- authorization;
- compliance;
- legal sufficiency;
- safety;
- production readiness;
- workflow blocking;
- waiver approval;
- risk acceptance;
- remediation closure.

Any such decision must be made by a separate authorized process with its own authority, accountability, evidence, and review path.

## Reviewer rule

When reviewing or citing Fork, state both the supported claim and the non-claim boundary.

A statement about Fork is incomplete if it describes what a verifier checked but omits what the verifier does not establish.
