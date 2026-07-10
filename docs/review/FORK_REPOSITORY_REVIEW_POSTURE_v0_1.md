# Fork Repository Review Posture v0.1

Status: Review posture / repository-specific contribution guide.  
Normative force: Maintainer guidance, not external certification.  
Scope: Public Fork repository artifacts, review comments, exterior observations, recomputation receipts, and pull-request history.  
Access classification: Public repository review guidance.  
Review use: Contributor guidance, maintainer review aid, exterior-observation interpretation aid.

## Non-endorsement and non-claims capsule

This document does not endorse Fork, certify Fork, validate production readiness, establish legal sufficiency, establish compliance, approve deployment, or convert any exterior observation into endorsement.

This document is an internal repository-review posture. It codifies how maintainers, contributors, and reviewers should evaluate Fork artifacts without upgrading evidence, recomputation, observations, or structural verification into authority, correctness, compliance, sufficiency, approval, or certification.

## Purpose

Fork preserves evidence boundaries for AI-assisted workflows.

This review posture explains how contributions should be interpreted and evaluated so that the repository remains consistent with its central architectural constraint:

> Preserve evidence, claims, non-claims, transitions, reliance, and reconstruction paths without inheriting or creating authority.

Fork review is therefore not primarily about whether a contribution is useful in the abstract. It is about whether the contribution makes a boundary, claim, transition, observation, receipt, or verification surface more inspectable without expanding what Fork is allowed to mean.

## Governing review principle

A Fork contribution is acceptable only if it preserves or clarifies evidence boundaries without converting them into truth, legal sufficiency, compliance, approval, safety, production readiness, institutional authority, or downstream reliance justification.

A reviewer should ask:

1. What is being preserved?
2. What is being claimed?
3. What is explicitly not being claimed?
4. What authority is referenced?
5. What authority is not transferred?
6. What can be independently recomputed or inspected?
7. What remains unresolved?
8. What downstream inference is prohibited?

If those questions cannot be answered from the artifact, the contribution needs clarification before merge.

## 1. Architecture

Fork architecture should remain out-of-band, read-only, evidentiary, and non-authoritative.

New modules should fit within the existing review grammar of evidence boundary, transition, reliance, interoperability, simulation, exterior observation, recomputation, or commercial orientation.

### Review criteria

A contribution should:

- preserve evidence rather than decide policy;
- clarify authority boundaries rather than absorb authority;
- distinguish runtime governance from post-execution accountability;
- preserve what crossed a boundary and what did not;
- preserve unresolved state rather than forcing artificial closure;
- avoid becoming a workflow controller, legal engine, compliance oracle, audit certifier, or production-readiness signal.

### Architectural blockers

A contribution should be rejected or revised if it causes Fork to:

- authorize execution;
- certify a decision;
- validate an upstream governance system;
- approve downstream reliance;
- imply compliance sufficiency;
- imply legal sufficiency;
- imply factual truth;
- act as a runtime control plane;
- convert structural verification into institutional approval.

## 2. Claim boundaries and non-claims

Every artifact should make its claim scope and non-claims explicit.

Fork artifacts should not rely on reader restraint. They should actively prevent foreseeable misreadings.

### Review criteria

A contribution should state:

- the bounded claim being made;
- the evidence being preserved;
- the verification or recomputation surface, if any;
- the non-claims;
- the downstream no-inference rule;
- any unresolved state;
- any authority reference;
- whether authority is absent, external, retained upstream, or explicitly not transferred.

### Claim-boundary blockers

A contribution should be revised if it implies:

- evidence equals approval;
- recomputation equals correctness;
- verification equals truth;
- observation equals endorsement;
- policy reference equals compliance;
- structural pass equals legal sufficiency;
- packet inclusion equals evidentiary sufficiency;
- downstream reliance is justified merely because a record exists.

## 3. Correctness

Correctness in Fork is structural unless another bounded meaning is explicitly declared.

A checker may verify schema conformance, hash stability, fixture behavior, canonicalization, receipt integrity, or boundary-rule behavior. It must not be framed as proving the underlying event, AI output, human decision, legal conclusion, compliance status, safety state, or governance adequacy.

### Review criteria

A contribution should distinguish:

- artifact correctness;
- checker correctness;
- receipt correctness;
- recomputation correctness;
- interpretive correctness.

The phrase "pass" should always be scoped. For example, "STRUCTURAL_PASS" is acceptable only when the artifact makes clear that it does not establish truth, sufficiency, approval, compliance, production readiness, or legal effect.

## 4. Testing and recomputation

Invalid examples are first-class artifacts in Fork.

Boundary infrastructure is not adequately reviewed by happy-path fixtures alone.

### Review criteria

A contribution should include, where applicable:

