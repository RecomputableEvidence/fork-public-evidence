# AHI Verification Matrix v0.2

## Purpose

This matrix maps the current AHI release surface to the local verification commands that a reviewer can run.

The matrix verifies structural and semantic proof-surface integrity only. It does not approve, certify, score, authorize, determine compliance, determine admissibility, establish legal sufficiency, decide acceptance, or judge correctness.

## Current endpoint

```text
ahi-sim-v0.1.9
ahi-viewer-v0.1.6
ahi-viewer-v0.2.1
```

## Verification matrix

| Surface | Command | Expected high-level result |
|---|---|---|
| Scenario 08 dedicated checker | `powershell -ExecutionPolicy Bypass -File scripts\check_scenario_08_stale_validity_authority_revocation_v0_1.ps1` | `PASS: Scenario 08 stale validity / authority revocation checks completed` |
| Main AHI simulation checker | `powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1` | `PASS: ahi-sim-v0.1.x simulation proof-surface checks completed` |
| Viewer v0.1 checker | `powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1` | `PASS: AHI viewer v0.1 hardening checks completed` |
| Viewer v0.1 determinism | `powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1 -CheckDeterminism` | `PASS: viewer builder is deterministic from a clean working tree` |
| Viewer v0.2 checker | `powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1` | `PASS: AHI viewer v0.2 comparison mode checks completed` |
| Viewer v0.2 determinism | `powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1 -CheckDeterminism` | `PASS: viewer v0.2 comparison builder is deterministic from a clean working tree` |
| Git whitespace check | `git diff --check` | no output |
| Git clean state | `git status -sb` | `## main...origin/main` after push |

## Scenario coverage

| Scenario | Dedicated or main-checker coverage | Viewer v0.1 bundle | Viewer v0.2 comparison |
|---:|---|---:|---:|
| 01 | main bundle/path checks | yes | compared through canonical pairs |
| 02 | main bundle/path checks | yes | compared with Scenario 01 |
| 03 | main semantic checks | yes | compared with Scenario 04 |
| 04 | main semantic checks | yes | compared with Scenario 03 |
| 05 | main + Scenario 05 checker | yes | compared with Scenario 06 |
| 06 | main + Scenario 06 checker + semantic invariant checker | yes | compared with Scenario 05 and 07 |
| 07 | main + Scenario 07 checker | yes | compared with Scenario 06 and 08 |
| 08 | main + Scenario 08 checker | yes | compared with Scenario 07 |

## Required current invariants

The current proof surface preserves these invariants:

```text
Bounded record integrity does not establish truth.
Internal inspectability does not establish external authority.
Policy reference does not establish policy satisfaction.
Prior validity does not establish current validity.
Prior authority does not establish current authority.
Prior evidence does not establish current evidence sufficiency.
```

## Review result interpretation

A passing check means the bounded proof-surface structure, scenario artifacts, viewer bundles, and deterministic generation checks conform to the repository's current local verification rules.

A passing check does not mean:

- the underlying claim is true;
- the downstream action is authorized;
- a legal or regulatory standard is satisfied;
- an external authority accepts the record;
- execution is eligible;
- a reviewer should rely without independent judgment.
