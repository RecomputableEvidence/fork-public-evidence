# PROOF-002 / PR #65 Exterior Recomputation Handoff v0.1

## Review target

- proof: `PROOF-002 — Correction Does Not Erase Failure`
- candidate PR: `#65`
- exact corrected head: `479de5f929cb37377ccba5ef93f7a4f7b93e1120`
- historical reviewed predecessor: `c15c105f7277494b335d1d038bda58c1dbc78b16`
- predecessor disposition: `REPRODUCED_WITH_CORRECTION_REQUIRED`
- current gate: `INDEPENDENT_EXACT_HEAD_EXTERIOR_RECOMPUTATION_REQUIRED`
- direct merge of PR #65: **not authorized**

The predecessor failure is evidence and must remain visible. A successful recomputation of the corrected head does not rewrite or erase it.

## Independence disclosure

Before reporting a result, state whether you participated in Fork or PR #65 construction, hardening, testing, or prior review. A construction-assisted or same-loop review must not be represented as independent.

## Exact checkout

Use the exact commit, not a mutable branch name:

```bash
git fetch origin
git checkout --detach 479de5f929cb37377ccba5ef93f7a4f7b93e1120
git rev-parse HEAD
```

Expected HEAD:

```text
479de5f929cb37377ccba5ef93f7a4f7b93e1120
```

## Canonical instructions

Follow the candidate's own immutable instruction surface:

`docs/recomputation/m87-fork/adv-003/RECOMPUTATION_INSTRUCTIONS_v0_1.md`

The required principal commands are:

```bash
python tools/check_longitudinal_reconstruction_day0_packet_v0_1_1.py --json
python tools/check_longitudinal_day0_adv_003_recomputation_v0_1.py --repo-root . --json > ADV_003_POST_FIX_RECOMPUTATION_v0_1.json
python -m pytest -q tests/test_longitudinal_day0_adv_003_v0_1.py
```

The derivative harness is expected to report 17/17 cases passing, including the ten-case canonical-path representation matrix. Do not substitute a summary assertion for the raw JSON return.

## Required adversarial boundary

Verify that the corrected head rejects the declared noncanonical path families after their relevant bindings are recomputed, including dot and dot-dot segments, duplicate/trailing separators, Windows drive forms, UNC forms, backslashes, and mixed separators. A stale hash or stale outer receipt is not sufficient evidence of semantic rejection.

## Return package

Return, without editing the generated machine output:

1. exact commit SHA;
2. OS, filesystem/runtime, Python version, and relevant symlink capability;
3. the generated `ADV_003_POST_FIX_RECOMPUTATION_v0_1.json`;
4. SHA-256 of that JSON and the four candidate artifacts listed in the canonical instructions;
5. focused pytest stdout/stderr and process exit status where available;
6. any tool/environment limitation;
7. any correction or contradictory observation;
8. one bounded disposition:
   - `RECOMPUTED_POST_FIX_CONFORMING`
   - `RECOMPUTED_POST_FIX_NON_CONFORMING`
   - `RECOMPUTATION_INCONCLUSIVE`

## Standing boundary

A return does not itself admit PR #65 or PROOF-002. If the return conforms, the next repository act is a **current-tip evidence successor** that preserves the predecessor failure, correction lineage, exact-head return, and reviewer independence disclosure. The deeply diverged PR #65 branch remains historical rather than being directly rebased or silently normalized.

No result here certifies security, closes ADV_001/ADV_002, authorizes execution, changes Candidate Model standing, authorizes a pilot, or transfers authority.
