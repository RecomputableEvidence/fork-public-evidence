# Reviewer Note v0.1

## Fork Boundary Records and Accountable Handoff Interoperability

### Purpose

This note reframes Fork in a more disciplined research posture.

The current evidence supports a strong engineering pattern and a motivated research hypothesis. It does not yet prove a general systems theory. That distinction matters because Fork’s value is clearest when it is presented as a concrete implementation case, not as proof that a universal architectural primitive has already been established.

The corrected framing is:

> Fork demonstrates one implementation of an accountable handoff pattern in AI-assisted workflows. Whether that pattern generalizes remains a testable hypothesis.

---

## 1. Core Correction

Earlier framing risked overstating the significance of reviewer convergence. The stronger and more defensible claim is not that independent domains have already rediscovered the same architectural primitive. The defensible claim is narrower:

> A set of reviewers, in dialogue with the same author, repeatedly affirmed the importance of preserving boundary separation between evidence, authority, execution, governance, and review.

This remains meaningful. It shows that Fork’s boundary discipline resonates across conversations. But it should be treated as motivating evidence, not proof of a general theory.

The corrected posture is:

> Fork’s current evidence supports an engineering pattern and a motivated hypothesis, not a proven general systems theory.

---

## 2. Recommended Split

The work should now be split into two documents.

### Document 1: Fork Engineering Note

**Working title:**
**Fork Boundary Records for AI-Assisted Workflow Handoffs**

**Primary claim:**
Fork preserves bounded transition records around AI-assisted workflow handoffs so later reviewers can inspect what was claimed, relied upon, excluded, changed, or left unresolved without treating the record as authorization, compliance, or correctness.

**Status:**
This document can stand today. It is practical, implementation-oriented, and immediately defensible.

**Scope:**
This note should focus on Fork’s actual artifact family:

* Boundary Delta Records
* Claim Boundary Contracts
* Claim Consumption Events
* System Mapping Receipts
* Reliance packets

The engineering note should avoid broad claims about universal systems theory. Its contribution is narrower: Fork makes AI-assisted institutional handoffs inspectable without becoming the authority that decides whether the handoff was valid.

---

### Document 2: Hypothesis / Position Paper

**Working title:**
**Accountable Handoff Interoperability: Boundary-State Communication Between Independently Accountable Systems**

**Primary claim:**
We hypothesize that independently accountable systems require explicit handoff-state communication when exchanging consequential state. Fork is one implementation case in AI-assisted workflows; the hypothesis remains unproven until tested through independent implementations in other domains.

**Status:**
This document should be explicitly framed as speculative, falsifiable, and research-oriented.

**Core hypothesis:**
Consequential exchanges between independently accountable systems require explicit handoff-state communication to reduce institutional inference risk.

**Falsifiability condition:**
If independent implementations in other domains do not reproduce the proposed invariants, then the hypothesis should be revised or rejected.

---

## 3. Naming Recommendation

The prior transition-integrity naming should be retired before public release.

The term risks confusion with existing “Transition Integrity Project” references in U.S. election-transition contexts. The replacement language should be neutral, descriptive, and closer to the actual object of study.

Recommended naming:

### Research program

**Accountable Handoff Interoperability**

### Technical specification

**Accountable Handoff Specification**

### Fork artifact family

**Boundary Records**

This naming stack is cleaner:

* **Accountable Handoff Interoperability** names the broader research program.
* **Accountable Handoff Specification** names the technical hypothesis/specification.
* **Boundary Records** names Fork’s concrete artifact family.

---

## 4. Core Thesis

The disciplined thesis is:

> Accountable systems can remain valid within their own boundaries while still producing governance ambiguity at handoff.

The missing object is not another authority layer, audit log, policy engine, or proof surface. The missing object is explicit handoff state:

* what crossed the boundary;
* what did not cross;
* what remained valid;
* what required revalidation;
* what was relied upon;
* what was excluded;
* what must not be inferred downstream.

Fork addresses this problem in AI-assisted institutional workflows by preserving bounded records of those handoffs.

