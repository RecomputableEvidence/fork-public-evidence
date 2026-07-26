# Kubernetes Master Exterior Longitudinal Observation v0.1

## Standing

`PREREGISTERED_RESEARCH_CANDIDATE_NOT_ADMITTED`

This package defines a bounded, read-only experiment for observing the public
`kubernetes/kubernetes` `master` branch through GitHub's REST API. It does not
modify Kubernetes, GitHub, Fork's governed branches, or any observed state.

The experiment separates three layers:

1. **retrieval observation** — the declared endpoint returned preserved bytes at
   a recorded observation coordinate;
2. **semantic derivation** — the preserved bytes derive a compact branch/commit
   projection under the pinned parser;
3. **external-world interpretation** — when, why, or under whose authority an
   underlying change occurred remains unresolved unless separately evidenced.

## Core hypothesis under test

> Fork can preserve and later recompute changes in an independently evolving
> external representation without changing the source, inheriting authority,
> or promoting an observation into truth, causality, approval, or execution
> standing.

## Fixed target

- public repository: `kubernetes/kubernetes`
- branch: `master`
- branch endpoint:
  `https://api.github.com/repos/kubernetes/kubernetes/branches/master`
- commit endpoint:
  `https://api.github.com/repos/kubernetes/kubernetes/commits/{sha}`
- method: `GET`
- authentication: forbidden for v0.1
- retries: zero
- redirect following: forbidden
- observer side effects: local output files and workflow artifacts only
- repository writes by observer: forbidden

## Package

- `EXPERIMENT_PREREGISTRATION_v0_1.json` — frozen experimental contract;
- `NO_EFFECTS_v0_1.json` — authority and mutation boundary;
- `CONSTRUCTION_RECEIPT_v0_1.json` — local build and test disclosure;
- `PACKAGE_MANIFEST_v0_1.json` — digest/size inventory with explicit self-exclusion;
- `schemas/OBSERVATION_RECORD_v0_1.schema.json` — observation shape;
- `schemas/COMPARISON_RECORD_v0_1.schema.json` — comparison shape;
- `tools/observe_kubernetes_master_v0_1.py` — read-only capture tool;
- `tools/check_kubernetes_observation_v0_1.py` — deterministic validator;
- `tools/check_kubernetes_experiment_package_v0_1.py` — scoped package validator;
- `tools/compare_kubernetes_observations_v0_1.py` — delayed comparison tool;
- `tests/test_kubernetes_longitudinal_observation_v0_1.py` — dependency-free
  adversarial suite;
- `.github/workflows/kubernetes-longitudinal-observation-v0-1.yml` — tests on
  pull request and manual observation dispatch only.

## Activation boundary

Opening or merging this candidate does not begin scheduled observation. The
workflow intentionally has no cron trigger because GitHub schedules execute
only from a repository's default branch and would silently couple the research
candidate to unrelated branch standing. Each live observation requires a
separate manual dispatch against an exact reviewed ref.

A later recurring-observation authorization, if desired, must be published
separately with an exact cadence, start/end window, retention plan, and
responsible operator. Elapsed time, this package, CI success, or review does not
supply that authorization.

## Correct claim form

A conforming comparison may state:

> At observation T1, GitHub's public API returned representation A for the
> declared branch. At T2, the same endpoint returned representation B. The
> preserved records establish the declared observable difference under the
> pinned procedure. The exact underlying transition time, cause, completeness,
> project approval, and authority effect remain unresolved.

It may not state that Fork verified Kubernetes' internal governance, safety,
correctness, release status, or institutional authorization.

## Local verification

```bash
python -m unittest discover \
  -s experiments/exterior-longitudinal-observation/kubernetes-master-v0.1/tests \
  -p "test_*.py" -v
```

The live observer is not called by the test suite. Tests use synthetic,
digest-bound byte specimens.
