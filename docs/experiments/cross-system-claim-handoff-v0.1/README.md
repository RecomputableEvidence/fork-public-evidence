# Cross-System Claim Handoff v0.1

Status: frozen baseline incomplete; two original provider attempts preserved; required repetitions blocked before invocation
Experiment class: comparative handoff experiment  
Treatment: explicit Fork handoff-state artifact  
Control: same source and workflow instruction without the explicit Fork handoff-state artifact

## Primary question

When the same bounded source material crosses into another system, does an explicit Fork handoff-state artifact reduce unsupported inheritance relative to an otherwise comparable handoff without that artifact?

## Canonical hypothesis

```text
E[U | H = 1] < E[U | H = 0]
```

Where:

- `U` is the rate of unsupported-inheritance events per receiver run.
- `H = 1` means the explicit Fork handoff-state artifact is present.
- `H = 0` means it is absent.

## Planned matrix

```text
6 scenarios x 2 conditions x 3 receiver classes x 3 replicates = 108 receiver runs
```

## Current admission state

- protocol: present;
- preregistration: present;
- schemas: present;
- classifier: present;
- corpus descriptors: present;
- receiver identities, versions, parameters, and adapters: configured and frozen;
- shared instruction, twelve prompt packets, six handoff artifacts, and fixed run order: configured and frozen;
- corpus digest freeze: complete;
- release anchor: signed tag published and GitHub-verified;
- baseline execution: original CSH-RUN-001 (HTTP 200) and CSH-RUN-002 (HTTP 429) preserved; neither is silently replaced;
- current mutable execution state: [Pair-001](execution-state/PAIR-001_EXECUTION_STATE_v0_1_1.json);
- current gate: [2026-09-21 preflight](execution-state/reconciliation-2026-09-21/PAIR001_GATE_DECISION_2026_09_21.json), blocked before new provider invocation;
- historical “not started” fields inside the semantic freeze remain freeze-time statements;
- optimization: prohibited until baseline completion and independent recomputation.

## Verification

```bash
python tools/check_cross_system_claim_handoff_v0_1.py --json
python tools/classify_unsupported_inheritance_v0_1.py tests/fixtures/csh/classifier_input_clean.json --json
python -m pytest tests/test_cross_system_claim_handoff_v0_1.py -q
```

Use `--require-complete-baseline` only after all planned runs have terminal dispositions.

## Boundary

This scaffold does not prove that Fork reduces unsupported inheritance. It does not certify, approve, authorize, validate, or establish production, compliance, legal, safety, procurement, or institutional sufficiency.
