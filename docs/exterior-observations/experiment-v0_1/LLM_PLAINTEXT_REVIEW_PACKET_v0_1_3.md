# LLM Plaintext Review Packet v0.1.3

Identifier: LLM_PLAINTEXT_REVIEW_PACKET_v0_1_3
Status: Draft
Classification: Plaintext fallback for input-integrity observance
Generated date: 2026-07-08

## Purpose

This packet provides the minimum review text for LLM observers evaluating v0.1.3 input-integrity hardening.

## Packet Inclusion Boundary Clarification v0.1.3

Inclusion in this packet indicates apparatus relevance only.

Inclusion does not make any artifact sufficient for compliance, legal, production-readiness, certification, approval, validation, or endorsement conclusions.

No endorsement, validation, certification, approval, production-readiness assessment, legal conclusion, or compliance conclusion is implied.

## v0.1.4 Candidate Addendum: Artifact-Boundary Hardening

This addendum records candidate v0.1.4 hardening pressure surfaces identified after the v0.1.3 input-integrity observance batch.

This packet remains a v0.1.3 plaintext review packet.

The addendum does not convert v0.1.3 observations into endorsement, validation, certification, approval, production-readiness assessment, legal conclusion, compliance conclusion, audit sufficiency, or consensus.

### v0.1.3 batch synthesis

The v0.1.3 batch surfaced heterogeneous access and interpretation behavior:

- clean access failure with no substantive source claim;
- access failure followed by generic or conceptual analysis;
- raw packet success with documentation-layer limitation;
- direct multi-file access with artifact-level findings;
- second-order observance of batch writeups.

These differences must be preserved.

They must not be collapsed into uniform review quality.

### Access and interpretation classification excerpt

Recommended observation classifications include:

```yaml
access_status: attempted_failed | performed | partial | not_performed | unknown
retrieval_fidelity: zero | prompt_only | plaintext_packet | packet_only | multi_file | repository_clone | executable | unknown
interpretation_scope: none | conceptual_only | documentation_layer_only | data_schema_layer | direct_raw_multi_file_review | second_order_observance | unknown
source_contamination: true | false | partial | unknown
substantive_packet_review: true | false | unknown
recommended_preservation: access_mode_failure | source_contamination_after_failed_retrieval | conceptual_only_after_failed_retrieval | raw_packet_success_documentation_layer_only | direct_file_review_with_artifact_boundary_findings | second_order_observance_not_packet_review | unknown
```

### Plaintext schema excerpt

Plaintext-only observers should be able to see the minimum intake structure even when schema retrieval fails.

Minimum intake fields include:

```yaml
observer_identity: string
observer_type: human | llm | tool | unknown
access_mode:
  github_rendered: performed | attempted_failed | not_performed | partial | unknown
  raw: performed | attempted_failed | not_performed | partial | unknown
  plaintext_packet: performed | attempted_failed | not_performed | partial | unknown
  repository_clone: performed | attempted_failed | not_performed | partial | unknown
  pasted_content: performed | attempted_failed | not_performed | partial | unknown
execution_performed: true | false | unknown
retrieval_fidelity: zero | prompt_only | plaintext_packet | packet_only | multi_file | repository_clone | executable | unknown
interpretation_scope: none | conceptual_only | documentation_layer_only | data_schema_layer | direct_raw_multi_file_review | second_order_observance | unknown
non_endorsement_attestation:
  acknowledged: true | false
  statement: string
non_endorsement_statement: string
observations: list
limitations: list
```

This excerpt is descriptive.

It is not a substitute for the canonical schema artifact.

### CSV matrix summary excerpt

The v0.1.3 and v0.1.4 matrix summaries are descriptive only.

They are not substitutes for canonical CSV artifacts.

They do not imply endorsement, validation, certification, approval, production-readiness assessment, legal conclusion, compliance conclusion, audit sufficiency, or consensus.

Relevant matrix concepts include:

- observation registry entries;
- retrieval fidelity tracking;
- input-integrity pressure classification;
- active non-endorsement attestation needs;
- source contamination after failed retrieval;
- coding volume non-authority;
- packet inclusion boundary preservation;
- synthesis top-and-bottom boundary preservation.

### Artifact-local boundary rule

A boundary at the packet level is necessary but insufficient.

Artifacts that may be retrieved independently should preserve an artifact-local boundary appropriate to their format.

For CSV files, do not add comment rows unless the file format explicitly allows them.

Prefer adjacent README files, data dictionary descriptions, schema descriptions, access-index notes, or plaintext summaries marked as descriptive only.

### v0.1.4 sandbox case summary

Candidate v0.1.4 sandbox cases:

- Case 24: Analyst-output excerpting;
- Case 25: Divergent or contradictory coding;
- Case 26: Coding volume misread as audit rigor;
- Case 27: Synthesis boundary violation;
- Case 28: Packet inclusion misread as sufficiency;
- Case 29: Source contamination after failed retrieval.

----- BEGIN FILE: docs/exterior-observations/experiment-v0_1/NEXT_PASS_LLM_OBSERVANCE_REQUEST_v0_1_3.md -----

Next-Pass LLM Observance Request v0.1.3

Fork has entered Exterior Observance Experiment v0.1.3 input-integrity hardening.

Do not answer as a product reviewer. Act as an exterior observance analyst.

The ask is not endorsement, validation, approval, certification, production-readiness judgment, legal conclusion, compliance conclusion, or a general opinion.

The ask is:

Can the observance apparatus preserve non-endorsement and boundary discipline when observers, summarizers, or downstream tools intentionally or accidentally inject endorsement, scrub caveats, or treat coded volume as authority?

## Primary access path

Start with the v0.1.3 plaintext packet:

Raw:
https://raw.githubusercontent.com/RecomputableEvidence/fork-public-evidence/main/docs/exterior-observations/experiment-v0_1/LLM_PLAINTEXT_REVIEW_PACKET_v0_1_3.md

If raw access fails, use pasted packet content if provided.

## Minimum files to inspect

