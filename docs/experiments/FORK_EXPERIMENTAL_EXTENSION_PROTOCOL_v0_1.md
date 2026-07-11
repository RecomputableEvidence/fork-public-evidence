# Fork Experimental Extension Protocol v0.1

Status: governed experimental-admission protocol  
Classification: process and evidence-boundary protocol; not an experiment result  
Version: v0.1

## 1. Purpose

This protocol governs the transition from exterior observation into controlled Fork-instrumented experiments.

It applies Fork's own boundary discipline to Fork's experiments. An experiment may not silently inherit authority, truth, approval, sufficiency, or production-readiness claims from architecture documents, external reviews, preserved receipts, or successful structural verification.

The governed transition is:

```text
exterior observation
-> admitted failure classes
-> preregistration
-> frozen corpus and receiver configuration
-> preserved receiver execution
-> independent classification
-> bounded synthesis
-> independent recomputation
-> optimization eligibility
```

## 2. Normative hierarchy

The following hierarchy applies:

1. **Experimental Extension Protocol** — governs whether and how an experiment may begin.
2. **Preregistration** — governs the hypothesis, variables, units, corpus, planned analyses, exclusions, and amendment policy.
3. **Experiment Manifest** — binds the concrete scenarios, conditions, receiver classes, versions, schemas, and checker identities.
4. **Run Records** — preserve what was presented to a receiver and what the receiver emitted.
5. **Classification Records** — preserve how a raw receiver output was evaluated.
6. **Receipts** — preserve bounded execution or recomputation observations.
7. **Synthesis** — interprets preserved records without rewriting them.

A README, buyer document, review summary, or synthesis may summarize a preregistered claim but must not broaden it.

## 3. Admission prerequisites

A baseline experiment is admitted only when all applicable conditions are satisfied:

- the canonical proof-surface state file exists and passes its checker;
- the current public-review round is unambiguous;
- current implementation-state contradictions have been removed;
- required schemas are present and mechanically exercised;
- the integrated proof-surface gate passes on Windows and Linux paths;
- the relevant recomputation/access-path surface is publicly routable;
- the experiment has a preregistration and manifest;
- the source corpus, prompts, receiver classes, scoring rules, and exclusions are frozen or explicitly marked not yet frozen;
- any unresolved prerequisite is represented as unresolved, not silently treated as satisfied.

## 4. Permitted extension classes

Permitted extension classes are:

- comparative handoff experiments;
- access-path and retrieval-integrity experiments;
- delayed temporal reconstruction trials;
- classifier-recomputation studies;
- bounded adversarial extensions derived from preserved failure cases.

An extension that introduces runtime authority, policy enforcement, compliance adjudication, legal sufficiency, safety approval, or production authorization is outside this protocol.

## 5. Preregistration requirements

A preregistration must identify:

- experiment and version;
- hypothesis and falsification condition;
- treatment and control;
- primary and secondary measurements;
- experimental unit;
- included scenarios;
- receiver classes and replicate count;
- planned exclusions;
- missing-data handling;
- classification method;
- human-coding and disagreement handling;
- stopping rule;
- planned synthesis;
- amendment policy;
- non-claims.

Exploratory analyses must be labeled exploratory.

## 6. Corpus and configuration freeze

Before baseline receiver execution:

- every included source artifact must have a stable path and SHA-256 digest;
- prompts and handoff packages must be preserved byte-for-byte;
- receiver identities, versions, parameters, and access paths must be recorded;
- schemas and checker versions must be bound;
- the freeze record must state whether the freeze is complete;
- an incomplete freeze prohibits baseline execution.

A change after freeze is an amendment. It must not silently replace the frozen artifact.

## 7. Baseline protection

The version progression is:

- **v0.1** — unoptimized baseline;
- **v0.1.1** — instrumentation repair only;
- **v0.2** — result-informed or optimized treatment variants.

A v0.1.1 change may repair a broken path, malformed record, schema error, or checker crash. It may not change the substantive treatment, corpus meaning, scoring rule, or receiver instruction.

A substantive change requires a new experiment version.

## 8. Amendment classes

| Class | Examples | Required consequence |
|---|---|---|
| administrative | typo, formatting, broken non-substantive link | preserve amendment record; baseline may remain valid |
| instrumentation repair | invalid path, malformed manifest, checker crash | patch version; repeat affected units |
| experimental change | prompt, corpus, treatment, scoring, receiver configuration | new experiment version |
| interpretive change | revised synthesis, additional analysis | preserve original results; label new interpretation |
| integrity repair | digest, seal, provenance, or anchor error | explicitly reassess affected baseline validity |

