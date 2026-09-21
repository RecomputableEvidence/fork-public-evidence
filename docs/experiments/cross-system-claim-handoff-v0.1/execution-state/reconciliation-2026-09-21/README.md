# CSH reconciliation and continuation gate — 2026-09-21

Status: LOCAL CANDIDATE, NOT PUSHED OR MERGED. Provider executions this session: **0**.

## Delivered changes

1. Canonical amendment register now indexes AMEND-001, AMEND-002 and AMEND-003. AMEND-001's historical content is unchanged. Source amendments remain byte-identical.
2. Mutable Pair-001 state now distinguishes the already-published instrumentation repair, observed successful required CI, and outstanding anchor publication. It appends two transitions; original attempt entries and repeat population are preserved.
3. One v0.5 predecessor-plus-delta standing overlay covers the four material post-v0.4 repository object changes (Stacked Cadence, FREEZE-002, SE-003, IRR-001) and current CSH reconciliation. Root and directory entry points route to it as a local candidate. Historical overlays are unchanged.
4. The missing instrumentation release anchor is prepared using the existing orchestrator's format, bound to the actual original repair commit and its two successful named workflows. Its own publication and CI are NOT asserted.
5. A bounded preflight receipt records the blockers, exact request hashes and two proposed new IDs. Neither ID is recorded as an executed run. The existing repeat population stays empty.

## Decision

**BLOCKED_BEFORE_PROVIDER_INVOCATION — DO NOT CONTINUE THE BASELINE.**

The original repair commit 54b04dc8d685c79abeceb9d79ddbcf6493ee1a71 has both required workflows successful. AMEND-003 commit adb7300f96cfc65d2764ca3a3ce45f344ab56404 also has both required workflows successful. Raw API responses preserve other workflow results, including the unrelated failure at the AMEND-003 commit. No all-CI-green claim is made.

The observed blockers are the unpublished new release anchor, absent GITHUB_TOKEN in this runtime, and absence of an operative external repeat adapter. The frozen repository adapter deliberately throws. The inspected resume-safe orchestrator additionally expects Windows PowerShell and authenticated GitHub CLI for its publication gate. This Linux runtime does not have PowerShell installed. No substitute model or fabricated raw response was used.

This is a pre-execution block. It is NOT a completed AMEND-002 repetition, provider failure, null result, adverse comparative result, or evidence about Fork's treatment effect.

## Apply the prepared change

The patch is bound to source commit 38a19bfedd37c630833893b372584fa56111bbb0. Use a clean review branch based on that commit. If main has advanced, reconcile the delta and refresh source bindings before publication; do not force this snapshot over newer work.

```powershell
git switch -c csh/reconcile-20260921 38a19bfedd37c630833893b372584fa56111bbb0
git apply --check CSH-Reconciliation-2026-09-21.patch
git apply CSH-Reconciliation-2026-09-21.patch
python tools/check_cross_system_claim_handoff_execution_v0_1_1.py --json
```

The archive also includes the changed/new files under `payload/`. Prefer applying the patch, which retains the base-file checks, over copying the payload blindly.

## Resume the existing experiment

1. Publish the reviewed reconciliation and prepared anchor. Preserve the exact commit containing that anchor. Observe both `Cross-System Claim Handoff v0.1` and `Fork Proof-Surface Integration` successful on that commit. Keep AMEND-003's historical candidate wording unchanged; current records supply its later publication state.
2. In the authorized execution environment, supply GITHUB_TOKEN through the existing secret mechanism, not in a message or committed file. Supply an operative provider-specific adapter to the existing resume-safe orchestrator. Preserve its source hash. The adapter must use the already-configured GitHub Models endpoint and DeepSeek-V3-0324; no silent model migration.
3. Copy and transmit each preserved exact-request.json byte-for-byte. Do not reconstruct the payload or insert a run identifier into it. Use two fresh IDs and link them to CSH-RUN-001 and CSH-RUN-002. The receipt's proposed IDs are placeholders until collision checks and actual invocation; the existing orchestrator generates its own timestamped fresh IDs.
4. Preserve every attempted terminal outcome, request bytes, raw response bytes (only if received), execution metadata, times, adapter identity and hashes. Do not retry under a used ID. If a transport or adapter fails, preserve the failure explicitly rather than inventing a provider response.
5. Validate repetition lineage with the existing execution checker in strict `--require-repeat` mode. Preserve execution, representation/normalization, classification, and pair comparison separately under the existing evidence contracts. Do not infer repaired semantic execution from HTTP 200 alone.
6. Issue a new evidence-bound gate decision from the two actual repetitions. Continue only if they demonstrate the repaired execution path and required evidence chain sufficiently. Otherwise preserve the bounded failure or blocked state and stop. Do not overwrite this preflight receipt.
7. If permitted, continue the frozen fixed order after the affected Pair-001 units using RUN_ORDER_v0_1.json. Keep the original 108-unit design, scenarios, receiver identities, parameters, prompts, treatment, classification and stopping rules. Repetition attempts are lineage attached to affected units, not extra randomized design cells. Preserve every terminal disposition. Keep independent classification recomputation and optimization restrictions as frozen.

No positive effect is required to continue or report a valid comparative result. Outcome direction and execution integrity are separate. No new architecture or revised scoring rule is introduced here.

## Validation and boundaries

VALIDATION_REPORT.json records 22 successful checks, including the existing 11-check instrumentation result and six existing tests. The strict repetition checker correctly fails on missing repetitions; that expected failure is preserved. All existing tracked modifications are restricted to five routing/register/mutable-state files. Original attempts, semantic and instrumentation freeze files, closed admissions and v0.1–v0.4 standing overlays remain unchanged.

The overlay covers repository-observed state through the bound commit, not an exhaustive new assessment of every off-repository research object. Source records retain their own limitations. No closed object was reopened or pressure-tested.
