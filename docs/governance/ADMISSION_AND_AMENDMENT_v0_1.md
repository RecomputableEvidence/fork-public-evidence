# Fork Admission and Amendment v0.1

## Status and purpose

This document defines a default repository procedure for distinguishing contribution submission, verification, review, merge, admission, publication, amendment, and supersession.

It applies only where a more specific frozen specification, experiment preregistration, package procedure, branch-specific admission rule, or artifact contract does not control.

This document does not itself admit any pull request, artifact, commit, branch, experiment result, reviewer, or release.

## Lifecycle distinctions

The following are separate repository events:

1. **Submission** — a candidate change is proposed.
2. **Verification** — declared checks are executed against an identified candidate.
3. **Review** — a reviewer records observations, findings, or a disposition.
4. **Merge** — Git history incorporates the candidate into a target branch.
5. **Admission** — a governing procedure grants defined repository standing to identified artifacts.
6. **Publication** — admitted or otherwise bounded material is exposed through a declared public surface.
7. **Release** — a versioned package or anchor is designated for a defined use or review surface.

No earlier event implies a later event unless an applicable governing procedure explicitly binds them.

In particular:

- successful local checks do not imply successful CI;
- successful CI does not imply substantive correctness;
- review does not imply independence unless independence is separately attributable;
- approval does not necessarily imply merge authority;
- merge does not necessarily imply admission;
- admission does not imply endorsement, certification, truth, compliance, legality, safety, authority transfer, production readiness, or experiment execution authority;
- publication does not broaden the claims or authority of the published artifact.

## Candidate identity

An admission decision must identify the candidate precisely enough to prevent mutable-reference substitution.

Where applicable, record:

- repository;
- target branch;
- base commit;
- candidate commit;
- candidate tree;
- merge base;
- exact merge commit;
- artifact paths and digests;
- governing specification or ruleset;
- verification tool and version;
- successful check or workflow run identifiers;
- review records required by the governing procedure.

Branch names, pull-request numbers, workflow names, and tags are useful references but are not substitutes for immutable object identity when exact identity is required.

## Admission scope

Admission must state what receives standing and what does not.

An admission record should identify:

- admitted artifacts;
- admitted versions;
- admitted relationships or transitions;
- effective branch or publication surface;
- applicable verification scope;
- exclusions;
- unresolved conditions;
- known residuals;
- superseded artifacts, if any;
- whether the record is append-only.

Admission of one artifact does not automatically admit sibling files, transitive dependencies, underlying claims, external source material, or later derivatives.

## Default admission prerequisites

Unless a more specific procedure controls, a C7 admission change should not be admitted until the following are recorded:

1. **Bounded candidate** — the exact candidate and affected artifacts are identified.
2. **Applicable classification** — the highest material change class is declared.
3. **Verification evidence** — required commands and checks have been executed against the identified candidate.
4. **Expected-result comparison** — observed results are compared with predetermined expectations.
5. **Boundary review** — claim, non-claim, authority, evidence-reference, unresolved-state, schema, and historical effects are addressed where applicable.
6. **Review disposition** — required reviewers have recorded their dispositions.
7. **Residual register** — known unresolved, untested, failed, or deferred conditions are preserved.
8. **Admission anchor** — an append-only or otherwise governed record identifies the admitted state.

A procedure may require additional prerequisites. A procedure may bind merge and admission together, but that binding must be explicit and attributable.

## Review dispositions

A review should use bounded language. Suggested default dispositions are:

- `READY_FOR_ADMISSION_REVIEW`
- `REVISION_REQUIRED`
- `INCONCLUSIVE_EVIDENCE_GAP`
- `INVALIDATED_BY_RECOMPUTATION`
- `VERIFIED_WITHIN_DECLARED_SCOPE`
- `NOT_APPLICABLE_TO_REVIEW_SCOPE`

These tokens do not have repository-wide normative force where another artifact defines different outcomes.

`VERIFIED_WITHIN_DECLARED_SCOPE` means only that the declared checks produced the declared result under the identified evidence and ruleset. It does not grant merge authority or establish independent human review.

## Independent review

Independent review is an attributable relationship, not a label created by a checker.

A review record presented as independent should identify:

- reviewer identity or permitted pseudonymous identifier;
- relationship to the contribution;
- prior authorship or material involvement;
- evidence and tools inspected;
- commands executed;
- environment and material limitations;
- findings and disposition;
- non-endorsement and authority limitations.

A machine verifier may support independent human review, but machine execution does not manufacture human independence.

## Historical preservation

Historical artifacts must remain distinguishable from later corrections and current-state projections.

When a historical artifact is defective, misleading, malformed, incomplete, or no longer current, the default procedure is:

1. preserve the original bytes or an exact sealed representation;
2. record the original identifier, path, commit, and digest where available;
3. state the defect without attributing unsupported motive;
4. add a corrective amendment, successor, or projection;
5. state the relationship between the original and later artifact;
6. recompute the current result under the identified procedure;
7. preserve any residual condition that remains unresolved.

Do not rewrite historical content solely to make the current repository appear internally clean.

## Amendment types

### Clarifying amendment

A clarifying amendment narrows ambiguity without changing the governed semantic result.

It must state:

- the ambiguous wording;
- the controlling interpretation;
- why prior conforming results remain valid;
- whether implementations or fixtures require change.

### Corrective amendment

A corrective amendment changes an erroneous rule, implementation binding, metadata field, relationship, or record.

It must state:

- the defect;
- the prior affected surface;
- the corrected surface;
- compatibility and historical consequences;
- whether prior results must be recomputed.

### Procedural amendment

A procedural amendment changes review, verification, admission, publication, or operational steps without silently changing the artifact’s substantive contract.

It must identify any effects on prior admissions or pending candidates.

### Superseding version

A superseding version replaces a prior version for future use while preserving the prior version’s historical standing.

It must identify:

- predecessor and successor;
- effective scope;
- migration rule;
- compatibility status;
- whether prior results remain interpretable under the predecessor ruleset.

### Current-state projection

A current-state projection describes present standing derived from historical records without modifying those records.

It must identify:

- source records;
- projection time or commit;
- transformation or selection rule;
- unresolved residuals;
- explicit non-retroactivity.

A current-state projection does not retroactively change what was true, recorded, admitted, unresolved, or observable at an earlier time.

## Append-only records

An append-only admission or publication register should add new entries rather than silently modifying prior entries.

A later entry may:

- correct a prior entry by reference;
- supersede a prior standing for future use;
- add a current-state projection;
- close or reclassify a residual with attributable evidence.

The prior entry should remain inspectable unless a separate security or privacy procedure requires restricted handling. Removal or redaction must itself be attributable and must not be represented as ordinary historical continuity.

## Merge methods and lineage

The governing procedure should identify the permitted merge method when exact lineage matters.

A merge commit preserves both parent lineages. A squash or rebase produces a different object relationship and must not be described as preserving the original commit topology.

An admission record should reference the actual resulting commit and not rely only on the pull-request head.

## Failed or partial admission

A candidate that fails verification, lacks evidence, or remains under review may still be preserved as a candidate or nonconformance record.

Preservation does not grant admission.

Where useful, preserve:

- candidate identity;
- failed commands or checks;
- observed outputs;
- missing evidence;
- reviewer disposition;
- next admissible action;
- explicit statement that no admission occurred.

A later successful candidate should reference the failed or superseded candidate when lineage is material.

## Experiment boundary

Experiment readiness, experiment execution, result classification, and result admission are separate states.

An instrumentation or readiness pull request must not imply provider execution authority. An execution record must not silently modify frozen controls. A result record must not become admitted merely because the execution workflow completed.

The experiment’s preregistration and execution-admission procedure control where they are more specific than this document.

## Required admission-record fields

A default admission record should include:

- record identifier and version;
- creation time or repository commit;
- candidate identity;
- target standing;
- change classification;
- governing artifacts;
- admitted artifact inventory;
- verification evidence;
- review evidence;
- exact observed outcome;
- residuals;
- exclusions and non-claims;
- resulting branch, release, or publication relationship;
- supersession or amendment relationships;
- append-only status.

## Non-claims

An admission or amendment record does not by itself establish:

- factual truth;
- source completeness;
- legal admissibility;
- compliance satisfaction;
- safety;
- security certification;
- decision correctness;
- production suitability;
- institutional authority;
- endorsement;
- reviewer independence;
- experiment execution authority;
- authority continuity from an upstream system.