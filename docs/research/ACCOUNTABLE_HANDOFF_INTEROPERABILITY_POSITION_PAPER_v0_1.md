# Accountable Handoff Interoperability

## Boundary-State Communication Between Independently Accountable Systems

### Fork as one implementation case in AI-assisted institutional workflows

## Status

This is a speculative position paper. It proposes a research hypothesis, not an established theory.

Fork is treated as one implementation case through which the hypothesis may be tested, refined, or falsified. Fork does not prove the hypothesis.

---

## Abstract

Independently accountable systems increasingly exchange consequential state across governance, execution, audit, procurement, legal, compliance, and AI-assisted workflow environments. These systems may remain valid within their own boundaries while still producing ambiguity at handoff: unclear claim scope, implied authority inheritance, uncertain reliance basis, missing revalidation requirements, and invisible non-claims.

This paper proposes **Accountable Handoff Interoperability** as a research hypothesis: consequential exchanges between independently accountable systems require explicit handoff-state communication to reduce institutional inference risk. The central failure mode is not merely that a system acted incorrectly, that evidence was missing, or that governance was insufficient. The deeper failure is that a downstream actor may infer more from a handoff than the upstream system actually established.

Fork is presented as one implementation case in AI-assisted institutional workflows. It preserves bounded handoff records that describe what was claimed, relied upon, excluded, changed, unresolved, or explicitly not transferred. It does not authorize execution, certify compliance, prove correctness, or replace institutional review.

The hypothesis remains unproven. It is falsifiable through independent implementations in other domains and through evaluation against shared invariants such as non-inheritance of authority, explicit claim scope, preserved non-claims, revalidation visibility, and recomputable handoff history.

---

## 1. Introduction

Modern institutions increasingly depend on systems that must interoperate while remaining separately accountable. A governance system may define policy. A runtime authority system may authorize execution. An AI system may generate analysis. A human reviewer may accept, narrow, reject, or modify that analysis. An audit system may preserve evidence. A procurement, legal, or compliance reviewer may later evaluate whether reliance was justified.

Each of these systems may be valid within its own boundary. The governance system may correctly state policy. The runtime system may correctly authorize a permitted action. The AI system may produce an artifact. The evidence system may preserve a record. The reviewer may act within assigned responsibility.

Yet failure can still emerge at the handoff between them.

The handoff may leave unclear what claim actually crossed the boundary, whether authority transferred, what assumptions survived, what required revalidation, what evidence supported reliance, and what must not be inferred downstream. In such cases, the failure is not necessarily internal to either system. It arises from underspecified handoff state.

This paper proposes that handoff state should be treated as a first-class governance object.

The claim is not that all systems require Fork. Nor is it that Fork proves a universal systems theory. The claim is narrower:

> Independently accountable systems may require explicit handoff-state communication when exchanging consequential state, because otherwise downstream actors can silently inherit claims, authority, reliance basis, or proof obligations that were never actually transferred.

Fork provides one implementation case of this idea in AI-assisted institutional workflows.

---

## 2. Limitations and Current Evidence

This paper advances a research hypothesis, not an established systems theory.

The current evidence base is limited in four important ways.

First, the implementation evidence comes primarily from Fork, a boundary-recording pattern developed for AI-assisted institutional workflows. Fork demonstrates one candidate implementation of accountable handoff recording, but it does not prove that the same pattern generalizes across domains, institutions, or technical architectures.

Second, the motivating convergence comes from a bounded set of reviewer and collaborator conversations involving AI governance, evidence preservation, runtime authority, procurement, audit, interoperability, and related institutional workflows. These conversations repeatedly identify the importance of preserving boundary separation between evidence, authority, execution, governance, and review. They should be treated as motivating evidence of a recurring concern, not as proof of a general architectural primitive.

Third, no independent non-Fork implementation of Accountable Handoff Interoperability has yet been evaluated. The hypothesis therefore remains open. It should be tested through independent implementations, adversarial handoff simulations, reviewer reconstruction exercises, and comparative workflow studies across domains such as healthcare, finance, procurement, legal review, insurance, industrial control, and public-sector AI governance.

Fourth, no controlled evaluation has yet established that explicit handoff-state records improve reviewer performance relative to ordinary logs, audit trails, chain-of-custody records, policy artifacts, or existing governance workflows. The proposed evaluation criteria in this paper should therefore be understood as research commitments, not demonstrated outcomes.

