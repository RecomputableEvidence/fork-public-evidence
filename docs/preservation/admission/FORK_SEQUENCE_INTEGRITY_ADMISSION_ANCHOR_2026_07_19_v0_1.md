# Fork Sequence and Integrity Admission Anchor — 2026-07-19 v0.1

Status: `PROPOSED_APPEND_ONLY_ADMISSION`

This separate successor record proposes admission of PR #81's Sequence Surface projection and PR #82's root-checksum preservation and enforcement change into `preservation/clean-continuance-v0.1`. It is based on exact preservation commit `0bac4f60986e0be4da53d6b69c49aab1f7e73e7d`, binds the reviewed heads, merge commits, merged trees, successful head-specific workflow runs, exterior-review standing, and remaining residuals, and performs no provider call or Pair-001 action.

The machine-readable record is `FORK_SEQUENCE_INTEGRITY_ADMISSION_ANCHOR_2026_07_19_v0_1.json`.

## Exact merge lineage

| PR | Reviewed head | Merge commit | Merge tree | Standing if this anchor is admitted |
|---|---|---|---|---|
| #81 | `c879242c4dafad68bdd8e7bcf2466e4169351969` | `97abe21daed2daec8a608851467875df42a99f0a` | `31f1838e6cff6035370c4d99fc58cff620cdb42f` | admitted cross-surface inspectability projection; not a seventh modular surface |
| #82 | `5150ece4c29cea38cfe5e25daeb781423c680834` | `0bac4f60986e0be4da53d6b69c49aab1f7e73e7d` | `34be4be69ef7c684c14b49a88df382e2db065bd3` | admitted byte-integrity enforcement with the adverse discrepancy preserved |

PR #81 was merged with first parent `5fbabbd486d4e863d23e0096600185ada92539a6` and second parent the reviewed head. PR #82 was retargeted onto the PR #81 merge before its final workflow runs, but its reviewed head retained parent `c6bb2df424193e7ef043ee3c0436bf97ba10fc6e`; it was not rewritten into a direct descendant of PR #81. Its merge commit has PR #81's merge as first parent and the exact reviewed PR #82 head as second parent, producing the combined tree bound above.

## Head-specific workflow evidence

- PR #81 head `c879242c4dafad68bdd8e7bcf2466e4169351969`: Fork Evidence CI `29711689896`; Fork Proof-Surface Integration `29711689916`.
- PR #82 head `5150ece4c29cea38cfe5e25daeb781423c680834`, after retargeting: Fork Evidence CI `29712015177`; Root Checksum Manifest v0.1 `29712015182`; Fork Proof-Surface Integration `29712015188`.

All five runs concluded `success`. This binds recorded workflow conclusions to the reviewed heads; it does not convert CI into semantic truth, independent approval, merge authority, or provider-execution authority.

## Bound standing

The Sequence Surface ledger, deterministic projection, transition contract, schema, and running checker are SHA-256 and Git-blob bound in the machine-readable anchor at the combined #82 merge tree. If this anchor is merged, their standing becomes an admitted cross-surface inspectability projection in the preservation lineage. They do not become a seventh modular surface and do not orchestrate progression.

The repaired 51-entry root manifest, preserved pre-repair specimen, discrepancy record, and strict checksum checker are likewise bound at the combined tree. The original `research/standards/README.md` mismatch remains append-only evidence. Admission makes its prospective enforcement standing explicit; it does not rewrite the discrepancy or claim that prior green workflows evaluated the manifest.

## Exterior-review standing

The root checksum discrepancy originated in a user-transmitted exterior fresh-clone report and was independently reproduced inside the repository workstream before preservation and repair. The complete exterior report is not enclosed by this anchor, and its source identity is not independently verified. Only the reproduced checksum observation is admitted here.

No independent exterior review is recorded for PR #81's final hardened head. The exact-head review comments for PRs #81 and #82 are tool-assisted recomputation records, not independent human review or GitHub-native approval. Mac McFall / M87's earlier review remains limited to PRs #63 and #64 and is not extended to these changes.

## Residuals

1. The Sequence Surface hash chain detects uncoordinated divergence but cannot defeat coordinated resealing of all mutually consistent artifacts.
2. A path-and-digest authorization anchor proves byte identity and declared semantics, not signer identity, institutional authority, or cryptographic authenticity.
3. The checksum manifest proves agreement for its 51 declared entries only; it does not establish repository-wide completeness or semantic truth.
4. Earlier green workflows did not evaluate the root manifest. This gap is closed prospectively by the new cross-platform workflow, not retroactively.

## Execution boundary

At base commit `0bac4f60986e0be4da53d6b69c49aab1f7e73e7d`, the deterministic state remains `DRIFT_CLASSIFIED_RETRY_NOT_AUTHORIZED`; Pair-001 remains `STRUCTURALLY_READY_EXECUTION_BLOCKED`, `executable=false`, and has zero repetitions. The instrumentation release anchor is published, but provider validation remains unsatisfied.

This anchor performs zero provider calls, supplies no uppercase or lowercase retry authorization, promotes no readiness, and executes no Pair-001 request. Passing the 24-hour threshold is necessary for an authorized uppercase retry but is not itself authorization.

## Non-claims

This anchor does not certify security, compliance, legality, safety, truth, manifest completeness, production readiness, signer identity, institutional authority, or independent human review. It does not authorize a provider call, a retry, or Pair-001 execution, and it transfers no authority from elapsed time, publication, recomputation, review, merge, or admission.