- LLM Plaintext Review Packet v0.1.3
- Input Integrity Guide
- Observation Intake Template
- Analysis Plan
- Coding Guide
- Sandbox v0.2 Draft
- Access Index
- Experiment Manifest

## Required evaluation

Please evaluate:

- Whether hostile endorsement injection is handled without becoming Fork authority.
- Whether automated non-endorsement scrubbing is detected as context loss.
- Whether active non-endorsement attestation is clear.
- Whether exported synthesis requires non-endorsement at both top and bottom.
- Whether coding volume is prevented from implying audit rigor, validation, production-readiness testing, consensus, or authority.
- Whether packet inclusion is clearly apparatus relevance only, not sufficiency for compliance, legal, production-readiness, certification, approval, validation, or endorsement conclusions.

## Required output format

- Scope of your pass
- Access and retrieval fidelity
- Input-integrity assessment
- Remaining overclaim risk
- Sandbox assessment
- Suggested edits
- Non-endorsement statement

Please include:

No endorsement, validation, certification, approval, production-readiness assessment, legal conclusion, or compliance conclusion is implied.

The goal is observable refinement data, not praise.


----- END FILE: docs/exterior-observations/experiment-v0_1/NEXT_PASS_LLM_OBSERVANCE_REQUEST_v0_1_3.md -----


----- BEGIN FILE: docs/exterior-observations/experiment-v0_1/ACCESS_INDEX_v0_1_3.md -----

# Access Index v0.1.3

This index records the main access surfaces for the exterior observance apparatus v0.1.3:

- Experiment protocol: https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/EXPERIMENT_PROTOCOL_v0_1.md
- Observer instructions: https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/OBSERVER_INSTRUCTIONS_v0_1.md
- Intake template: https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/templates/OBSERVATION_INTAKE_TEMPLATE_v0_1.md
- Data dictionary: https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/DATA_DICTIONARY_v0_1.md
- Coding guide: https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/CODING_GUIDE_v0_1.md
- Analysis plan: https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/ANALYSIS_PLAN_v0_1.md
- Sandbox failure cases: https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/sandbox-v0_2/SANDBOX_FAILURE_CASES_v0_2_DRAFT.md
- Intake schema: https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/schema/observation_intake_v0_1_2.schema.json
- Observation registry: https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/data/OBSERVATION_REGISTRY_v0_1.csv
- Retrieval fidelity matrix: https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/data/RETRIEVAL_FIDELITY_MATRIX_v0_1_2.csv
- Input integrity matrix: https://github.com/RecomputableEvidence/fork-public-evidence/blob/main/docs/exterior-observations/experiment-v0_1/data/INPUT_INTEGRITY_MATRIX_v0_1_3.csv


----- END FILE: docs/exterior-observations/experiment-v0_1/ACCESS_INDEX_v0_1_3.md -----


----- BEGIN FILE: docs/exterior-observations/experiment-v0_1/INPUT_INTEGRITY_GUIDE_v0_1_3.md -----

# Input Integrity Guide v0.1.3

Identifier: INPUT_INTEGRITY_GUIDE_v0_1_3
Status: Draft
Classification: Input-integrity hardening guidance

No endorsement, validation, certification, approval, production-readiness assessment, legal conclusion, or compliance conclusion is implied.

## Purpose

This guide defines how the Exterior Observance Experiment handles observer input that attempts to create authority, endorsement, validation, consensus, audit sufficiency, legal sufficiency, compliance sufficiency, or production-readiness implication.

The purpose is not to reject adverse, mistaken, enthusiastic, or hostile input.

The purpose is to preserve such input with scope, limitation, classification, and non-endorsement intact so it cannot become authority for Fork's claims.

## Input-integrity risks

The following are input-integrity pressure surfaces:

- hostile endorsement injection;
- automated non-endorsement scrubbing;
- enthusiastic observer overclaim;
- malformed intake entries;
- coding accumulation misread as audit rigor;
- downstream excerpting;
- synthesis compression;
- stale or partial retrieval presented as full-surface review;
- observer commentary treated as authority;
- recurring observations treated as consensus.

## Hostile endorsement injection

Hostile endorsement injection occurs when an observer, summarizer, or downstream tool deliberately inserts language such as:

- "Fork is validated";
- "Fork is certified";
- "Fork is production-ready";
- "Fork is legally sufficient";
- "Fork is compliance-ready";
- "Reviewers approved Fork";
- "Observers endorsed Fork";
- "The experiment proves Fork."

Such language may be preserved only as an input-integrity pressure signal.

It must not be adopted as Fork doctrine, Fork authority, observer consensus, validation, certification, approval, legal sufficiency, compliance sufficiency, audit sufficiency, or production-readiness evidence.

## Automated non-endorsement scrubbing

Automated non-endorsement scrubbing occurs when a parser, summarizer, downstream model, marketing tool, or external system removes:

- non-endorsement statements;
- scope limitations;
- execution status;
- access-mode limitations;
- stale or partial retrieval limitations;
- uncertainty markers;
- distinction between recurring observation and consensus.

A scrubbed derivative is not a valid replacement for the preserved source observation.

The apparatus may preserve the scrubbed derivative as evidence of context loss, but the scrubbed derivative does not create authority.

## Handling rule

Observer language that claims endorsement, validation, certification, approval, production readiness, legal sufficiency, compliance sufficiency, audit sufficiency, or consensus may be preserved only as an input-integrity pressure signal.

It must not be preserved as authority for Fork's claims.

## Active attestation rule

Observers should actively acknowledge that their observation does not imply endorsement, validation, certification, approval, production-readiness assessment, legal conclusion, compliance conclusion, audit sufficiency, or consensus.

Recommended attestation:

```yaml
non_endorsement_attestation:
  acknowledged: true
  statement: "By submitting this observation, the observer acknowledges that no endorsement, validation, certification, approval, production-readiness assessment, legal conclusion, or compliance conclusion is implied."
```

## Quarantine rule

If an observation includes prohibited endorsement or authority language, the intake process should:

- preserve the original language as received;
- mark the language as an input-integrity pressure signal;
- state that the language is not adopted by Fork;
- preserve the observation's scope and limitations;
- avoid using the injected language in synthesis except as a pressure-case example.

## Coding-volume boundary

Observation volume is not audit rigor.
Coding volume is not validation.

The number of coded observations must not be used to imply:

- endorsement;
- consensus;
- certification;
- approval;
- compliance sufficiency;
- legal sufficiency;
- production readiness;
- statistically representative testing;
- audit completion;
- validation of Fork's claims.

Codes structure exterior observations. They do not create authority for the observations or for Fork.

## Non-endorsement

No endorsement, validation, certification, approval, production-readiness assessment, legal conclusion, or compliance conclusion is implied.


----- END FILE: docs/exterior-observations/experiment-v0_1/INPUT_INTEGRITY_GUIDE_v0_1_3.md -----


----- BEGIN FILE: docs/exterior-observations/experiment-v0_1/EXPERIMENT_PROTOCOL_v0_1.md -----

# Experiment Protocol v0.1

Identifier: EXPERIMENT_PROTOCOL_v0_1
Status: Draft
Experiment: Exterior Observance Experiment v0.1

## 1. Research question

Does the evidence surface continue to preserve distinguishability between structural reproduction, unresolved state, evidentiary sufficiency, authority, and truth-claims under adverse conditions?

## 2. Experiment type

Structured qualitative observance experiment.

This is not a product trial, certification review, compliance review, audit, endorsement campaign, or production-readiness assessment.

## 3. Observed object

Fork's evidence-boundary surface, including:

- repository framing;
- exterior-observations corpus;
- semantic classification triage;
- sandbox v0.2 failure-case draft;
- recomputation and non-inheritance language;
- adjacent-system boundaries.

## 4. Participant categories

Potential exterior observers may include:

- AI governance practitioners;
- audit practitioners;
- compliance practitioners;
- procurement or ATO reviewers;
- systems architects;
- evidence or assurance researchers;
- adjacent governance-system builders;
- LLM reviewers;
- security or risk reviewers.

## 5. Primary observation dimensions

Observers are asked to identify:

- what Fork appears to preserve;
- what Fork appears not to claim;
- whether structural recomputation is distinguishable from evidentiary sufficiency;
- whether authority is distinguishable from preserved evidence;
- whether truth-claims remain external to evidence preservation;
- where the architecture is misunderstood;
- where terminology creates confusion;
- which adjacent systems Fork appears to touch but not occupy;
- which adverse cases should be tested next.

## 6. Hypotheses

H1: Exterior observers can distinguish Fork's evidence-preservation function from authority, approval, compliance, and truth-claim sufficiency.

H2: Observers will identify semantic classification as a recurring pressure surface.

H3: Observers will map Fork to adjacent systems without requiring Fork to absorb those systems.

H4: Misunderstandings will cluster around overloaded terms such as validation, approval, authority, compliance, evidence, truth, and verification.

H5: Failure-case observation will produce useful fixture candidates for future sandbox iterations.

## 7. Non-hypotheses

This experiment does not test whether Fork is correct, complete, compliant, safe, production-ready, commercially validated, or legally sufficient.

This experiment does not test whether observers endorse Fork.

This experiment does not test whether Fork should become an authority, policy engine, runtime controller, compliance oracle, or truth engine.

## 8. Procedure

1. Provide observers with the exterior observance entry point.
2. Provide the governing sandbox question.
3. Ask observers to inspect the materials within their own discipline.
4. Ask observers to record observations using the intake template.
5. Preserve observations with explicit scope, limitations, execution status, and non-endorsement.
6. Code observations using the coding guide.
7. Update the synthesis only as a description of recurring themes, not as consensus or validation.

## 9. Data captured

Each observation should capture:

- observer or role;
- interaction type;
- scope requested;
- scope performed;
- execution performed;
- artifacts reviewed;
- observed boundary interpretations;
- misunderstandings;
- pressure cases;
- adjacent-system mappings;
- limitations;
- non-endorsement statement;
- permission and attribution preference.

## 10. Success condition

The experiment succeeds if it produces structured exterior observation data that improves Fork's boundary language, failure-case design, semantic triage, and adjacent-system mapping without converting observer commentary into authority for Fork's claims.

## Success Condition Hardening v0.1.1

The experiment succeeds if it produces structured exterior observation data that improves or narrows Fork's boundary language, failure-case design, semantic triage, and adjacent-system mapping without converting observer commentary into authority for Fork's claims.

Success may include:

- refining boundary language;
- adding failure cases;
- improving navigation;
- identifying overloaded terms;
- narrowing a claim;
- retracting a claim;
- identifying a claim as unsupported;
- marking a term as unstable;
- marking a proposed surface as out of scope.

The experiment must not assume that every observation resolves into a wording improvement. Some observations may require claim reduction, scope reduction, or explicit non-adoption.

## v0.1.3 Packet Inclusion Boundary

Inclusion of an artifact in the plaintext packet indicates apparatus relevance only.

Inclusion does not imply:

* endorsement;
* validation;
* certification;
* approval;
* compliance sufficiency;
* legal sufficiency;
* production readiness;
* audit completion;
* consensus.

The packet is a portability surface. It is not a checklist for legal, compliance, or production readiness.


----- END FILE: docs/exterior-observations/experiment-v0_1/EXPERIMENT_PROTOCOL_v0_1.md -----


----- BEGIN FILE: docs/exterior-observations/experiment-v0_1/OBSERVER_INSTRUCTIONS_v0_1.md -----

# Observer Instructions v0.1

Identifier: OBSERVER_INSTRUCTIONS_v0_1
Status: Draft

## Purpose

You are being asked to provide a bounded exterior observation of Fork.

You are not being asked to endorse Fork, validate Fork, certify Fork, approve Fork, or determine whether Fork is production-ready.

## Primary question

Does the evidence surface continue to preserve distinguishability between structural reproduction, unresolved state, evidentiary sufficiency, authority, and truth-claims under adverse conditions?

## What to observe

Please look for:

- what Fork appears to preserve;
- what Fork appears not to claim;
- where evidence and authority remain distinct;
- where recomputation and truth-claim sufficiency remain distinct;
- where semantic language creates confusion;
- where the architecture seems to touch adjacent systems;
- where the architecture appears under-specified;
- where failure cases should be added;
- where the repository framing is unclear.

## What not to provide

Please do not provide:

- endorsement language;
- certification language;
- production-readiness conclusions;
- legal conclusions;
- compliance conclusions;
- investment or commercial validation language;
- statements that imply your observation is authority for Fork's claims.

## Preferred observation format

Use the observation intake template if possible.

If not, please explicitly state:

- what you reviewed;
- whether you executed anything;
- what your observation is limited to;
- what you think Fork preserves;
- what you think Fork must not inherit or imply;
- what pressure cases you would test next;
- that no endorsement is implied.


----- END FILE: docs/exterior-observations/experiment-v0_1/OBSERVER_INSTRUCTIONS_v0_1.md -----


----- BEGIN FILE: docs/exterior-observations/experiment-v0_1/templates/OBSERVATION_INTAKE_TEMPLATE_v0_1.md -----

# Observation Intake Template v0.1

identifier:
observer:
date:
interaction_type:
  - technical recomputation
  - architectural observation
  - governance observation
  - interoperability observation
  - semantic pressure observation
  - upstream admission observation
  - downstream procurement observation
  - scope declination
  - consulting scope signal
scope_requested:
scope_performed:
execution_status:
artifacts_reviewed:
endorsement: none
limitations:
attribution_preference:
permission_to_preserve:
classification:
  - boundary interpretation
  - semantic pressure surface
  - upstream admission
  - downstream procurement
  - role separation
  - consulting scope signal
  - failure-case proposal

## 1. Observation

[Observer text here.]

## 2. Boundary interpretation

What does Fork appear to preserve?

What does Fork appear not to claim?

Where does evidence remain distinct from authority?

Where does structural recomputation remain distinct from truth-claim sufficiency?

## 3. Misunderstandings or ambiguity

What was unclear?

Which terms created confusion?

Which claims felt too broad?

## 4. Pressure cases

What failure cases should Fork test?

## 5. Adjacent-system mapping

Which neighboring systems or functions does Fork appear to touch?

Which responsibilities should remain outside Fork?

## 6. Non-endorsement

No endorsement, certification, approval, validation, production-readiness conclusion, legal conclusion, or compliance conclusion is implied.

## Taxonomy Clarification v0.1.1

`interaction_type` describes the mode of engagement.

`classification` describes the analytical content of the observation.

These fields should not be treated as a single taxonomy.

## Access Mode Reporting v0.1.2

Observers should report access mode results explicitly:

```yaml
execution_status: not_performed
access_modes:
  github_rendered: succeeded
  raw: failed
  plaintext_packet: not_attempted
  repository_clone: not_attempted
  pasted_content: not_attempted
artifacts_requested:
  - EXPERIMENT_PROTOCOL_v0_1.md
  - OBSERVER_INSTRUCTIONS_v0_1.md
artifacts_inspected:
  - EXPERIMENT_PROTOCOL_v0_1.md
```

`execution_status` is not the same as access status.

Missing execution status, unknown execution status, failed retrieval, and not-performed execution must remain distinguishable.

## Active Non-Endorsement Attestation v0.1.3

Observers should actively acknowledge the non-endorsement boundary when submitting an observation.

Recommended structured field:

```yaml
non_endorsement_attestation:
  acknowledged: true
  statement: "By submitting this observation, the observer acknowledges that no endorsement, validation, certification, approval, production-readiness assessment, legal conclusion, or compliance conclusion is implied."
```

This attestation is an intake boundary. It does not make the observation authoritative. It records that the observer understands the observation is exterior commentary and not authority for Fork's claims.


----- END FILE: docs/exterior-observations/experiment-v0_1/templates/OBSERVATION_INTAKE_TEMPLATE_v0_1.md -----


----- BEGIN FILE: docs/exterior-observations/experiment-v0_1/DATA_DICTIONARY_v0_1.md -----

# Data Dictionary v0.1

Identifier: DATA_DICTIONARY_v0_1
Status: Draft

## Observation fields

| Field | Meaning |
|---|---|
| identifier | Stable observation record identifier |
| observer | Name, role, or anonymized label |
| date | Date observation was received |
| interaction_type | Type of contribution |
| scope_requested | What was asked of the observer |
| scope_performed | What the observer actually did |
| execution_performed | Whether the observer executed code or recomputation steps |
| artifacts_reviewed | Files, branches, docs, or sandbox elements reviewed |
| endorsement | Whether endorsement was provided; default should be none |
| limitations | Stated limits of the observation |
| attribution_preference | Named, role-only, anonymous, or private |
| permission_to_preserve | Whether the observation may be preserved |
| classification | Analytical tags assigned to the observation |

## Interaction types

| Type | Meaning |
|---|---|
| technical recomputation | Observer executed code or recomputation workflow |
| architectural observation | Observer interpreted system architecture |
| governance observation | Observer interpreted governance or authority boundary |
| interoperability observation | Observer mapped Fork to adjacent systems |
| semantic pressure observation | Observer identified language or classifier pressure |
| upstream admission observation | Observer identified execution-entry or admission boundary |
| downstream procurement observation | Observer identified procurement, ATO, or external review boundary |
| scope declination | Observer declined or bounded participation |
| consulting scope signal | Observer indicated further work requires formal engagement |

## Coding dimensions

| Dimension | Meaning |
|---|---|
| evidence_authority_distinction | Whether observer distinguished evidence from authority |
| recomputation_sufficiency_distinction | Whether observer distinguished recomputation from sufficiency |
| truth_claim_boundary | Whether observer treated truth-claims as external to preservation |
| semantic_pressure | Whether observer identified semantic classifier pressure |
| upstream_admission_mapping | Whether observer mapped Fork to governed execution or admission |
| downstream_review_mapping | Whether observer mapped Fork to procurement, ATO, or review packaging |
| role_separation | Whether observer preserved boundaries between projects or roles |
| failure_case_candidate | Whether observer proposed a testable failure case |
| misunderstanding | Whether observer revealed a misunderstanding useful for refinement |

