# Fork Change Classification v0.1

## Status and purpose

This document classifies repository changes so that review, verification, and admission requirements are proportional to the surface being changed.

It governs change classification and review routing. It does not grant merge authority, admit an artifact, supersede a frozen specification, authorize experiment execution, or establish substantive correctness.

Where this document conflicts with a frozen specification, schema, experiment preregistration, admission procedure, or artifact-specific verification guide, the more specific governing artifact controls.

## Core rule

A pull request must be classified according to its highest-impact material change.

A pull request may contain lower-impact supporting edits, but it must not use an editorial or documentation label to conceal semantic, behavioral, historical, experimental, or admission effects.

When classification is genuinely unresolved, classify upward for review and record the uncertainty. Classification may be narrowed only after the reviewer can identify why the higher-impact requirements do not apply.

## Change classes

### C0 — Editorial

A C0 change alters presentation without changing meaning, behavior, evidence standing, verification scope, or historical interpretation.

Examples:

- spelling, punctuation, or broken-link repair;
- whitespace or formatting correction;
- non-semantic reflow;
- comment cleanup that does not change a declared contract;
- path correction where the referenced artifact is unchanged.

C0 must not change normative terms, examples that function as fixtures, executable commands, expected outcomes, classifications, findings, digests, record identifiers, or authority boundaries.

Minimum evidence:

- concise description of the editorial correction;
- diff inspection;
- targeted link or formatting check where applicable;
- explicit statement that no semantic or behavioral boundary changed.

### C1 — Explanatory documentation or non-canonical example

A C1 change adds or revises explanatory material that is not itself a normative contract, canonical fixture, admitted record, or experiment control.

Examples:

- contributor guidance;
- reviewer orientation;
- architectural explanation;
- non-canonical worked example;
- navigation or cross-reference documentation.

Minimum evidence:

- identified scope and intended audience;
- boundary-impact statement;
- link and command review where applicable;
- confirmation that the text does not silently redefine a governed artifact.

If a document introduces new mandatory requirements, changes the meaning of a normative term, or controls verification behavior, it is not C1.

### C2 — Implementation or verification logic

A C2 change alters executable behavior without changing the declared schema or normative contract.

Examples:

- parser or checker implementation repair;
- deterministic output correction;
- CI workflow logic;
- command wrapper;
- report generation;
- validation performance improvement that preserves results.

Minimum evidence:

- exact verification commands;
- expected outputs or exit status;
- tests for intended behavior and relevant failure behavior;
- regression results;
- statement identifying the governing contract;
- confirmation that the implementation does not emit conclusions beyond that contract.

If the change alters accepted input, output meaning, finding precedence, classification behavior, authority standing, or schema semantics, classify it as C3 or higher.

### C3 — Schema, contract, or normative rule

A C3 change alters a structural contract or normative meaning.

Examples:

- schema evolution;
- enumeration or required-field change;
- finding-code registration;
- classification precedence;
- canonicalization or seal-scope rule;
- explicit authority or non-claim boundary;
- versioned interface contract.

Minimum evidence:

- governing artifact and version;
- classification as normative, clarifying, corrective, or editorial;
- exact semantic delta;
- affected schemas, tools, fixtures, and documentation;
- valid and invalid test cases where applicable;
- compatibility and migration analysis;
- statement of whether historical results remain valid under their original ruleset.

An existing released version must not be semantically rewritten in place when an amendment or successor version is required.

### C4 — Canonical fixture, registry, receipt, manifest, or public evidence record

A C4 change creates or alters an artifact whose bytes, identifiers, relationships, or standing are intended to be relied upon by later recomputation or review.

Examples:

- canonical or adversarial fixture;
- participant or experiment registry entry;
- generated receipt committed as evidence;
- checksum manifest;
- public evidence packet;
- current-state projection tied to historical records.

Minimum evidence:

- artifact class and governing ruleset;
- source and generation procedure;
- exact verification command;
- expected result;
- provenance and attribution fields required by the artifact;
- mutability status;
- relationship to prior or superseded records;
- confirmation that generated artifacts were not manually edited unless the format permits manual authorship.

A passing checker establishes only the checker’s declared structural result. It does not establish truth, compliance, legality, authority, endorsement, or production readiness.

### C5 — Experiment instrumentation, preregistration, or execution

A C5 change affects an experiment’s controls, execution surface, raw evidence capture, stopping rule, receiver binding, corpus, prompts, parameters, or result formation.

Examples:

- preregistration;
- frozen corpus or prompt packet;
- instrumentation change;
- experiment-run workflow;
- raw provider-output capture;
- classification of experimental results.

Minimum evidence:

- experiment identifier and phase;
- frozen versus mutable elements;
- optimization and intervention constraints;
- instrumentation lineage;
- execution authority state;
- raw evidence handling;
- predetermined classification and stopping rules;
- independent review requirements declared by the experiment.

Instrumentation changes and experiment execution should not be mixed when the instrumentation change could affect the result. Passing readiness checks does not authorize execution.

### C6 — Historical correction, amendment, recovery, or supersession

A C6 change addresses a malformed, incomplete, misleading, or obsolete historical artifact without erasing its prior state.

Examples:

- sealed malformed-content record;
- corrective amendment;
- historical regression repair;
- superseding artifact;
- current-state projection derived from an unchanged historical record;
- repository recovery lineage.

Minimum evidence:

- exact historical artifact and originating commit or record identifier;
- preserved original bytes or sealed representation;
- defect statement;
- corrective or superseding artifact;
- explicit relationship between historical and current state;
- recomputation procedure;
- non-retroactivity statement where applicable.

Historical records must not be rewritten merely to make the present state appear clean. A correction must not manufacture retroactive authority, validation, or execution state.

### C7 — Admission, publication, release anchor, or canonical-state transition

A C7 change records a repository-level standing transition.

Examples:

- admission anchor;
- release anchor;
- canonical-state update;
- publication-phase transition;
- append-only record that identifies admitted pull requests or exact merge commits;
- supersession declaration with repository-wide effect.

Minimum evidence:

- exact candidate commit and tree where applicable;
- exact base and merge relationship;
- required reviews and checks;
- admitted artifact inventory;
- resulting standing and effective scope;
- exclusions and non-claims;
- append-only or supersession behavior;
- independently recomputed package or verification result when required by the admission procedure.

Submission, successful CI, review, merge, admission, publication, and release are separate events unless a governing procedure explicitly binds them.

## Mixed changes

A pull request should contain one material change class whenever practical.

The following combinations should normally be separated:

- C0 formatting with C2 or C3 behavior;
- C3 schema change with unrelated documentation cleanup;
- C5 instrumentation with experiment execution;
- C6 historical repair with new feature development;
- C7 admission with candidate implementation changes.

A mixed pull request must explain why separation would destroy necessary atomicity. Convenience alone is not sufficient.

## Required classification declaration

Every pull request must declare:

- primary change class;
- any secondary classes;
- governing artifact or ruleset;
- affected artifact classes;
- boundary impact;
- historical impact;
- verification commands and expected result;
- known untested or unresolved conditions.

## Review routing

C0 and C1 may use ordinary repository review unless a specific artifact says otherwise.

C2 requires implementation-focused review and executable evidence.

C3 and C4 require contract or evidence-surface review proportionate to their effect.

C5 requires the experiment’s declared review and execution controls.

C6 requires historical-preservation review.

C7 requires the repository’s admission or publication procedure and must not be inferred from ordinary pull-request approval.

## Classification non-claims

A change classification does not establish:

- that the change is correct;
- that the change should merge;
- that the artifact is admitted;
- that a reviewer is independent;
- that an experiment may execute;
- that a result is true, compliant, safe, legal, authoritative, or production-ready.