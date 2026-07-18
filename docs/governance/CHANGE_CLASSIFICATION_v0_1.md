# Fork Change Classification v0.1

Status: Repository contribution procedure.  
Normative force: Maintainer-governed classification and review requirements for public repository changes.  
Scope: Pull requests, direct commits, amendments, admission acts, and publication changes in `fork-public-evidence`.  
Non-claim: Classification does not certify correctness, safety, compliance, legal sufficiency, production readiness, or authority.

## Purpose

This procedure distinguishes ordinary repository changes from changes that affect contracts, canonical evidence, experiments, history, admission, or publication.

Its purpose is to keep the common contribution path usable while preventing exceptional changes from being mistaken for ordinary ones.

## Controlling rule

Assign every change the highest applicable class.

A lower class may not be used to avoid the evidence, review, or separation requirements of a higher class. Mixed-class pull requests should be separated when the classes create materially different review or admission obligations.

A file path alone does not determine the class. Classification follows the semantic and procedural effect of the change.

## Classes

### E0 — Editorial

No intended semantic, behavioral, evidentiary, historical, or authority effect.

Examples:

- spelling or grammar correction;
- broken-link repair;
- formatting or whitespace repair;
- non-semantic comment clarification;
- navigation-only documentation changes.

Minimum requirements:

- identify why the change is non-semantic;
- inspect the diff for accidental meaning changes;
- run any repository check that validates the affected documentation or workflow syntax;
- state that claim, non-claim, authority, schema, classification, experiment, and historical standing are unchanged.

Escalate when wording changes a requirement, interpretation boundary, declared claim, non-claim, expected result, or artifact standing.

### I1 — Implementation

Changes executable behavior without intentionally changing the governing contract.

Examples:

- checker or parser repair;
- workflow implementation change;
- deterministic-output repair;
- portability improvement;
- performance improvement that preserves behavior;
- tooling or test-harness change.

Minimum requirements:

- identify the governing contract;
- provide conforming and failing coverage where applicable;
- include regression coverage for repaired defects;
- run the affected component checks;
- explain why the implementation remains within the existing semantic boundary.

Escalate when the implementation requires new fields, findings, enums, precedence, classifications, or normative interpretation.

### S2 — Schema or Contract

Changes a structural contract or the meaning of a governed field, rule, finding, enum, precedence order, or verification outcome.

Examples:

- schema field addition or removal;
- validation-rule change;
- finding-code registration;
- classification-precedence change;
- canonicalization-rule change;
- normative specification amendment;
- change to what a pass, failure, or unresolved result means.

Minimum requirements:

- identify the affected versioned contract;
- state whether the change is additive, corrective, clarifying, breaking, or superseding;
- enumerate affected schemas, tools, fixtures, documentation, and consumers;
- include valid and invalid fixtures;
- document compatibility and migration behavior;
- obtain heightened maintainer review;
- avoid changing the meaning of a published version in place when a new version or explicit amendment is required.

### C3 — Canonical Fixture or Registry

Changes controlled data used as canonical input, expected output, registered state, participant state, or experiment metadata.

Examples:

- canonical fixture changes;
- findings registry changes;
- participant profile registry entries;
- experiment registry records;
- canonical expectation updates;
- controlled example admission.

Minimum requirements:

- identify the registry, fixture set, or controlling schema;
- state whether the record is new, corrected, superseding, or projected;
- run the governing checker;
- preserve prior admitted records unless an amendment procedure applies;
- document effect on prior test results and downstream references;
- obtain review independent of the record author when the governing procedure requires it.

A canonical fixture must not be edited merely to make an implementation pass.

### X4 — Experiment or Receipt

Changes experiment instrumentation, execution inputs, raw outputs, receipts, result records, or recomputation evidence.

Examples:

- experiment preregistration;
- instrumentation change;
- experiment run;
- raw evidence capture;
- recomputation receipt;
- result classification;
- exterior verification record.

Minimum requirements:

- identify whether the change concerns design, instrumentation, execution, review, or publication;
- preserve the distinction between preregistration and post-result interpretation;
- keep instrumentation changes separate from execution when changing the instrumentation could affect the result;
- preserve raw outputs and execution coordinates where required;
- state what was and was not executed, observed, or recomputed;
- preserve non-endorsement and authority limitations;
- obtain independent review when required by the experiment or admission procedure.

A receipt records a bounded execution or observation. It is not authority, truth, certification, or endorsement.

### H5 — Historical Correction

Corrects, supersedes, seals, annotates, or projects from a previously published, admitted, frozen, or relied-upon artifact.

Examples:

- malformed historical record repair;
- defect record;
- superseding artifact;
- sealed-original preservation;
- current-state projection;
- lineage correction;
- correction of a published PR or release reference.

Minimum requirements:

- preserve the original artifact or its sealed representation;
- identify exact defect coordinates and originating lineage when known;
- add an append-only correction, supersession, or projection record;
- state whether prior conclusions remain valid, become limited, or require recomputation;
- avoid presenting current state as historical state;
- obtain independent review before admission when the correction affects a canonical or published record.

The detailed procedure is defined in [`ADMISSION_AND_AMENDMENT_v0_1.md`](ADMISSION_AND_AMENDMENT_v0_1.md).

### A6 — Admission or Publication

Explicitly admits, freezes, anchors, releases, or publishes an artifact or collection.

Examples:

- admission anchor;
- publication manifest;
- release freeze;
- canonical corpus admission;
- publication-phase update;
- release checksum or instrumentation anchor.

Minimum requirements:

- identify the exact artifacts and commit or content digests being admitted;
- record successful required checks with exact run or receipt references;
- distinguish verification from endorsement and certification;
- preserve unresolved conditions and residuals;
- state the admission scope and exclusions;
- use an append-only admission or publication record;
- keep implementation and admission separate unless the governing procedure expressly permits a combined act.

Merge alone is not an A6 admission event unless a controlling procedure explicitly defines it as one.

## Review matrix

| Class | Typical review | Verification evidence | Separate admission act |
|---|---|---|---|
| E0 | Maintainer or delegated review | Diff inspection and applicable syntax/link check | No |
| I1 | Maintainer technical review | Component tests and regression evidence | Usually no |
| S2 | Heightened contract review | Contract tests, valid/invalid fixtures, compatibility analysis | When canonical or frozen |
| C3 | Controlled-record review | Governing checker and lineage review | Often |
| X4 | Experiment or receipt review | Execution coordinates, raw evidence, recomputation record | When results are published or canonical |
| H5 | Historical amendment review | Original preservation, defect record, correction verification | Yes when the affected record was admitted or published |
| A6 | Admission/publication review | Exact commit or digest anchors and required successful checks | This class is the admission act |

The matrix defines default expectations. A more specific specification, experiment preregistration, registry procedure, or publication contract may impose stronger requirements.

## Classification questions

Before submitting, answer:

1. Does the change alter meaning or only presentation?
2. Does executable behavior change?
3. Does a schema, rule, finding, enum, precedence, or outcome meaning change?
4. Does controlled or canonical data change?
5. Does the change design, execute, record, or interpret an experiment?
6. Does it modify the standing of a historical or published artifact?
7. Does it explicitly admit, freeze, anchor, release, or publish anything?

The highest “yes” determines the minimum class.

## Non-equivalence rule

Passing the review requirements for one class does not satisfy another class by implication.

In particular:

- CI success does not equal admission;
- merge does not equal publication;
- recomputation does not equal correctness;
- independent review does not equal endorsement;
- a current-state projection does not rewrite historical state;
- a documentation label does not change an artifact's governed standing.