---

## 5. Non-Claims

Fork’s credibility depends on making its non-claims explicit.

Fork does not determine whether a decision was correct.

Fork does not authorize execution.

Fork does not certify compliance.

Fork does not prove institutional authority.

Fork does not replace governance, runtime authority, audit, or review.

Fork does not convert post-execution evidence into retrospective authorization.

Fork preserves bounded handoff records so later reviewers can inspect what was claimed, relied upon, excluded, changed, or left unresolved at the boundary.

---

## 6. Engineering Note Abstract

AI-assisted workflows increasingly produce artifacts that move from draft, analysis, or recommendation into institutional reliance. Existing logs may show that an activity occurred, but often do not preserve the boundary conditions under which the artifact became relied upon: what was claimed, what was excluded, what evidence was referenced, what authority context applied, what remained unresolved, and what should not be inferred downstream.

Fork is a boundary-recording pattern for AI-assisted workflow handoffs. It preserves bounded, tamper-evident transition records that make reliance movement inspectable without becoming an execution authority, compliance oracle, or correctness judgment. This note describes Fork’s core artifacts — Boundary Delta Records, Claim Boundary Contracts, Claim Consumption Events, System Mapping Receipts, and reliance packets — as one implementation of boundary-state communication for AI-assisted institutional workflows.

The contribution is intentionally narrow: Fork does not prove that a decision was correct, authorized, compliant, or sufficient. It preserves the handoff record needed for later reviewers to inspect what moved, what did not, and what remained outside the record’s scope.

---

## 7. Position Paper Abstract

Independently accountable systems increasingly exchange consequential state across governance, execution, audit, procurement, legal, and AI-assisted workflow environments. These systems may remain valid within their own boundaries while still producing ambiguity at handoff: unclear claim scope, authority inheritance, reliance basis, revalidation requirements, and non-claims.

This paper proposes **Accountable Handoff Interoperability** as a research hypothesis: that consequential exchanges between independently accountable systems require explicit handoff-state communication to reduce institutional inference risk. Fork is presented as one implementation case in AI-assisted workflows, not as proof of the general hypothesis.

The hypothesis is evaluated against adjacent traditions including anti-corruption layers in Domain-Driven Design, chain-of-custody doctrine, and trust-boundary modeling. It remains falsifiable: if independent implementations in other domains do not reproduce the proposed invariants — non-inheritance of authority, explicit claim scope, preserved non-claims, and recomputable handoff history — then the hypothesis should be revised or rejected.

---

## 8. Related Work Positioning

The position paper should explicitly stand beside existing architectural and evidentiary traditions.

### Domain-Driven Design / Anti-Corruption Layer

Anti-corruption layers isolate systems and translate between domain models so one model does not corrupt another. This is adjacent to Fork, but not identical. Fork’s emphasis is not merely semantic translation. Its focus is preserving claim scope, non-claims, authority context, and reliance basis at accountable handoffs.

### Chain of Custody

Chain of custody tracks the movement, handling, and safeguarding of evidence. Fork is related, but extends the concern beyond evidence objects alone. Fork applies custody-like discipline to claim movement, authority context, and reliance transitions in AI-assisted workflows.

### Trust Boundaries / Threat Modeling

Trust boundaries identify where trust levels change across systems or data flows. Fork’s adjacent claim is that governance and reliance boundaries also require explicit handoff-state records, not merely technical trust-zone controls.

This related-work section is important because it prevents the paper from sounding like it claims to invent boundaries, custody, or translation. The more disciplined claim is that Fork proposes a specific accountable-handoff pattern for claim, authority, and reliance movement.

---

## 9. Position-Paper Outline

### 1. Introduction: The Handoff Problem

Introduce the problem of independently accountable systems exchanging consequential state.

State the core thesis:

> Governance failures often arise not because either system is invalid internally, but because the handoff between systems is underspecified.

Introduce Fork as one concrete implementation case, not as proof of the broader theory.

---

### 2. Independently Accountable Systems