Accordingly, this paper makes a limited claim: Fork supports an engineering pattern and motivates a broader hypothesis. It does not establish that explicit handoff-state communication is universally required, superior to existing mechanisms, or sufficient for accountability by itself.

The hypothesis should be strengthened only if independent implementations preserve similar invariants and improve reviewability in practice. It should be narrowed if the pattern applies only to certain domains, risk tiers, or workflow types. It should be revised or rejected if simpler existing mechanisms prove sufficient, if handoff-state records fail to reduce institutional inference risk, or if they introduce more ambiguity than they resolve.

---

## 3. Core Hypothesis

The research hypothesis is:

> Consequential exchanges between independently accountable systems require explicit handoff-state communication to preserve accountability, reduce institutional inference risk, and prevent unsupported inheritance of claims, authority, reliance basis, or proof obligations.

This hypothesis can be weakened, refined, or rejected.

It would be strengthened if independent implementations in other domains reproduce similar invariants, such as explicit claim scope, preserved non-claims, authority non-inheritance, and recomputable handoff history.

It would be weakened if explicit handoff-state records do not materially improve reviewability, reduce ambiguity, or prevent unsupported downstream inference.

It would be rejected, or at least significantly narrowed, if the same problems can be solved more simply through existing logs, access controls, policy engines, audit trails, chain-of-custody practices, or anti-corruption layers without requiring a distinct handoff-state representation.

---

## 4. Definitions

### Independently Accountable System

An independently accountable system is any system, role, process, or institutional layer that retains responsibility for a class of decisions, claims, actions, evidence, or reviews.

Examples include:

* governance systems;
* runtime authority systems;
* execution systems;
* evidence-preservation systems;
* audit systems;
* legal review systems;
* procurement systems;
* compliance systems;
* AI-assisted workflow systems;
* human decision bodies.

The relevant feature is not whether the system is software. The relevant feature is whether it carries distinct accountability that should not silently collapse into another system's accountability.

### Consequential State

Consequential state is state that can affect institutional action, reliance, review, liability, compliance posture, authorization, or interpretation.

Examples include:

* a claim;
* a decision basis;
* a reviewer acceptance;
* an authority context;
* a compliance assertion;
* an evidence reference;
* a model-generated recommendation;
* a human modification;
* an unresolved assumption;
* a limitation or exclusion.

### Handoff State

Handoff state is the explicit representation of what changed, crossed, survived, failed, narrowed, expanded, or remained unresolved when consequential state moved between independently accountable systems.

It answers questions such as:

* What crossed the boundary?
* What did not cross?
* What claim scope was preserved?
* What authority context applied?
* What authority did not transfer?
* What evidence was referenced?
* What assumptions survived?
* What required revalidation?
* What non-claims remained explicit?
* What did the downstream system consume?
* What must not be inferred later?

### Institutional Inference Risk

Institutional inference risk is the risk that downstream actors infer more from a handoff than the upstream system established.

Examples include:

* treating human review as legal sufficiency;
* treating runtime authorization as compliance approval;
* treating preserved evidence as proof of correctness;
* treating policy attachment as proof that policy was satisfied;
* treating an upstream claim as broader than its original scope;
* treating an AI-generated artifact as institutionally reliable without preserving the basis for reliance.

---

## 5. Problem Statement

Many interoperability failures are treated as failures of logging, access control, policy enforcement, or auditability. Those may be real failures, but they do not exhaust the problem.

A log can show that an event occurred without preserving what the event was allowed to mean downstream.

An audit trail can show sequence without preserving claim scope.

A policy engine can show whether a rule fired without preserving how later actors relied on the result.

A chain-of-custody record can show evidence movement without preserving authority context or non-claims.

An API contract can specify data format without specifying institutional reliance boundaries.

The missing object is handoff state.

When handoff state is not explicit, downstream systems and reviewers may reconstruct meaning from surrounding context, institutional memory, dashboard labels, workflow position, or implied authority. That reconstruction may be wrong even when every individual system acted within its own boundary.

The consequence is unsupported inheritance.

Unsupported inheritance occurs when a downstream system treats some property as transferred even though the handoff did not explicitly establish that transfer.

The inherited property may be:

* authority;
* claim scope;
* legal sufficiency;
* compliance status;
* evidentiary weight;
* reviewer approval;
* methodological validity;
* execution safety;
* institutional intent.

This paper argues that unsupported inheritance is a recurring failure mode at the boundary between independently accountable systems.

---

## 6. Boundary-State Communication as an Architectural Pattern

