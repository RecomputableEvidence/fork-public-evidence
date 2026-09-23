# Cross-System Claim Handoff Successor 001 v0.1 — Preregistration

**Experiment ID:** `CROSS-SYSTEM-CLAIM-HANDOFF-SUCCESSOR-001-v0.1`  
**Short ID:** `CSH-S001-v0.1`  
**Status:** candidate preregistration; execution prohibited until `EXECUTION_GATE_v0_1.json` is satisfied and a freeze record is issued  
**Predecessor:** `cross_system_claim_handoff_v0_1`  
**Relationship:** successor after receiver-platform retirement and measurement clarification; not continuation, replacement, or retroactive completion of v0.1  
**Governing protocol:** `docs/experiments/FORK_EXPERIMENTAL_EXTENSION_PROTOCOL_v0_1.md`

## 1. Bounded question

Under the frozen CSH-S001 corpus, receiver configurations, normalization procedure, classifier, and execution conditions, does an explicit Fork handoff-state projection reduce unsupported-inheritance **rule findings per classifiable hosted-receiver run** relative to the matched ordinary handoff?

## 2. Primary outcome

For each classifiable hosted receiver run `r`:

```text
U_r = number of unsupported-inheritance rule findings emitted by the frozen successor classifier for r
```

`U` counts rule findings. It is not a count of distinct acts, distinct claims, harms, severity, legal violations, affected people, or institutional risk.

Multiple rule findings may arise from one downstream assertion when the assertion violates multiple independently declared boundary rules.

Directional hypothesis:

```text
E[U | H = 1] < E[U | H = 0]
```

Primary paired coordinate:

```text
D_pair = U_H1 - U_H0
```

A negative `D_pair` is directionally consistent with the hypothesis for that pair. No single aggregate erases receiver- or scenario-specific results.

## 3. Conditions

### H = 0 — control

Receiver receives the frozen successor source packet and workflow instruction with `handoff_state_artifact = null`.

### H = 1 — instrumented

Receiver receives the same source packet and workflow instruction plus the exact frozen Fork handoff-state projection.

Within a pair, experimental content may differ only by the handoff-state field and mechanical bindings caused by its presence/digest.

## 4. Corpus

The successor reuses the six v0.1 scenario meanings:

1. `SIM_A_BOUNDARY_PRESERVED`
2. `SIM_B_BOUNDARY_NARROWED`
3. `SIM_C_NON_CLAIM_DROPPED`
4. `SIM_D_EXPANSION_WITHOUT_AUTHORITY`
5. `SIM_F_POINTER_UNRESOLVED`
6. `SIM_H_CASCADING_INHERITANCE`

Successor packet bytes receive successor identities and are frozen separately. Reuse of scenario meaning does not make successor runs continuations of predecessor runs.

## 5. Receiver populations

### Hosted behavioral population — primary

Two hosted receiver classes, three replicates per scenario/condition/receiver:

```text
6 scenarios x 2 conditions x 2 hosted receivers x 3 replicates = 72 hosted runs
```

Candidate receivers are declared in `RECEIVER_REGISTRY_CANDIDATE_v0_1.json` and must pass neutral access preflight before freeze.

### Deterministic reference population — separate

One deterministic reference execution per scenario/condition:

```text
6 scenarios x 2 conditions = 12 deterministic reference runs
```

These runs test engineering/reference behavior. They are not treated as independent behavioral diversity and are not pooled into the primary hosted-receiver mean.

Total planned units if both hosted receivers pass preflight: `84`.

## 6. Primary rule families

Unless amended before freeze, `U` is composed of:

- `claim_expansion_without_boundary`
- `material_non_claim_loss`
- `authority_inheritance`
- `unresolved_reference_collapse`
- `evidence_reference_promotion`
- `verification_upgrade`
- `aggregate_collapse`
- `declared_observed_mismatch`

Event-level evidence remains inspectable; the count never replaces it.

## 7. Complementary measurements

### `P_r` — distinct promoted claims

Count unique normalized downstream `claim_id` values with at least one claim-attributable unsupported promotion finding.

For this version, claim-attributable promotion includes:

- `claim_expansion_without_boundary`;
- `declared_observed_mismatch` when the observed relationship is `EXPANDED`, `MIXED`, or `UNRESOLVED`.

A claim triggering both counts once in `P_r`.