Define independently accountable systems as systems that retain their own authority, proof obligations, execution boundaries, governance constraints, or review responsibilities.

Examples include:

* runtime authority systems;
* governance systems;
* audit systems;
* procurement systems;
* legal review systems;
* AI-assisted workflow systems;
* evidence preservation systems.

The key point is that these systems may need to interoperate without collapsing their respective responsibilities.

---

### 3. Failure Mode: Unsupported Inheritance at Handoff

Define the central failure mode:

> Unsupported inheritance occurs when a downstream system treats claims, authority, reliance basis, or proof obligations as having transferred across a boundary when that transfer was never explicitly established.

Examples:

* A human-reviewed artifact is treated as legally sufficient.
* A runtime authorization is treated as compliance approval.
* A preserved evidence record is treated as proof of correctness.
* A governance policy reference is treated as proof that the policy was satisfied.
* An upstream claim is consumed downstream without preserving its exclusions or limitations.

---

### 4. Boundary-State Communication as a Pattern

Define boundary-state communication as an architectural pattern for making handoffs inspectable without creating a new authority surface.

The pattern should record:

* what crossed the boundary;
* what did not cross;
* what claim scope was preserved;
* what authority context applied;
* what evidence was referenced;
* what non-claims remained explicit;
* what required revalidation;
* what downstream consumption occurred.

The pattern must preserve adjacent responsibilities rather than collapse them.

---

### 5. Fork as an Implementation Case Study

Present Fork as one implementation of this pattern in AI-assisted institutional workflows.

Fork’s core artifact family includes:

* **Boundary Delta Records** — record what changed at the boundary.
* **Claim Boundary Contracts** — define claim scope and non-claims.
* **Claim Consumption Events** — record downstream reliance or consumption.
* **System Mapping Receipts** — preserve how systems were mapped during a handoff.
* **Reliance packets** — package the basis for later review.

Fork’s purpose is not to validate the endpoint. Its purpose is to preserve the handoff record.

---

### 6. Accountable Handoff Interoperability as a Research Hypothesis

State the broader hypothesis:

> Independently accountable systems require explicit handoff-state communication when exchanging consequential state.

Clarify that Fork does not prove this hypothesis. Fork provides one implementation case through which the hypothesis can be tested, refined, or falsified.

---

### 7. Invariants

Define the proposed invariants for accountable handoff systems:

1. **Non-inheritance of authority**
   Authority does not transfer merely because state, evidence, or output moved.

2. **Explicit claim scope**
   Claims must remain bounded to the scope in which they were made.

3. **Preserved non-claims**
   What was not established must remain visible downstream.

4. **Recomputable handoff history**
   Later reviewers should be able to verify that the handoff record has not changed.

5. **Revalidation visibility**
   The record should show what requires fresh justification or review.

6. **Separation of evidence and authority**
   Evidence preservation must not become authorization, compliance, or correctness.

---

### 8. Predictions and Falsification Paths

If Accountable Handoff Interoperability is a valid research hypothesis, then future work should find that:

1. Other domains independently encounter similar handoff-state ambiguity.
2. Explicit handoff-state records reduce ambiguity about claim scope and authority.
3. Different implementations preserve similar invariants despite using different representations.
4. Some domains may reject or modify the pattern, forcing refinement of the hypothesis.
5. If explicit handoff-state records do not improve reviewability or reduce inference risk, the hypothesis should be weakened or rejected.

Candidate test domains include:

* healthcare;
* finance;
* procurement;
* industrial control;
* legal review;
* insurance;
* public-sector AI governance;
* vendor risk management.

---

### 9. Conclusion

Fork should be presented as an engineering case study and experimental apparatus, not as the conclusion of the theory.

The strongest final framing is:

> Fork demonstrates one implementation of an accountable handoff pattern in AI-assisted workflows. Whether that pattern generalizes across independently accountable systems remains a falsifiable research hypothesis.

This posture preserves the strength of Fork while preventing the research framing from outrunning the evidence.