Boundary-state communication is a candidate architectural pattern for making handoffs inspectable without collapsing adjacent responsibilities.

The pattern does not decide whether the upstream system was correct.

It does not decide whether the downstream system should rely.

It does not become the authority surface.

It records the handoff state so later actors can inspect what moved, what did not move, and what remained unresolved.

A boundary-state communication mechanism should preserve at least five classes of information.

First, it should preserve transferred claims. It should show which claims crossed the boundary and under what scope.

Second, it should preserve non-claims. It should show what was not established, what was out of scope, and what must not be inferred.

Third, it should preserve authority context. It should show what authority was exercised, by whom or by what system, for what purpose, and within what boundary. It should also show what authority did not transfer.

Fourth, it should preserve reliance basis. It should show what evidence, constraints, assumptions, or reviewer actions supported downstream reliance.

Fifth, it should preserve revalidation requirements. It should show what requires fresh review, new authority, additional evidence, or downstream justification.

The goal is not to make the handoff self-authorizing. The goal is to make the handoff inspectable.

---

## 7. Fork as an Implementation Case

Fork is one candidate implementation of boundary-state communication for AI-assisted institutional workflows.

In this setting, AI-generated or AI-assisted artifacts often move from draft or analysis into institutional reliance. The handoff may occur when a human reviewer accepts, modifies, cites, routes, submits, escalates, or incorporates an AI-assisted output into a workflow that can affect a decision.

Fork’s role is to preserve a bounded record of that movement.

It does not govern the model.

It does not decide whether the output is true.

It does not authorize execution.

It does not certify compliance.

It does not prove legal sufficiency.

It does not replace review.

It preserves the record needed for later review.

Fork’s artifact family can be understood as one implementation of accountable handoff recording:

**Boundary Delta Records** record what changed at the boundary.

**Claim Boundary Contracts** define claim scope, exclusions, and non-claims.

**Claim Consumption Events** record how a downstream actor or system consumed an upstream claim.

**System Mapping Receipts** preserve how systems, artifacts, or proof surfaces were mapped during a handoff.

**Reliance packets** package the evidence, authority context, claim scope, limitations, and unresolved issues needed for later reconstruction.

Together, these artifacts describe the transition rather than judging the endpoints.

Fork therefore provides an experimental apparatus for the broader hypothesis. It gives one concrete way to ask whether explicit handoff-state communication improves reviewability and reduces institutional inference risk.

But Fork does not prove Accountable Handoff Interoperability.

---

## 8. Non-Claims

This hypothesis depends on strict non-claim discipline.

Fork does not determine whether a decision was correct.

Fork does not authorize execution.

Fork does not certify compliance.

Fork does not prove institutional authority.

Fork does not replace governance, runtime authority, audit, legal review, procurement review, or compliance review.

Fork does not convert post-execution evidence into retrospective authorization.

Fork does not make an AI-generated artifact reliable merely by recording it.

Fork does not establish that downstream reliance was justified.

Fork preserves bounded handoff records so later reviewers can inspect what was claimed, relied upon, excluded, changed, unresolved, or explicitly not transferred.

The broader hypothesis carries the same discipline. Accountable Handoff Interoperability is not a theory of correctness, authority, compliance, or truth. It is a hypothesis about preserving accountability at transitions.

---

## 9. Related Work and Adjacent Concepts

Accountable Handoff Interoperability should be evaluated beside existing traditions, not presented as if it invents boundaries, custody, or translation.

### 8.1 Domain-Driven Design and Anti-Corruption Layers

In Domain-Driven Design, anti-corruption layers protect one domain model from being distorted by another. They translate between bounded contexts so that assumptions from one system do not corrupt another system’s model.

This is adjacent to Accountable Handoff Interoperability.

The difference is emphasis. Anti-corruption layers primarily address semantic and model translation. Accountable Handoff Interoperability focuses on claim scope, authority context, reliance basis, non-claims, and revalidation at accountable handoffs.

A handoff-state record may include translation, but it is not limited to translation. It asks what may legitimately be inferred after the translation occurs.

### 8.2 Chain of Custody

Chain of custody tracks the movement, handling, and safeguarding of evidence.

This is also adjacent.

The difference is that Accountable Handoff Interoperability applies custody-like discipline not only to evidence objects, but to claim movement, reliance basis, authority context, and institutional interpretation.

A chain-of-custody record may show that an object moved. A handoff-state record should also show what the movement did and did not establish.

### 8.3 Trust Boundaries and Threat Modeling