- valid fixtures;
- invalid fixtures;
- explicit expected failures;
- failure classifications;
- deterministic commands;
- recomputation instructions;
- receipt outputs;
- checksum or hash evidence;
- regression examples for previously observed failure modes;
- clear interpretation of what a passing result means and does not mean.

### Testing blockers

A contribution should be revised if:

- it only tests valid cases;
- it silently absorbs failure;
- it does not name the boundary being tested;
- it makes structural reproduction look like truth;
- it requires undisclosed local context to reproduce;
- it cannot be recomputed by a reviewer using the documented path.

## 5. Security and adversarial review

Fork security includes evidence-boundary security.

The primary risks include authority laundering, endorsement injection, source contamination, retrieval distortion, semantic paraphrase bypass, non-claim suppression, and conversion of observations into proof.

### Review criteria

A contribution should be evaluated for whether it resists:

- failed retrieval being treated as observation;
- exterior commentary being treated as endorsement;
- observation volume being treated as consensus;
- semantic paraphrase being used to bypass prohibited claims;
- structural verification being treated as compliance;
- evidence preservation being treated as approval;
- authority references being treated as authority transfer.

### Security blockers

A contribution should be revised if it allows ambiguous observational, recomputation, or reviewer material to appear as certification, validation, approval, consensus, production readiness, legal sufficiency, or compliance sufficiency.

## 6. Boundary Pressure Review

Boundary Pressure Review evaluates whether a Fork artifact preserves its declared claim, authority, evidence, non-claim, sufficiency, and truth boundaries under adverse interpretation.

This includes pressure from:

- failed retrieval;
- partial access;
- downstream reliance;
- semantic paraphrase;
- stakeholder pressure;
- reviewer overreading;
- model-generated synthesis;
- authority-adjacent language;
- exterior observations;
- packet inclusion;
- commercial framing.

### Boundary Pressure Review acceptance rule

A Fork artifact passes Boundary Pressure Review only if the following remain distinguishable under pressure:

- structural reproduction;
- unresolved state;
- evidentiary sufficiency;
- factual truth;
- authority;
- compliance;
- legal sufficiency;
- approval;
- endorsement;
- production readiness.

### Boundary Pressure Review failure modes

A contribution should be revised if it allows any of the following collapses:

- structural pass becomes correctness;
- recomputation becomes validation;
- evidence reference becomes approval;
- observation becomes endorsement;
- artifact inclusion becomes sufficiency;
- policy reference becomes compliance;
- authority context becomes authority transfer;
- reviewer receipt becomes certification;
- commercial orientation becomes deployment readiness.

## 7. Documentation

Documentation is part of Fork's control surface.

A documentation artifact can create architectural drift if it overstates what the technical artifact supports.

### Review criteria

A documentation contribution should:

- identify its audience;
- identify its review surface;
- state non-claims;
- link to the smallest supporting artifact;
- avoid broad repo-level support claims;
- distinguish research, review, pilot discovery, commercial orientation, and production claims;
- include recomputation or verification commands where applicable;
- avoid implying certification, approval, legal sufficiency, compliance sufficiency, safety, or deployment readiness.

### Documentation blockers

A documentation contribution should be revised if it:

- treats the whole repo as a single proof surface;
- cites exterior observations as endorsements;
- treats buyer-facing material as procurement proof;
- treats reviewer material as validation;
- omits non-claims where overreading is foreseeable.

## 8. Exterior observations

Exterior observations are preserved observations. They are not endorsements, certifications, validations, or authority sources.

### Review criteria

An exterior-observation artifact should preserve:

- who or what observed;
- what was requested;
- what was actually accessed;
- whether execution occurred;
- what limitations applied;
- what failed or remained inaccessible;
- what was inferred, if anything;
- what was not evaluated;
- how the observation may be used;
- how the observation must not be used.

### Exterior-observation blockers

An exterior-observation contribution should be revised if it:

- hides access limitations;
- treats failed retrieval as successful review;
- treats commentary as execution;
- treats model output as authority;
- treats observation count as consensus;
- removes non-endorsement language;
- allows a reader to infer approval or certification.

## 9. Commercial and pilot-language review

Commercial and pilot artifacts are orientation surfaces. They should not imply procurement readiness, legal readiness, compliance coverage, deployment completeness, or client suitability.

### Review criteria

Commercial-facing language should prefer:

- "supports reconstruction" over "proves compliance";
- "preserves evidence" over "validates decisions";
- "pilot-discovery ready" over "production-ready";
- "may help reviewers inspect" over "satisfies audit";
- "bounded evidence surface" over "governance solution";
- "post-execution accountability" over "runtime authorization."

### Commercial-language blockers

A commercial or pilot contribution should be revised if it implies:

- finalized pricing;
- procurement sufficiency;
- compliance coverage;
- production deployment readiness;
- legal defensibility as a conclusion;
- replacement of existing governance systems;
- authority over customer decision-making.

## 10. Code style, portability, and readability

Fork favors deterministic, reviewable, text-first artifacts.

### Review criteria

A contribution should prefer:

- stable filenames;
- versioned paths;
- UTF-8 text;
- LF line endings;
- deterministic output;
- minimal dependencies;
- standard-library verification where feasible;
- PowerShell 5.1-compatible scripts where Windows execution is expected;
- commands that can be copied and run by independent reviewers.

### Portability blockers

A contribution should be revised if it:

- depends on undisclosed local state;
- requires the original author to interpret;
- produces non-deterministic artifacts without explanation;
- creates encoding or line-ending instability;
- breaks documented reviewer commands;
- relies on hidden tooling where a simple verifier would suffice.

## 11. Performance

Performance is not the primary historical review concern of this repository.

Performance improvements are welcome only when they do not reduce inspectability, determinism, portability, or claim clarity.

### Review criteria

A performance-oriented change should preserve:

- deterministic behavior;
- inspectable outputs;
- fixture clarity;
- reproducible commands;
- bounded interpretation of results.

A faster verifier that is harder to inspect is not automatically better.

## 12. Policy gaps needing clarification

The following areas require formal policy before the project scales.

### Semantic classification severity

Fork needs clearer rules for when a semantic-classification finding is a blocker, warning, limitation, or future-work item.

### Observation volume versus evidentiary weight

Fork needs a standard roll-up disclaimer stating that observation volume is not consensus, endorsement, validation, audit rigor, or certification.

### Directory-level review surfaces

Fork should label directories as canonical, experimental, archived, commercial, reviewer-facing, recomputation, exterior-observation, or support material.

### Recomputability versus sufficiency

Receipts, checkers, and test outputs should carry a standard interpretation footer explaining that recomputation does not establish truth, authority, approval, legal sufficiency, compliance, or production readiness.

### Formal review tiers

Fork should define when a change requires:

- maintainer review only;
- CI/checker pass;
- recomputation receipt;
- external reviewer execution;
- boundary-pressure review;
- policy clarification before merge.

## Contributor and reviewer checklist

Before approving a Fork contribution, confirm:

1. The change preserves evidence without inheriting authority.
2. Claims and non-claims are explicit.
3. Verification language is bounded to structural or integrity meaning.
4. Valid and invalid fixtures are present where applicable.
5. Failure modes are named rather than silently absorbed.
6. Documentation cites the smallest supporting artifact.
7. Public, experimental, commercial, and reviewer-facing surfaces are not conflated.
8. Exterior observations remain observations, not endorsements.
9. Encoding, line endings, paths, and commands are portable.
10. Buyer-facing language does not imply production, legal, compliance, audit, safety, or procurement sufficiency.
11. Structural reproduction, unresolved state, evidentiary sufficiency, authority, compliance, truth, approval, and endorsement remain distinguishable under pressure.

## Closing posture

Fork review is a boundary discipline.

The review question is not only whether an artifact works. The review question is whether the artifact can be inspected, recomputed, cited, and reused later without allowing preserved evidence to become inherited authority.

<!-- FORK_BOUNDARY_PRESSURE_RETRIEVAL_DISTORTION_CASE:START -->

## Boundary Pressure Review / Retrieval Distortion Test Case

A first Boundary Pressure Review test case is maintained here:

- [Boundary Pressure Review / Retrieval Distortion Test Case v0.1](boundary-pressure/BOUNDARY_PRESSURE_RETRIEVAL_DISTORTION_TEST_CASE_v0_1.md)

The case evaluates whether failed retrieval, partial access, commentary, observation, recomputation, structural reproduction, approval, endorsement, compliance, legal sufficiency, and truth remain distinguishable under pressure.

Run the checker from repo root:

    python .\tools\check_boundary_pressure_review_cases_v0_1.py

<!-- FORK_BOUNDARY_PRESSURE_RETRIEVAL_DISTORTION_CASE:END -->

<!-- FORK_BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_REVIEW_POSTURE:START -->

Boundary Pressure: Recomputation Receipt Overread
A recomputation receipt is not authority.
A receipt may show that a bounded replay or checker execution occurred and produced a particular structural result. It does not validate the underlying artifact, replace missing source evidence, establish legal sufficiency, establish compliance, prove truth, approve a decision, establish safety, or demonstrate production readiness.
The recomputation receipt overread case tests this pressure directly by preserving one valid fixture where the receipt remains structural evidence and one invalid fixture where the receipt is upgraded into validation or authority.

<!-- FORK_BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_REVIEW_POSTURE:END -->