## 9. Receiver execution and raw-output preservation

Each receiver run must preserve:

- receiver run identifier;
- experiment, scenario, condition, receiver, and replicate identifiers;
- exact input artifacts and prompt;
- exact treatment or control package;
- receiver identity, version, parameters, and environment;
- access path and retrieval status;
- start and end timestamps;
- raw output;
- raw-output digest;
- execution status and errors;
- exclusion status and reason.

A failed retrieval, partial retrieval, interpreter incompatibility, or unavailable execution environment is an access/execution state. It is not a negative content finding.

## 10. Classification independence

Receiver execution and unsupported-inheritance classification are separate events.

At minimum, preserve:

- `receiver_run_id`;
- `classification_run_id`;
- `classification_method_id`.

Classification must be rerunnable from preserved source boundaries, treatment/control package, raw output, and classification rules without rerunning the original receiver.

Reclassification creates a new record. It does not overwrite an earlier classification.

## 11. Event-level classification

The classifier should emit event-level findings for at least:

- claim expansion without a new boundary;
- material non-claim loss;
- authority inheritance;
- unresolved-reference collapse;
- evidence-reference promotion into asserted support;
- verification-to-approval or verification-to-truth upgrade;
- mixed or unresolved aggregate collapse;
- declared-versus-observed mismatch.

A total count may be derived, but it must not replace event-level evidence.

## 12. Recomputation requirements

The baseline package must permit an external reviewer to:

- obtain the preregistration, manifest, corpus, schemas, raw outputs, and classification rules;
- validate required schemas;
- recompute artifact digests;
- rerun the deterministic classifier;
- preserve disagreements;
- distinguish receiver execution from classification;
- distinguish classification from interpretation.

Independent recomputation is evidence of bounded reproducibility. It is not endorsement, certification, approval, truth, compliance, legal sufficiency, or institutional authority.

## 13. Temporal linkage

An experiment may reference a Day-0 subject commit, replay receipt, frozen corpus digest, and planned delayed replay checkpoints.

Cross-system behavior and temporal survivability remain separate claims:

- Cross-System Claim Handoff asks whether explicit handoff instrumentation changes downstream inheritance behavior.
- Temporal replay asks whether the preserved experiment can still be reconstructed later.

Shared identifiers do not collapse those claims.

## 14. Integrity anchoring

A release anchor may bind the preregistration, manifest, corpus freeze, schemas, and source commit.

A signed tag or externally preserved digest strengthens later mutation detection and signer-controlled continuity. It does not establish truth, institutional authority, certification, or correctness.

Tag creation and publication require an explicit separate action. This protocol does not authorize a commit, tag, push, or release.

## 15. Optimization admission gate

Optimization remains prohibited until:

- every planned baseline unit has a terminal disposition;
- exclusions follow preregistered rules;
- raw outputs and digests are preserved;
- original classifications are complete;
- disagreements are preserved;
- baseline synthesis is filed;
- deviations and amendments are recorded;
- at least one independent classification recomputation is complete;
- optimized variants receive new identifiers, manifests, and freeze records.

## 16. Non-claims

This protocol does not:

- prove the Cross-System Claim Handoff hypothesis;
- establish that Fork reduces unsupported inheritance;
- authorize production use;
- certify compliance;
- establish legal sufficiency;
- approve a workflow;
- establish factual truth;
- transfer reviewer authority;
- convert successful checks into institutional sufficiency.

<!-- ASI_DEFERRED_EXTENSION_START -->
## Deferred authority-state extension

`AUTHORITY_STATE_INVARIANCE_AND_TRANSITION_MODEL_v0_1.md` is admitted as an implemented structural specification module and checker surface. `HISTORICAL_AUTHORITY_ACCRETION_EXPERIMENT_DRAFT_v0_1.md` remains a deferred draft.

This extension MUST NOT alter the Cross-System Claim Handoff v0.1 preregistration, hypothesis, corpus, treatment, control, scoring rules, or baseline schedule. Historical Authority Accretion may proceed only through a separate preregistration, frozen corpus, receiver registry, amendment policy, and independent recomputation plan.

Fork records validity, authority, and reliance histories and exposes structural misalignment. It does not decide truth, grant permission, block execution, assign answerability, determine compliance, or impose consequences.
<!-- ASI_DEFERRED_EXTENSION_END -->