Trust-boundary modeling identifies points where data, control, or privilege crosses zones of differing trust.

This is closely related.

The difference is that Accountable Handoff Interoperability treats governance and reliance boundaries as first-class, not only technical trust zones. The question is not only whether data crossed a technical boundary safely. It is also whether institutional meaning crossed appropriately.

### 8.4 Audit Trails

Audit trails preserve sequences of events.

They are necessary but insufficient for the hypothesis advanced here.

A sequence of events may not show claim scope, authority exercised, non-claims, reliance basis, or revalidation requirements. Accountable handoff records should supplement audit trails by preserving the meaning and limits of the handoff.

---

## 10. Proposed Invariants

A system that claims to implement accountable handoff interoperability should preserve several invariants.

### 9.1 Non-Inheritance of Authority

Authority does not transfer merely because data, evidence, output, or state moved.

If authority is transferred, delegated, narrowed, or newly exercised, that transition must be explicit.

### 9.2 Explicit Claim Scope

Claims must remain bounded to the scope in which they were made.

A claim made for one purpose, environment, time window, workflow, or risk tier should not silently expand downstream.

### 9.3 Preserved Non-Claims

What was not established must remain visible.

Non-claims are not peripheral. They are part of the handoff state because they prevent downstream over-inference.

### 9.4 Revalidation Visibility

The record should show what requires fresh justification, review, evidence, or authority before downstream reliance expands.

### 9.5 Recomputable Handoff History

Later reviewers should be able to verify that the handoff record has not changed since sealing or preservation.

Recomputability does not prove correctness. It supports independent reconstruction.

### 9.6 Separation of Evidence and Authority

Evidence preservation must not become execution authorization, compliance certification, or correctness judgment.

### 9.7 Representation Independence

Different domains may implement handoff-state communication differently. The hypothesis predicts invariant preservation, not uniform representation.

---

## 11. Predictions

If Accountable Handoff Interoperability is a useful systems hypothesis, several predictions follow.

### Prediction 1: Similar Ambiguity Will Appear Across Domains

Healthcare, finance, procurement, industrial control, insurance, legal review, public-sector AI, and vendor risk workflows should independently encounter handoff-state ambiguity when multiple accountable systems interact.

The hypothesis does not require these domains to use the same terminology. It predicts that similar structural questions will recur:

* What moved?
* What did not move?
* What authority transferred?
* What required revalidation?
* What was relied upon?
* What must not be inferred?

### Prediction 2: Explicit Handoff Records Should Reduce Downstream Ambiguity

Workflows with explicit handoff-state records should reduce ambiguity about claim scope, authority, reliance basis, and revalidation requirements compared with workflows that exchange only artifacts, logs, or data.

This could be evaluated by measuring:

* time required to reconstruct reliance basis;
* frequency of disputes about what was authorized;
* frequency of disputes about what a record established;
* number of downstream assumptions later found unsupported;
* reviewer confidence in scope boundaries;
* ability to identify non-claims and unresolved issues.

### Prediction 3: Different Implementations Should Preserve Similar Invariants

Different domains may use different mechanisms: schemas, signed records, policy annotations, workflow receipts, case packets, review notes, or evidence bundles.

The hypothesis predicts that successful implementations should preserve similar invariants even if their representations differ.

### Prediction 4: Some Domains Will Force Refinement

The hypothesis should not assume universal fit.

Some domains may require additional invariants. Others may already solve the problem through mature doctrine or regulation. Some may show that handoff-state communication is unnecessary, too costly, or too ambiguous to operationalize.

Those findings should refine the hypothesis rather than be treated as exceptions to ignore.

### Prediction 5: Absence of Measurable Benefit Weakens the Hypothesis

If explicit handoff-state records do not improve reviewability, reduce inference risk, or clarify accountability, then the hypothesis should be weakened or rejected.

---

## 12. Evaluation Criteria

The hypothesis can be evaluated through domain-specific pilots, adversarial simulations, reviewer studies, and comparative workflow analysis.

A useful evaluation should ask:

1. Can reviewers identify what crossed the handoff boundary?

2. Can reviewers identify what did not cross?

3. Can reviewers distinguish evidence preservation from authorization?

4. Can reviewers distinguish claim scope from downstream inference?

5. Can reviewers identify whether reliance was preserved, narrowed, expanded, or newly justified?

6. Can reviewers reconstruct the basis for reliance without relying on institutional memory?

7. Can reviewers verify that the handoff record remained unchanged?

