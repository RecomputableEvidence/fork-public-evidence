# Fork Conversational Authority Drift Research Protocol v0.1

Status: `CANDIDATE_NOT_ADMITTED`

## 1. Purpose

This protocol defines a bounded method for examining claim-standing and source-role changes in AI-assisted exchanges. It is designed to preserve useful technical content while preventing contextual presence, repeated agreement, confident wording, or model self-critique from inheriting evidentiary standing they have not earned.

## 2. Unit of analysis

The unit of analysis is not an entire conversation. It is a tuple:

`<claim, actor, source span, source role, prior standing, asserted transition, supporting event, current disposition>`

A single exchange may contain supported findings, contradicted statements, unresolved interpretations, and useful proposals at the same time.

## 3. Source-role binding precedes claim classification

Before classifying any claim, the case must bind each supplied artifact to a declared role.

The following dimensions must remain distinct:

1. **Presence** — the artifact appears in the supplied bundle or visible interface.
2. **Byte access** — the reviewer can read or hash the artifact bytes.
3. **Parse access** — the reviewer can extract or inspect its content.
4. **Role understanding** — the reviewer correctly understands why the artifact was supplied.
5. **Technical validity** — claims inside the artifact are supported by implementation, execution, measurement, recomputation, or other declared evidence.

Presence does not establish validity. Byte access does not establish role understanding. Correctly finding one defect does not validate every other reviewer statement.

## 4. Standing vocabulary

This candidate uses the following bounded dispositions:

- `PRESENT_IN_SOURCE`
- `USER_DECLARED_ROLE`
- `ILLUSTRATED`
- `IMPLEMENTED_NOT_ESTABLISHED`
- `EXECUTED_NOT_ESTABLISHED`
- `REPORTED_EXECUTION`
- `SUPPORTED`
- `PARTIALLY_SUPPORTED`
- `CONTRADICTED`
- `INTERNALLY_CONFLICTING`
- `ROLE_MISCLASSIFIED`
- `UNRESOLVED`
- `OVERCLAIMED`

These values classify claims or observations. They are not a project-maturity ladder and do not replace Fork's existing artifact, admission, publication, or maturity vocabularies.

## 5. Transition rule

A claim may advance only when a discrete supporting event is identified. The following are not sufficient by themselves:

- contextual presence;
- repetition;
- citations without claim-level linkage;
- architectural plausibility;
- mocked values;
- commented-out execution;
- additional model agreement;
- self-diagnosis;
- rhetorical confidence;
- imported memory.

## 6. Correction rule

A correction is a new event. It does not erase the earlier statement.

A valid correction record should identify:

- the affected claim;
- the contrary source or event;
- the revised disposition;
- any descendants that relied on the earlier statement;
- remaining disagreement.

A reviewer that receives a source-role correction must either update the role map or preserve a reasoned disagreement. Continuing from the prior role assignment without either action is recorded as `CORRECTION_NOT_INTEGRATED`.

## 7. Cross-taxonomy rule

Similarity between two vocabularies does not establish equivalence. Before describing one as duplicative, the reviewer must compare:

- unit of analysis;
- transition event;
- authority effect;
- admission effect;
- recomputation meaning;
- whether the vocabulary applies to projects, artifacts, claims, or observations.

Absent that crosswalk, equivalence remains `UNRESOLVED`.

## 8. Reflexivity rule

Claims about Fork, the corpus, the reviewer, or the user's significance are subject to the same standing requirements as claims about the source system.

No actor receives an exemption for being the reviewer, repository maintainer, user, or model.

## 9. Public/private separation

Raw source artifacts may remain private. A public candidate may contain:

- opaque source identifiers;
- filenames;
- byte lengths;
- SHA-256 digests;
- user-declared source roles;
- bounded excerpts where disclosure is authorized;
- claim ledgers;
- transition records;
- findings and non-claims.

A digest establishes byte identity against a trusted reference. It does not establish authorship, truth, authority, completeness, or technical validity.

## 10. Adversarial review

A reviewer must be able to return any of:

- supported;
- partially supported;
- contradicted;
- unresolved;
- role misclassified;
- incorrectly accused.

Disagreement must remain visible rather than being collapsed into consensus.

## 11. No global inference

A case establishes only the bounded observations recorded for its exact source package. It does not establish prevalence, novelty, provider-wide behavior, user intent beyond the preserved record, or comparative importance.

## 12. Repository effects

This protocol:

- authorizes zero provider calls;
- does not modify `main`;
- does not affect Pair-001;
- does not promote readiness;
- does not constitute admission, publication, endorsement, or certification.