## Taxonomy Axis Clarification v0.1.1

`interaction_type` and `classification` are separate axes.

`interaction_type` describes the mode of engagement: what kind of interaction occurred.

Examples:

- technical recomputation;
- architectural observation;
- governance observation;
- access constraint observation;
- scope declination;
- consulting scope signal.

`classification` describes the analytical content of the observation: what the observation is about.

Examples:

- boundary interpretation;
- semantic pressure surface;
- upstream admission;
- downstream procurement;
- role separation;
- failure-case proposal;
- navigation friction.

Example:

An observer may provide an `architectural observation` as the interaction type while the classification may include `boundary interpretation`, `semantic pressure surface`, and `failure-case proposal`.

## Retrieval and Execution Status v0.1.2

The observance apparatus distinguishes execution status from retrieval status.

`execution_status` describes whether code, scripts, checkers, or recomputation steps were performed.

Allowed values:

- `not_performed`
- `performed`
- `attempted_failed`
- `partial`
- `unknown`

Access mode reporting describes whether the observer could access the requested files.

Access modes:

- GitHub-rendered links
- raw links
- plaintext packet
- repository clone
- pasted content

A failed access mode is observance data. It must not be treated as a completed full-surface pass.

`interaction_type` and `classification` remain orthogonal axes. Any interaction type may pair with any classification when the observation supports it.

## Retrieval Fidelity v0.1.2

Retrieval fidelity is encoded using:

- classification tokens (e.g., `source_substitution`, `stale_or_partial_retrieval`, `LLM_accessibility_gap`);
- access-mode reporting (github_rendered/raw/plaintext_packet/repository_clone/pasted_content);
- manifest digests.

Retrieval fidelity observations are apparatus data. They do not assert endorsement, validation, certification, approval, production readiness, legal sufficiency, or compliance sufficiency.

## Input Integrity Matrix v0.1.3

The INPUT_INTEGRITY_MATRIX_v0_1_3.csv file records input-integrity pressure signals and hardening directions derived from v0.1.2 plaintext-packet observance.

Fields include:

* hostile_endorsement_injection;
* non_endorsement_scrubbing;
* coding_accumulation_risk;
* active_attestation_needed;
* packet_inclusion_boundary_needed;
* synthesis_top_bottom_boundary_needed;
* notes.

The matrix is descriptive. It does not represent consensus, endorsement, validation, certification, approval, compliance sufficiency, legal sufficiency, or production readiness.


----- END FILE: docs/exterior-observations/experiment-v0_1/DATA_DICTIONARY_v0_1.md -----


----- BEGIN FILE: docs/exterior-observations/experiment-v0_1/CODING_GUIDE_v0_1.md -----

# Coding Guide v0.1

Identifier: CODING_GUIDE_v0_1
Status: Draft

## Purpose

This guide supports consistent coding of exterior observations.

Coding describes observation patterns. It does not convert observations into consensus, authority, validation, or endorsement.

## Codes

### EVIDENCE_AUTHORITY_DISTINCTION

Use when an observer distinguishes preserved evidence from authority, approval, institutional standing, delegated power, or permission to act.

### RECOMPUTATION_SUFFICIENCY_DISTINCTION

Use when an observer distinguishes structural recomputation from evidentiary sufficiency, compliance, correctness, truth, or approval.

### TRUTH_CLAIM_BOUNDARY

Use when an observer identifies that preserved evidence and institutional authority do not themselves guarantee truth.

### SEMANTIC_PRESSURE_SURFACE

Use when an observer identifies semantic lint, authority paraphrase, false positives, false negatives, or classification ambiguity.

### UPSTREAM_ADMISSION_MAPPING

Use when an observer maps Fork to a neighboring upstream governed execution, admission, or runtime authorization layer.

### DOWNSTREAM_REVIEW_MAPPING

Use when an observer maps Fork to downstream procurement, ATO, evidence inventory, control mapping, gap register, or review packaging.

### ROLE_SEPARATION

Use when an observer maintains a boundary between their project, authority, role, or organization and Fork.

### FAILURE_CASE_CANDIDATE

Use when an observer proposes a testable adverse condition, fixture, or sandbox case.

### MISUNDERSTANDING_SIGNAL

Use when an observer misreads or conflates a Fork boundary in a way useful for future clarification.

## Coding rules

- Code only what appears in the observation.
- Do not infer endorsement.
- Do not infer consensus.
- Do not treat repeated themes as proof.
- Preserve limits, corrections, and uncertainty.
- Prefer under-coding to over-coding when ambiguous.

## What Coding Is Not v0.1.1

Coding is not endorsement.

Coding is not consensus.

Coding is not proof.

Coding is not validation.

Coding is not certification.

Coding is not approval.

Coding is not production-readiness assessment.

Coding is not legal or compliance judgment.

Coding describes patterns in bounded observations. It must not convert those observations into authority for Fork's claims.

## Retrieval Fidelity Codes v0.1.2

### ACCESS_MODE_FAILURE

Use when an observer cannot access GitHub-rendered links, raw links, plaintext packets, repository clones, or pasted content.

### PLAINTEXT_PACKET_REQUIRED

Use when an observer reports that the only reliable method is direct plaintext in the prompt or a bundled plaintext packet.

### SOURCE_SUBSTITUTION

Use when an observer is asked to inspect the experiment apparatus but instead relies on top-level README material, release notes, landing pages, mirror repositories, search snippets, or generated summaries.

### STALE_OR_PARTIAL_RETRIEVAL

Use when an observer appears to inspect outdated, incomplete, cached, or partial content.

### SURFACE_MISATTRIBUTION

Use when an observer attributes a finding to a file or surface that does not contain the stated content.

### PROMPT_ECHO_RISK

Use when an observer repeats the prompt's framing as a finding without grounding it in inspected files.