8. Can downstream actors avoid treating the record as correctness, compliance, or authority?

9. Does the mechanism reduce ambiguity compared with ordinary logs or artifacts?

10. Does the mechanism remain useful without absorbing the responsibilities of adjacent systems?

These criteria make the hypothesis testable.

---

## 13. Falsification Paths

A serious hypothesis must name what would count against it.

Accountable Handoff Interoperability would be weakened if:

* ordinary audit logs preserve sufficient handoff meaning without additional structure;
* existing chain-of-custody practices already capture claim scope, non-claims, authority context, and revalidation requirements;
* reviewers do not perform better with explicit handoff-state records;
* handoff-state records introduce more confusion than clarity;
* downstream actors still treat the records as implicit authorization despite non-claim discipline;
* implementations across domains fail to preserve common invariants;
* domain-specific costs exceed the governance value produced.

It would be substantially falsified if independent testing shows that explicit handoff-state communication does not reduce institutional inference risk or improve reconstruction of reliance basis compared with simpler existing mechanisms.

---

## 14. Research Program

The proposed research program has three tracks.

### Track 1: Fork as Implementation Case

Develop and test Fork Boundary Records in AI-assisted institutional workflows.

Candidate workflows include:

* AI-assisted vendor risk review;
* procurement recommendation drafting;
* policy memo generation;
* compliance note preparation;
* audit evidence assembly;
* legal intake summarization;
* grant review support;
* public-sector AI decision support.

The goal is to test whether Fork’s boundary records make handoffs more inspectable without becoming an authority layer.

### Track 2: Independent Domain Implementations

Invite implementations outside Fork’s immediate domain.

Candidate domains include:

* healthcare clinical review;
* insurance claims review;
* financial risk approval;
* aerospace safety evidence;
* industrial control handoffs;
* public procurement;
* legal review;
* regulated AI deployment.

The goal is not to copy Fork’s representation. The goal is to test whether similar invariants emerge.

### Track 3: Comparative Evaluation

Compare workflows with and without explicit handoff-state records.

Evaluation should include:

* reviewer reconstruction tasks;
* adversarial handoff simulations;
* ambiguity scoring;
* time-to-reconstruct measurements;
* error classification;
* downstream over-inference detection;
* comparison against ordinary logs, audit trails, and evidence bundles.

---

## 15. Discussion

The hypothesis is intentionally modest.

It does not say that Accountable Handoff Interoperability is always necessary. It does not say that Fork is the canonical implementation. It does not say that boundary records solve governance, compliance, authority, or correctness.

It says that a recurring class of failures may arise when consequential state moves between independently accountable systems without explicit handoff-state communication.

That is a narrower claim, but it is also more durable.

It allows Fork to be valuable without being universal. It allows other implementations to confirm, refine, or contradict the hypothesis. It allows reviewers to evaluate the pattern by its invariants rather than by attachment to a specific tool.

The strongest version of the thesis is therefore:

> Fork demonstrates one implementation of an accountable handoff pattern in AI-assisted workflows. Whether that pattern generalizes across independently accountable systems remains a falsifiable research hypothesis.

---

## 16. Conclusion

Independently accountable systems increasingly interoperate in institutional workflows. Each system may remain valid inside its own boundary while governance ambiguity emerges at the handoff between systems.

This paper proposes Accountable Handoff Interoperability as a research hypothesis: consequential exchanges between independently accountable systems may require explicit handoff-state communication to preserve accountability and reduce institutional inference risk.

Fork is one implementation case in AI-assisted institutional workflows. It preserves bounded records of what was claimed, relied upon, excluded, changed, unresolved, or explicitly not transferred. It does not prove correctness, authorize execution, certify compliance, or replace review.

The hypothesis remains open. It should be tested through independent implementations, adversarial simulations, and reviewer studies across domains where consequential state crosses accountable boundaries.

The central object of study is the handoff.

The central discipline is non-inheritance.

The central test is whether explicit handoff-state communication helps independent systems interoperate without silently exchanging authority, proof obligations, or unsupported claims.

---

## Short Form

Accountable Handoff Interoperability is the hypothesis that independently accountable systems require explicit handoff-state communication when exchanging consequential state.

Fork is one implementation case for AI-assisted institutional workflows.

The hypothesis is not proven.

It is testable through independent implementations and evaluation against shared invariants: non-inheritance of authority, explicit claim scope, preserved non-claims, revalidation visibility, separation of evidence and authority, and recomputable handoff history.
