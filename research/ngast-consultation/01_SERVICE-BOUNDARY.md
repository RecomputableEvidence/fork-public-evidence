# 01_SERVICE-BOUNDARY

**Object ID:** `NGAST-CONSULTATION-01-SERVICE-BOUNDARY`  
**Version:** `v0.1-CANDIDATE`  
**Parent:** `NGAST-CONSULTATION-FOUNDATION-001-v0.1-FREEZE`  
**Parent SHA-256:** `e8dc36afa92afaefdc6e2e48bf815f0fbd1968c8d7febedb1068ef824a7ac044`  
**Parent relation:** `BOUNDED_SUCCESSOR_INPUT`  
**Standing inheritance:** `NONE`  
**Admission:** `NOT_YET_ADMITTED`  
**Service availability effect:** `NONE`  
**Candidate package SHA-256:** `4e54387ebde8bf5a6938ad9347805d5dade2e0e15f84cc0aea11b4dc56a9022c`  
**Admission receipt digest:** `4918311e3e45b87ba3455cea15e609780f8d8bed7eb703914babd1da9d0a48a8`

## Purpose

Define what NGAST Consultation may examine, what it may produce, what authority it does not hold, what kinds of conclusions it may and may not issue, and which external professional dependencies must remain explicit.

## Bounded service proposition

NGAST Consultation may examine bounded AI-assisted systems, evidence flows, authority relations, decision records, failure surfaces, governance controls, and intervention opportunities within an explicitly authorized engagement scope.

Subject to the engagement's access and authority boundary, work products may include:

- operational system reconstruction;
- evidence-source and claim-support mapping;
- identification and delineation of evidence gaps, missingness, uncertainty, and unresolved states;
- client-specific, falsifiable worked scenarios using bound operational values;
- counterexamples and pressure tests;
- intervention-option analysis;
- mitigation and mediation design;
- solutions work orders;
- authorized implementation support;
- post-intervention recomputation or verification against a named rule;
- executive and technical views derived from the same bound engagement record.

## Authority exclusions

NGAST Consultation does not, merely by performing an engagement:

- issue legal opinions or determine legal sufficiency;
- certify compliance or regulatory approval;
- assume client decision rights or operational authorization;
- establish universal system correctness, safety, fairness, security, or governance maturity;
- determine factual truth outside the examined record and authorized system boundary;
- convert client-supplied assertions into independently verified facts;
- convert consultant observation or analysis into client decision or disposition;
- convert recommendation into authorization;
- convert implementation into post-intervention verification;
- validate Fork or promote Fork research standing;
- substitute for external professional expertise where a scoped conclusion depends on legal, privacy, cybersecurity, insurance, tax, regulatory, jurisdictional, domain-safety, quantum-physics/hardware, or other named specialist expertise.

## Engagement relation sequence

```text
CLIENT_CONCERN
→ AUTHORIZED_SCOPE
→ ACCESS_BOUNDARY
→ OBSERVATION / RECONSTRUCTION
→ EVIDENCE_DECONSTRUCTION
→ FALSIFIABLE_SCENARIOS
→ FINDINGS + RESIDUAL_UNCERTAINTY
→ INTERVENTION_OPTIONS
→ CLIENT_DISPOSITION
→ AUTHORIZED_WORK_ORDER
→ IMPLEMENTATION
→ POST_INTERVENTION_VERIFICATION
```

The arrows are relations, not inheritance channels.

## Governing non-equivalences

```text
ACCESS != AUTHORITY
CLIENT_SUPPLIED_FACT != INDEPENDENTLY_VERIFIED_FACT
CONSULTANT_OBSERVATION != CLIENT_DECISION
CONSULTANT_ANALYSIS != CLIENT_DISPOSITION
RECOMMENDATION != AUTHORIZATION
CLIENT_DISPOSITION != IMPLEMENTATION
IMPLEMENTATION != POST_INTERVENTION_VERIFICATION
RECOMPUTATION != COMPLIANCE_CERTIFICATION
CLIENT_ENGAGEMENT != FORK_VALIDATION
```

## External professional dependencies

Where a scoped conclusion depends on expertise or authority not held by NGAST Consultation, the dependency must remain explicit and the external expert's conclusion retains its own identity and standing.

Named dependency classes presently include:

- legal;
- privacy;
- cybersecurity;
- insurance;
- tax;
- regulatory;
- jurisdictional;
- domain safety;
- quantum physics or hardware;
- other named subject-matter expertise.

Naming a dependency does not establish competence or authority in that domain.

## Commercial boundary

This candidate does not authorize pricing, public solicitation, engagement acceptance, enterprise-readiness claims, or website language describing NGAST Consultation as publicly available.

Those remain downstream of the foundation gates.

## Candidate disposition

The separately preserved candidate package verifies `PASS files=9 checksums=8 admission=NOT_YET_ADMITTED`.

Recommended state: `READY_FOR_BOUNDARY_REVIEW`.

Repository placement of this candidate has `standing_effect = NONE` and does not alter repository-wide Fork standing.