## Coding Volume Non-Authority Rule v0.1.3

Observation volume is not audit rigor.

Coding volume is not validation.

The number of `FAILURE_CASE_CANDIDATE`, `MISUNDERSTANDING_SIGNAL`, `BOUNDARY_INTERPRETATION`, or other coded observations must not be used to imply:

* endorsement;
* consensus;
* certification;
* approval;
* compliance sufficiency;
* legal sufficiency;
* production readiness;
* statistically representative testing;
* audit completion;
* validation of Fork's claims.

Codes structure exterior observations. They do not create authority for the observations or for Fork's claims.


----- END FILE: docs/exterior-observations/experiment-v0_1/CODING_GUIDE_v0_1.md -----


----- BEGIN FILE: docs/exterior-observations/experiment-v0_1/ANALYSIS_PLAN_v0_1.md -----

# Analysis Plan v0.1

Identifier: ANALYSIS_PLAN_v0_1
Status: Draft

## Purpose

This plan describes how exterior observations will be analyzed.

The purpose is to improve boundary language, sandbox design, semantic triage, and adjacent-system mapping.

The purpose is not to prove Fork, validate Fork, certify Fork, or create consensus.

## Analysis questions

1. Which boundaries do exterior observers identify without prompting?
2. Which boundaries require explanation?
3. Which terms create confusion?
4. Which adjacent systems do observers map Fork against?
5. Which adverse cases recur?
6. Which observations reveal semantic pressure?
7. Which observations reveal role or authority boundary concerns?
8. Which observations should become sandbox fixtures?
9. Which claims should be narrowed?
10. Which documentation surfaces require clearer navigation?

## Outputs

Analysis may produce:

- updated synthesis;
- semantic triage entries;
- sandbox fixture candidates;
- terminology refinements;
- repository navigation changes;
- observer-instruction refinements.

## Prohibited outputs

Analysis must not produce:

- endorsement claims;
- consensus claims;
- production-readiness claims;
- compliance claims;
- legal sufficiency claims;
- claims that exterior observers validated Fork;
- claims that observation volume proves correctness.

## Reporting format

Recurring themes should be written as:

Across preserved exterior observations, the following theme appeared...

Not:

Reviewers agreed that...

or:

This proves that...

## Synthesis Aggregation Guardrails v0.1.1

Synthesis is a high-risk overclaim point because repeated observations can visually resemble consensus.

Synthesis artifacts must carry their own non-endorsement statement.

Recurring themes should use descriptive, non-consensus phrasing, such as:

- "Several observations independently raised..."
- "Across preserved observations, the following theme appeared..."
- "N observations used similar language regarding..."
- "This theme appeared in multiple bounded observations..."

Avoid evaluative or authority-converting phrases, including:

- "Observers agreed..."
- "This proves..."
- "The review confirmed..."
- "The corpus validates..."
- "Exterior reviewers established..."

A recurring theme is an observation pattern. It is not consensus, endorsement, validation, proof, approval, certification, legal sufficiency, compliance sufficiency, or production readiness.

## Retrieval-Fidelity Analysis v0.1.2

Second-pass LLM observation showed that access can fail even when raw and GitHub-rendered links are provided.

Analysis should preserve retrieval fidelity before interpreting substantive findings.

Before coding boundary or overclaim findings, record:

* what files were requested;
* what files were actually inspected;
* what access modes succeeded;
* what access modes failed;
* whether the observer relied on top-level, release, mirror, landing-page, or search-result surfaces;
* whether any finding is stale, partial, or misattributed.

A response that fails to inspect the requested files may still be useful as retrieval-fidelity data, but it should not be treated as a completed full-surface observance pass.

## Synthesis Export Boundary Rule v0.1.3

Any exported synthesis document must embed the canonical non-endorsement statement at both the top and bottom of the file.

Top-of-file statement:

> No endorsement, validation, certification, approval, production-readiness assessment, legal conclusion, or compliance conclusion is implied.

Bottom-of-file statement:

> No endorsement, validation, certification, approval, production-readiness assessment, legal conclusion, or compliance conclusion is implied by this synthesis or by any recurring observation pattern described within it.

Reason: downstream excerpting often strips context. Duplicating the boundary at both ends creates structural friction against context loss.

Synthesis must also preserve:

* scope of observations included;
* access modes used;
* execution status;
* known stale or partial retrieval limitations;
* dissent, mismatch, or non-response where relevant;
* the distinction between recurring observation and consensus.


----- END FILE: docs/exterior-observations/experiment-v0_1/ANALYSIS_PLAN_v0_1.md -----


----- BEGIN FILE: docs/exterior-observations/sandbox-v0_2/SANDBOX_FAILURE_CASES_v0_2_DRAFT.md -----

Identifier: SANDBOX_FAILURE_CASES_v0_2_DRAFT
Status: Draft v0_2
Classification: Experimental sandbox design
Question answered: Under adverse conditions, does Fork's evidence surface preserve distinguishability between structural reproduction, unresolved state, evidentiary sufficiency, and authority?

## Governing objective

> Does the evidence surface continue to preserve distinguishability between structural reproduction, unresolved state, evidentiary sufficiency, authority, and truth-claims under adverse conditions?

## Scenario set (v0.2)

This sandbox will be defined around seven scenarios:

1. Missing required runtime coordinates.
2. Conflicting attributed emissions from two sources.
3. Later authorized determination added without rewriting original state.
4. Benign statement that triggers the semantic lint.
5. Approval or authority claim paraphrased to avoid the lint.
6. Valid receipt whose referenced source is unavailable.
7. Structurally reproducible packet containing a claim the evidence does not support.

Each scenario is evaluated against the governing objective. For every case, an independent reviewer should be able to determine:

- What reproduced.
- What failed.
- What remained unresolved.
- What the evidence packet is explicitly not allowed to prove.

Detailed fixtures and expected observations will be added in subsequent iterations.

## v0.1.1 Truth-Claim Consistency Note

The governing sandbox question includes five distinguishability targets:

- structural reproduction;
- unresolved state;
- evidentiary sufficiency;
- authority;
- truth-claims.

Truth-claims are not folded silently into evidentiary sufficiency. A structurally reproducible and evidentially well-supported packet may still be paired with a natural-language claim that is false. The sandbox should preserve that distinction visibly.

## Additional Process-Failure Pressure Cases v0.1.1

The v0.2 sandbox should include observer-process and downstream-use failures in addition to artifact-level failures.

### Case 8: Downstream excerpt without non-endorsement

Setup: An exterior observation is reproduced in a downstream document with the non-endorsement clause removed.

Expected observation: The corpus preserves the original bounded observation and its non-endorsement; downstream excerpting does not convert the observation into authority.

### Case 9: Convergent language misread as consensus

Setup: Multiple independent observations use similar language around a boundary.

Expected observation: Synthesis describes recurring language without saying observers agreed, validated, confirmed, or proved the claim.

### Case 10: Adjacent-system misattribution

Setup: An adjacent system cites a Fork evidence packet as though Fork made the adjacent system's determination.

Expected observation: Fork preserves the referenced evidence boundary without inheriting the adjacent system's determination, authority, or responsibility.

### Case 11: Reproducible packet paired with false natural-language claim

Setup: A packet is structurally reproducible and evidentially sufficient for a narrow record, but a related natural-language statement is false.

Expected observation: Structural reproduction and evidentiary sufficiency do not become truth.

### Case 12: Observer-boundary violation

Setup: Observer commentary is copied into Fork-facing claims as if it were authority.

Expected observation: The observation remains exterior commentary and must not become authority for Fork's claims.

### Case 13: Template non-compliance

Setup: An observer submits useful commentary without using the template and without an explicit non-endorsement statement.

Expected observation: Intake records the limitation and requests or appends a boundary note before preservation.

### Case 14: Downstream legal or compliance misinterpretation

Setup: A downstream legal, compliance, procurement, or ATO reader treats recomputation as legal proof or compliance approval.

Expected observation: The corpus preserves this as a misinterpretation signal, not as Fork's claim.

### Case 15: Automated observer with uncertain access scope

Setup: An LLM observer reports inability to access directory views or only reviews a subset of direct files.

Expected observation: The access limitation is preserved explicitly and does not become a full-surface review.

## Additional Retrieval-Fidelity Pressure Cases v0.1.2

### Case 16: Reviewer source substitution

Setup: An observer is asked to inspect the experiment apparatus but instead inspects top-level repository material, release notes, mirror pages, search snippets, or public landing pages.

Expected observation: The intake process preserves the substitution as a retrieval-fidelity limitation and does not treat the response as a completed full-surface observance pass.

### Case 17: Reviewer access-mode failure

Setup: An LLM observer is provided GitHub-rendered links and raw links but cannot retrieve underlying markdown text.

Expected observation: The access failure is preserved as an access-scope limitation. The observer is offered a plaintext packet fallback.

### Case 18: Stale or partial retrieval

Setup: An observer reports full-surface access but misses content that exists in the current apparatus version.

Expected observation: The observation is preserved with a stale-or-partial retrieval classification.

### Case 19: Prompt echo with misattribution

Setup: An observer repeats the prompt's requested checks as findings and attributes them to files that were not actually inspected.

Expected observation: The response is coded as prompt-echo risk and surface misattribution.

### Case 20: Model-to-model propagation context loss

Setup: An LLM-generated observation is later summarized by another model without scope, limitation, or non-endorsement.

Expected observation: The context loss is preserved and corrected before any downstream use.

### Case 21: Compression or summarization drift

Setup: A downstream summary compresses a bounded observation into a flat claim.

Expected observation: The apparatus identifies the drift and restores the original scope, limitation, and non-endorsement.

### Case 22: Hostile Endorsement Injection

Setup: An observer ignores the observer instructions and attempts to inject validation, certification, approval, endorsement, production-readiness, legal, or compliance language into the intake template.

Expected observation: The intake process preserves the attempted injection as an input-integrity pressure signal. The endorsement language is not adopted as Fork authority, consensus, validation, approval, certification, legal sufficiency, compliance sufficiency, or production-readiness evidence.

Boundary preserved: Observer commentary remains exterior commentary. Even hostile or enthusiastic observer language does not become authority for Fork's claims.

Residual risk: Downstream users may still quote the injected language outside the repository. This requires excerpting and context-loss controls.

### Case 23: Automated Non-Endorsement Scrubbing

Setup: An automated parser, summarizer, marketing tool, or downstream LLM extracts observation text while removing the non-endorsement statement, scope limitation, execution status, or access-mode limitation.

Expected observation: The apparatus identifies the scrubbed version as context loss. The preserved source observation remains bounded by its original scope, limitations, and non-endorsement. The scrubbed derivative is not treated as authority, validation, consensus, approval, certification, legal sufficiency, compliance sufficiency, or production-readiness evidence.

Boundary preserved: Non-endorsement is part of the preserved observation context, not optional decoration.

Residual risk: External systems may continue to circulate scrubbed excerpts. The apparatus can preserve and correct the loss but cannot control external redistribution.


----- END FILE: docs/exterior-observations/sandbox-v0_2/SANDBOX_FAILURE_CASES_v0_2_DRAFT.md -----


----- BEGIN FILE: docs/exterior-observations/experiment-v0_1/RETRIEVAL_FIDELITY_GUIDE_v0_1_2.md -----

# Retrieval Fidelity Guide v0.1.2

Identifier: RETRIEVAL_FIDELITY_GUIDE_v0_1_2
Status: Draft
Classification: Instrumentation guidance

## Purpose

This guide records how observers should report what they actually accessed.

The Exterior Observance Experiment must distinguish:

- requested files;
- files actually inspected;
- access method used;
- failed access modes;
- stale or partial retrieval;
- source substitution;
- prompt echo;
- conclusions grounded in adjacent surfaces.

## Required access-mode reporting

Each LLM or automated observer should report:

