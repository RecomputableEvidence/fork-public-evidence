# CCEC Governance Interoperability Profile v0.1

## Status

Controlled pilot structural interoperability profile.

This document defines how a Claim Consumption Event Contract, or CCEC, may be referenced by surrounding governance systems without being converted into approval, truth, safety, compliance, legal sufficiency, institutional authorization, policy satisfaction, risk acceptance, or authority transfer.

## Purpose

A CCEC records local reliance behavior:

> This receiving workflow consumed this bounded source artifact in this local way, preserved these non-claims, left these unresolved gaps open, and named this local decision owner.

A CCEC Governance Interoperability Profile records how an external governance system may ingest, reference, route, or preserve that CCEC.

The central question is:

> What may travel into the surrounding governance system without silently transferring authority?

## Accord principle

A contract unifies two or more parties in mutual accord.

A CCEC Governance Interoperability Profile defines the accord between:

- the bounded CCEC record;
- the external governance system;
- the local owner accountable for any downstream decision;
- the preserved non-claims and unresolved gaps that must not be collapsed.

The profile does not make Fork the governance system. It does not make the external governance system a Fork verifier. It defines the permitted field-level relationship between them.

## Surrounding systems

This profile is intended for bounded references into systems such as:

- GRC registers;
- audit evidence systems;
- policy registers;
- risk registers;
- legal review queues;
- model governance systems;
- evidence management systems;
- procurement and vendor-risk workflows;
- insurance and underwriting review workflows.

## Permitted mappings

A surrounding governance system may reference a CCEC as:

- an evidence reference;
- a boundary record reference;
- a local reliance record;
- an unresolved gap reference;
- a non-claim reference;
- a decision owner reference;
- a boundary effect reference;
- a source artifact reference;
- a receiving context reference.

These mappings preserve evidence-boundary structure. They do not create approval, compliance, legal, safety, risk, or authority status.

## Prohibited mappings

A CCEC must not be mapped into:

- approval status;
- truth status;
- safety status;
- compliance status;
- legal sufficiency status;
- institutional authorization status;
- policy satisfaction status;
- risk acceptance status;
- authority transfer;
- claim expansion by mapping;
- automated control decision.

## Local authority boundary

A CCEC may show that a local reliance decision was recorded.

It does not prove that the decision was authorized, correct, compliant, safe, legally sufficient, policy-satisfying, or risk-accepted.

A surrounding governance system must make its own local decision before changing any approval-like, compliance-like, safety-like, legal-like, policy-like, risk-like, or authority-like status.

## Checker scope

`tools/check_ccec_governance_interoperability.py` performs structural validation only.

It checks:

- JSON parseability;
- schema conformance;
- required permitted and prohibited mappings;
- mapping-rule consistency;
- forbidden oracle-like target fields;
- authority-inheritance prohibition;
- unresolved-gap preservation;
- machine-readable non-claims;
- checker output contract conformance.

It does not check:

- whether the underlying CCEC is true;
- whether the external governance system is compliant;
- whether the receiving decision was correct;
- whether the external owner had authority;
- whether policy was satisfied;
- whether risk was accepted;
- whether legal sufficiency exists.

## Canonical summary

A CCEC interoperability profile defines what surrounding governance systems may reference from a Claim Consumption Event Contract without inheriting authority, approval, truth, safety, compliance, legal sufficiency, policy satisfaction, or risk acceptance.

Evidence may enter the governance system.

Non-claims and unresolved gaps must enter with it.

Authority remains local.