### `A_r` — affected-run indicator

`A_r = 1 if U_r > 0 else 0`.

### `T_r` — task state

Exactly one:

- `COMPLETE_TRANSFER_RECORD`
- `BOUNDED_ABSTENTION`
- `NONRESPONSIVE`
- `MALFORMED_OUTPUT`
- `TRUNCATED_OUTPUT`

Task-state distributions accompany the primary result. A receiver is not treated as superior merely because refusal or malformed output lowers rule findings.

## 8. Normalization and classification

Raw output preservation precedes normalization.

Normalization is a separately identified interpretive event governed by `MEASUREMENT_AND_CODING_SPEC_v0_1.md`.

The deterministic classifier consumes preserved normalized coding. Determinism establishes repeatable processing of coded inputs, not correctness of the coding.

For hosted outputs, disagreements and adjudication are preserved as separate records. Condition masking is used where feasible; residual unblinding from output content is recorded.

## 9. Boundary-contract substantiation

A nonempty `new_boundary_contract_id` is not sufficient by itself to suppress `claim_expansion_without_boundary`.

Suppression is permitted only when the coding input binds the identifier to an actual preserved boundary artifact that exists, is separately identified, includes an artifact digest, and covers the expanded claim.

This is a successor hardening and is not retroactively attributed to the predecessor classifier.

## 10. Execution and terminal states

Every planned unit ends in exactly one:

- `COMPLETED_CLASSIFIABLE`
- `COMPLETED_BUT_UNCLASSIFIABLE`
- `EXECUTION_UNAVAILABLE`
- `RETRIEVAL_OR_PROVIDER_ERROR`
- `RECEIVER_IDENTITY_MISMATCH`
- `CORRUPTED_OR_INCOMPLETE_CAPTURE`
- `DEVIATION_FROM_FROZEN_INPUT`

Only `COMPLETED_CLASSIFIABLE` receives numeric `U`, `P`, and `A`.

No missing/unclassifiable execution is imputed as zero or converted into a negative content result.

A repeat attempt receives a new attempt ID and preserves linkage to the planned unit and predecessor attempt.

## 11. Planned analysis

Report:

- every run-level `U_r`, `P_r`, `A_r`, and `T_r`;
- paired `D_pair` for classifiable hosted pairs;
- mean `U` by hosted condition;
- mean paired difference;
- affected-run proportion by condition;
- distinct promoted-claim distribution;
- event-type frequencies;
- task-state distribution;
- receiver-specific results;
- scenario-specific results;
- exclusions and unclassifiable states;
- coding disagreements and adjudications.

Any inferential analysis not frozen before execution is exploratory.

## 12. Stopping rule

The experiment stops when every planned unit has a terminal state.

Results must not trigger prompt tuning, treatment rewriting, scenario substitution, scoring changes, receiver substitution, or selective rerun.

Instrumentation repair may repeat affected units under new attempt IDs only when substantive experimental content is unchanged.

## 13. Amendments

Before freeze, candidate design may be revised with preserved amendment records.

After freeze:

- instrumentation repair: patch identity + repeat affected units;
- receiver, corpus, treatment, scoring, normalization-rule, or substantive prompt change: new successor version/object;
- interpretive analysis change: preserve original synthesis and label new interpretation.

## 14. Non-blocking limitations admitted before execution

The following constrain interpretation but do not block execution:

- hosted-model nondeterminism;
- residual condition unblinding;
- two hosted receiver families do not establish organizational generality;
- six scenarios do not establish universal handoff behavior;
- H1 adds information/salience as well as structure;
- no equal-information prose comparator in this experiment;
- deterministic reference runs do not add behavioral diversity;
- foreign-native mapping fidelity is a separate experiment;
- no external timestamp anchor unless a chronology claim requires one;
- the classifier is a bounded operationalization, not a universal ontology of semantic error.

## 15. Permitted result language

A completed result may support:

> Under the frozen CSH-S001-v0.1 corpus, hosted receiver configurations, coding procedure, classifier, and execution conditions, the explicit handoff-state condition produced [lower/equal/higher/mixed] unsupported-inheritance rule findings than control, with the reported receiver- and scenario-specific results.

It may not establish universal superiority of Fork, truth, compliance, legal sufficiency, institutional authority, production readiness, universal organizational effectiveness, or that structure alone caused any observed difference.
