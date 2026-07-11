# Cross-System Claim Handoff v0.1 Preregistration

Status: preregistered design; baseline execution prohibited until the corpus/configuration freeze is complete  
Version: v0.1  
Governing protocol: `docs/experiments/FORK_EXPERIMENTAL_EXTENSION_PROTOCOL_v0_1.md`

## 1. Hypothesis

Let `U` be the rate of unsupported-inheritance events per receiver run.

Let `H` indicate the presence of an explicit Fork handoff-state artifact.

The preregistered directional hypothesis is:

```text
E[U | H = 1] < E[U | H = 0]
```

The hypothesis is weakened or requires refinement if the instrumented condition does not reduce unsupported inheritance, reliance ambiguity, non-claim loss, or authority leakage under the frozen experiment design.

## 2. Experimental unit

One unit is:

```text
scenario x condition x receiver class x replicate
```

Planned matrix:

```text
6 scenarios x 2 conditions x 3 receiver classes x 3 replicates = 108 receiver runs
```

## 3. Conditions

### Control — H = 0

The receiver receives:

- the frozen source artifact;
- the frozen workflow instruction;
- no explicit Fork handoff-state artifact.

### Instrumented — H = 1

The receiver receives the same frozen source artifact and workflow instruction plus an explicit Fork handoff-state artifact preserving:

- emitted claim boundary;
- non-claims;
- relationship to upstream claims;
- authority references;
- evidence references;
- unresolved state;
- permitted narrowing;
- prohibited inherited conclusions;
- required local revalidation.

Only the handoff instrumentation may differ between paired control and treatment units.

## 4. Included scenarios

The primary corpus uses existing Fork simulation classes:

1. `SIM_A_BOUNDARY_PRESERVED`
2. `SIM_B_BOUNDARY_NARROWED`
3. `SIM_C_NON_CLAIM_DROPPED`
4. `SIM_D_EXPANSION_WITHOUT_AUTHORITY`
5. `SIM_F_POINTER_UNRESOLVED`
6. `SIM_H_CASCADING_INHERITANCE`

Declared-versus-observed mismatch and aggregate-collapse extensions are reserved for a separately versioned adversarial extension unless admitted before freeze.

## 5. Receiver classes

Three receiver classes are planned:

- `llm_receiver_a`;
- `llm_receiver_b`;
- `deterministic_receiver`.

Exact providers, model/version identifiers, parameters, tools, wrappers, and access paths must be recorded in `SYSTEM_REGISTRY_v0_1.json` before freeze.

Human reviewers code preserved outputs. Human reviewers are not primary experimental receivers.

## 6. Primary measurement

The primary measurement is the count and rate of unsupported-inheritance events per receiver run.

An unsupported-inheritance event includes:

- claim expansion without a new boundary contract;
- material non-claim loss;
- authority inheritance;
- unresolved-reference collapse;
- evidence-reference promotion into asserted support;
- structural verification upgraded into approval, truth, compliance, or sufficiency;
- mixed or unresolved aggregate collapsed into a positive determination;
- declared-versus-observed relationship mismatch.

## 7. Secondary measurements

Record separately:

- claim preservation;
- valid narrowing;
- claim expansion;
- non-claim loss;
- authority leakage;
- unresolved-pointer collapse;
- evidence promotion;
- verification upgrade;
- aggregate collapse;
- access-path compatibility;
- execution success;
- classifier success;
- human/automated agreement;
- independent recomputation success.

No single confidence, compliance, trust, or readiness score will replace these event-level measurements.

## 8. Classification

Receiver execution and classification are separate events.

The deterministic classifier consumes:

- source boundary;
- expected relationship;
- applicable non-claims;
- unresolved references;
- treatment/control metadata;
- normalized receiver output.

It emits event-level findings and a total event count.

Human coding and disagreements are preserved separately. Reclassification creates a new record linked to the original receiver run.

## 9. Planned analysis

Primary descriptive analysis:

- compare mean unsupported-inheritance events per run for `H = 1` and `H = 0`;
- compute paired differences within scenario, receiver class, and replicate;
- report event-type frequencies by condition;
- report receiver-class and scenario-specific results without collapsing them into a universal claim.

Any inferential analysis added later is exploratory unless preregistered by amendment before freeze.

## 10. Exclusions and missing data

A run may be excluded only for:

- retrieval failure;
- interpreter incompatibility;
- execution unavailable;
- corrupted or incomplete preserved output;
- receiver identity/version mismatch;
- deviation from the frozen input or condition.

Every excluded run receives a terminal record with reason. Exclusion does not erase the run attempt.

A replacement run uses a new run identifier and preserves linkage to the excluded attempt.

## 11. Stopping rule

The baseline stops when every planned experimental unit has a terminal disposition:

- completed and classifiable;
- completed but unclassifiable with preserved reason;
- excluded under a preregistered rule;
- execution unavailable with preserved reason.

Results must not trigger early termination, prompt tuning, treatment rewriting, or corpus substitution.

## 12. Amendments

Amendments follow the classes in the Experimental Extension Protocol.

A substantive prompt, corpus, treatment, scoring, receiver, or classification-rule change requires a new experiment version.

Instrumentation repairs after execution begins require a patch version and repetition of affected units.

## 13. Baseline protection and optimization

No result-informed optimization is permitted in v0.1.

Optimization may begin only after:

- complete baseline disposition;
- raw-output preservation;
- original classification completion;
- disagreement preservation;
- baseline synthesis;
- deviation filing;
- at least one independent classification recomputation.

Optimized variants begin at v0.2 and retain the v0.1 corpus for comparison.

## 14. Temporal reconstruction

Each run should reference the Day-0 subject state, corpus digest, experiment release anchor, and planned delayed replay checkpoints.

CSH behavior and temporal replay remain separate claims.

## 15. Non-claims

This preregistration does not:

- prove the hypothesis;
- establish universal superiority of explicit handoff artifacts;
- establish production readiness;
- certify compliance;
- establish legal sufficiency;
- validate source truth;
- authorize execution;
- transfer reviewer authority;
- establish institutional sufficiency.

## 16. Pre-freeze receiver and ordering configuration

The v0.1 receiver bindings are:

- `llm_receiver_a`: `meta/Llama-4-Scout-17B-16E-Instruct` through the GitHub Models REST inference endpoint;
- `llm_receiver_b`: `deepseek/DeepSeek-V3-0324` through the same GitHub Models REST inference endpoint;
- `deterministic_receiver`: `tools/csh_receiver_deterministic_v0_1.py`, bound by source SHA-256 in `SYSTEM_REGISTRY_v0_1.json`.

Both hosted receivers use the same serving platform. The baseline therefore compares model families, not serving-platform independence.

Each paired prompt packet contains the same workflow task and exact scenario object. The only pairwise field difference is `handoff_state_artifact`: `null` for `control_h0` and the exact scenario-specific handoff object for `instrumented_h1`.

The 54 scenario/receiver/replicate pairing keys are ordered by SHA-256 of the fixed salt `CSH_V0_1_PAIR_BLOCK_ORDER_SHA256_2026_07_11`, a separator, and the pairing key. Paired conditions remain adjacent, with H0-first and H1-first alternating by pair-block ordinal, yielding 27 blocks of each order. The resulting 108-unit order is recorded in `prompts/RUN_ORDER_v0_1.json`.

This configuration remains draft and execution-blocked until the corpus freeze is committed, verified, and anchored by the signed freeze tag.
