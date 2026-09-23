# Recognized program-change accounting v0.1

The required admission gate runs `python scripts/check_standing_freshness_v0_1.py --json` on every PR and main push. The dedicated standing workflow also runs without path filters. Full Git history is required; unavailable ancestry fails the check.

This detector conservatively recognizes byte transitions under `admissions/`, `docs/experiments/`, `registries/`, `receipts/`, `schemas/`, and `tools/`. These paths are a declared recognition scope, not an exhaustive definition of program significance. Purely editorial changes inside the scope also require accounting. Significant events outside it, external service changes, permission changes, reviewer exposure, and unmerged PR updates are not automatically discovered.

The coverage base is bound to the current register's snapshot commit. Starting there, the checker walks every first-parent transition through HEAD, then the working checkout. It checks intermediate changes even when later reverted. At merge commits, the aggregate first-parent diff is the admission boundary; unmerged second-parent intermediate states are outside this detector. Identical repeated before/after transitions are deduplicated, so this is not an event count or latency metric. File-mode-only changes are outside the blob-change detector; recognized symlinks/submodules fail closed.

Each recognized transition must appear in `PROGRAM_CHANGE_ACCOUNTING_v0_1.json` with:

| Field | Meaning |
| --- | --- |
| `path` | Exact recognized repository path |
| `before_git_blob` | Previous Git blob SHA; null for addition |
| `after_git_blob` | New Git blob SHA; null for deletion |
| `disposition` | `INCORPORATED`, `EXPLICITLY_DEFERRED`, or `IN_FLIGHT` |
| `reason` | Nonempty explanation of the bounded change and treatment |
| `standing_reference` | Existing document under `docs/current-standing/` explaining it |

The checker rejects missing, duplicate, stale, or fabricated transition keys. A future PR can identify transitions with `recognized_transitions(root, base)` from the checker module, then add explicit accounting and its standing explanation. The checker does not generate classifications. `IN_FLIGHT` means the underlying research process remains unresolved; it does not mean a merged file is unmerged. Open PR #165 is separately pinned in v0.8 and is not part of the admitted transition population.

The initial accounting has no post-base recognized transitions because this repair changes the interpretation/checking layer, not experimental records. PR #161/#163/#164 are explicitly accounted for in v0.8. The observation is committed before v0.8 and the checker verifies its exact manifest population and bytes against that preservation commit. Preserve both commits when merging this repair; squash would remove the ancestry needed to verify the sequence.

Future standing successors must explicitly bind a new coverage base and preserve prior registers/accounting history. Updating coverage is a reviewed interpretation event, not an automatic reset. No machine check establishes whether a deferral is substantively justified or the interpretation semantically adequate. This version is bound to the v0.8 observation; a later successor requires an explicit checker/routing update, not silent mutation of v0.8.

```text
ACCOUNTED_FOR != SEMANTICALLY_COMPLETE
PRESERVATION != SYNCHRONIZATION
PRESERVED != CURRENTLY INTERPRETED
CURRENTLY INTERPRETED != CURRENTLY REPRESENTATIVE
```