- GitHub-rendered link access: succeeded / failed / not attempted
- raw link access: succeeded / failed / not attempted
- plaintext packet access: succeeded / failed / not attempted
- repository clone: succeeded / failed / not attempted
- pasted-content access: succeeded / failed / not attempted

## Retrieval fidelity classifications

Use these classifications when appropriate:

- access_mode_failure
- plaintext_packet_required
- source_substitution
- stale_or_partial_retrieval
- prompt_echo_risk
- surface_misattribution
- retrieval_scope_unclear
- retrieval_fidelity_sufficient

## Source substitution

Source substitution occurs when an observer is asked to inspect the experiment apparatus but instead inspects:

- top-level README material;
- release notes;
- project landing pages;
- mirror repositories;
- search snippets;
- generated summaries;
- adjacent documentation.

Source substitution is useful observance data, but it must not be treated as a full-surface observance pass.

## Stale or partial retrieval

A stale or partial retrieval occurs when an observer claims to inspect the surface but misses expected current content.

The intake process should preserve the observation while marking the retrieval limitation.

## Non-endorsement

Retrieval success or failure does not imply endorsement, validation, certification, approval, production readiness, legal sufficiency, or compliance sufficiency.


----- END FILE: docs/exterior-observations/experiment-v0_1/RETRIEVAL_FIDELITY_GUIDE_v0_1_2.md -----


----- BEGIN FILE: docs/exterior-observations/experiment-v0_1/EXCERPTING_AND_CONTEXT_LOSS_APPENDIX_v0_1.md -----

# Excerpting and Context-Loss Appendix v0.1

Identifier: EXCERPTING_AND_CONTEXT_LOSS_APPENDIX_v0_1
Status: Draft
Classification: Context-preservation guidance

## Purpose

Exterior observations can be misused when quoted without scope, limitations, or non-endorsement.

This appendix provides examples of context loss and corrected preservation.

## Example 1: Bad excerpt

Original observation:

"Fork's boundary language is disciplined. No endorsement, validation, certification, approval, production-readiness assessment, legal conclusion, or compliance conclusion is implied."

Bad downstream excerpt:

"Fork's boundary language is disciplined."

Problem:

The non-endorsement clause was removed. The excerpt may be read as approval.

Corrected excerpt:

"One bounded exterior observation stated that Fork's boundary language is disciplined, while explicitly preserving that no endorsement, validation, certification, approval, production-readiness assessment, legal conclusion, or compliance conclusion was implied."

## Example 2: Bad consensus compression

Original synthesis:

"Across preserved observations, several observers used similar language regarding the evidence-authority boundary."

Bad downstream summary:

"Reviewers agreed that Fork preserves the evidence-authority boundary."

Problem:

Recurring language was converted into agreement.

Corrected summary:

"Several preserved observations used similar language regarding the evidence-authority boundary. This pattern is descriptive and does not imply consensus, validation, or endorsement."

## Example 3: Bad authority transfer

Original observation:

"Fork appears to preserve evidence without absorbing authority."

Bad downstream use:

"External observers confirmed Fork does not absorb authority."

Problem:

An observation was converted into confirmation.

Corrected use:

"A bounded exterior observation described Fork as appearing to preserve evidence without absorbing authority. That observation is not authority for Fork's claims."

## Required preservation rule

When excerpting an observation, preserve:

- observer scope;
- execution status;
- limitation;
- non-endorsement;
- whether the observer inspected the requested files;
- whether the statement is descriptive rather than normative.

## Non-endorsement

This appendix does not establish correctness, endorsement, validation, certification, approval, production readiness, legal sufficiency, or compliance sufficiency.


----- END FILE: docs/exterior-observations/experiment-v0_1/EXCERPTING_AND_CONTEXT_LOSS_APPENDIX_v0_1.md -----


----- BEGIN FILE: docs/exterior-observations/experiment-v0_1/EXPERIMENT_MANIFEST_v0_1_3.json -----

{
  "version": "v0.1.3",
  "status": "draft",
  "date": "2026-07-08",
  "components": {
    "protocol": "docs/exterior-observations/experiment-v0_1/EXPERIMENT_PROTOCOL_v0_1.md",
    "observer_instructions": "docs/exterior-observations/experiment-v0_1/OBSERVER_INSTRUCTIONS_v0_1.md",
    "intake_template": "docs/exterior-observations/experiment-v0_1/templates/OBSERVATION_INTAKE_TEMPLATE_v0_1.md",
    "data_dictionary": "docs/exterior-observations/experiment-v0_1/DATA_DICTIONARY_v0_1.md",
    "coding_guide": "docs/exterior-observations/experiment-v0_1/CODING_GUIDE_v0_1.md",
    "analysis_plan": "docs/exterior-observations/experiment-v0_1/ANALYSIS_PLAN_v0_1.md",
    "sandbox_failure_cases": "docs/exterior-observations/sandbox-v0_2/SANDBOX_FAILURE_CASES_v0_2_DRAFT.md",
    "intake_schema": "docs/exterior-observations/experiment-v0_1/schema/observation_intake_v0_1_2.schema.json",
    "observation_registry": "docs/exterior-observations/experiment-v0_1/data/OBSERVATION_REGISTRY_v0_1.csv",
    "retrieval_fidelity_matrix": "docs/exterior-observations/experiment-v0_1/data/RETRIEVAL_FIDELITY_MATRIX_v0_1_2.csv",
    "input_integrity_matrix": "docs/exterior-observations/experiment-v0_1/data/INPUT_INTEGRITY_MATRIX_v0_1_3.csv",
    "access_index": "docs/exterior-observations/experiment-v0_1/ACCESS_INDEX_v0_1_3.md",
    "plaintext_packet": "docs/exterior-observations/experiment-v0_1/LLM_PLAINTEXT_REVIEW_PACKET_v0_1_3.md"
  },
  "non_endorsement": "No endorsement, validation, certification, approval, production-readiness assessment, legal conclusion, or compliance conclusion is implied."
}


----- END FILE: docs/exterior-observations/experiment-v0_1/EXPERIMENT_MANIFEST_v0_1_3.json -----
