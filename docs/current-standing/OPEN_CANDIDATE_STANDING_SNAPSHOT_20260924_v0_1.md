# Open Candidate Standing Snapshot — 2026-09-24

Observation coordinate: `2026-09-24T23:47:00Z`  
Repository: `RecomputableEvidence/fork-public-evidence`  
Main at observation: `115992d750f0e893d07b61dbb6d584c87dc64d5d` (merge of PR #178)  
Open pull requests observed: **18**

This is a representational snapshot of GitHub open-candidate state. It does not alter any source PR and does not infer standing from open status, draft status, mergeability, chronology, adjacency, or branch location. The machine-readable companion is [`OPEN_CANDIDATE_STANDING_SNAPSHOT_20260924_v0_1.json`](OPEN_CANDIDATE_STANDING_SNAPSHOT_20260924_v0_1.json).

## Classification vocabulary

- **ACTIVE_GATE_BLOCKED** — the open PR still corresponds to a current gate, but the gate remains unsatisfied.
- **EVIDENCE_ONLY_RECONCILIATION** — the PR preserves or explains evidence without promoting the underlying object.
- **EXTERIOR_REVIEW_PENDING / EXTERIOR_RECOMPUTATION_UNRESOLVED** — the declared next evidence-bearing event remains an exterior return.
- **EXTERIOR_DEPENDENCY_HOLD** — progression is intentionally withheld pending separately produced external material.
- **HISTORICAL_COORDINATE_SNAPSHOT** — the PR is a dated coordinate record, not a merge queue.
- **HISTORICAL_HOLD_CLOSED_OBJECT / HISTORICAL_HOLD_RECONCILIATION_OPEN** — later repository records control interpretation of the older open description.
- **PROOF_PACKAGING_REVIEW_UNRESOLVED** — bounded source evidence has been separately admitted, but proof packaging remains unresolved.
- **SUPERSEDED_BUT_PRESERVED** — a later correction/review lineage exists; the older PR remains preserved but is not the active merge target.
- **INTENTIONALLY_UNRESOLVED** — no automatic continuation or disposition is inferred.

## Snapshot

| PR | Exact head | Snapshot classification | Repository-bounded basis |
| ---: | --- | --- | --- |
| #65 | `479de5f929cb37377ccba5ef93f7a4f7b93e1120` | PROOF_PACKAGING_REVIEW_UNRESOLVED | PR #123 admitted bounded source evidence on `preservation/clean-continuance-v0.1`; direct merge was not selected and proof packaging remains not admitted. |
| #84 | `46fcd2c2580abd86ffbe215e6c387fee2bcb1b39` | SUPERSEDED_BUT_PRESERVED | Later PROOF-005 v0.2 correction lineage preserves the historical #84/#86 review record through separately named successors. |
| #86 | `f72ca3fad82bee068527fe63eaf1c8eba87dd698` | SUPERSEDED_BUT_PRESERVED | Later PROOF-005 v0.2 correction lineage preserves the historical #84/#86 review record through separately named successors. |
| #100 | `cdb757a97c2e554cf3df822e4764ac51122ca8eb` | PROOF_PACKAGING_REVIEW_UNRESOLVED | PR #123 admitted bounded source evidence on the preservation branch; direct merge was not selected, proof packaging is not admitted, and live adapters remain closed. |
| #110 | `c6cd61270bac4938878df06f0085089c8f61b9dc` | EXTERIOR_RECOMPUTATION_UNRESOLVED | Exterior recomputation and a separate merge disposition remain required; PR #121 gives #110/#111 no pilot, production, or proof standing. |
| #111 | `042f3e1a46d60abe5b5a52d432aa0b47d2606939` | EXTERIOR_RECOMPUTATION_UNRESOLVED | Exterior recomputation and separate admission/deployment authorization remain required; PR #121 gives #110/#111 no pilot, production, or proof standing. |
| #112 | `052a7dcf7febb2d213c3a94dae4c89d2bab4dceb` | HISTORICAL_COORDINATE_SNAPSHOT | The PR declares itself a temporal snapshot rather than a merge queue. |
| #124 | `4ce0413e70fc9355c1319d7e25b5157497faa90c` | SUPERSEDED_BUT_PRESERVED | PR #125 preserved an exterior return with correction required; PR #126 is the bounded successor. |
| #126 | `a8b528be8acaa5b69bc928450001a56b4b8335e3` | SUPERSEDED_BUT_PRESERVED | PR #127 preserved the successor exterior return and residuals; PR #128 followed. |
| #128 | `9e3cdd2fb6d67f9abd6233ce673341bd817d6338` | SUPERSEDED_BUT_PRESERVED | PR #131 preserved completed executable exterior recomputation; direct merge was not selected and PR #132 is the F3 successor. |
| #132 | `92fd0719c5244b58bec71302491d971cc7e691de` | EXTERIOR_REVIEW_PENDING | Exact-head review, freeze, exterior delta recomputation, preserved return, and separate disposition remain required before merge. |
| #133 | `53db708a9f6b45b8c0210fe8c830bd671f3a9b7f` | EXTERIOR_DEPENDENCY_HOLD | Blind reciprocal comparison remains gated on independently produced external records. |
| #135 | `0280a9f32f45074ef29625f9c31ea178685a6ddf` | INTENTIONALLY_UNRESOLVED | Candidate outward-charter standing does not self-admit or become merge-authorized from structural validity. |
| #152 | `db8b02280ef88e002db6c8ffc3e9e139e4c5925b` | HISTORICAL_HOLD_CLOSED_OBJECT | PR #154 admitted FREEZE-002 as `CLOSED_HISTORICAL_EVIDENCE` and prohibits further modification/reseal/pressure under that object identity. |
| #153 | `57119a3acb270e394461cb70f4dd31a735fa0356` | HISTORICAL_HOLD_CLOSED_OBJECT | PR #154 admitted FREEZE-002 as `CLOSED_HISTORICAL_EVIDENCE` and prohibits further modification/reseal/pressure under that object identity. |
| #162 | `ca28599b7ca411060e1fc3667ef97596244ed9bb` | HISTORICAL_HOLD_RECONCILIATION_OPEN | PR #167 preserved receipt/manifest/population discrepancies and explicitly did not admit or qualify the freeze; #168 is an evidence-only follow-up. |
| #165 | `e3eabe49a7aa4eb9ec3fa451e16bae671fada19b` | ACTIVE_GATE_BLOCKED | The recorded Mistral/OpenAI 429 responses are access observations only; receiver registry and run order remain unfrozen and corpus execution is not established. |
| #168 | `0165314b15b2dc835a8653dd9afd406260ff7d42` | EVIDENCE_ONLY_RECONCILIATION | Records the LF-to-CRLF digest relationship and scoped source-search outcome without reseal, MEASURE, holdout opening, or automatic successor. |

## Cross-branch nuance for #65 and #100

PR #123 merged to `preservation/clean-continuance-v0.1`, not `main`. It admits the bounded recomputation returns as **source evidence** for PROOF-002/#65 and PROOF-004/#100 while explicitly leaving direct merge unselected and proof packaging not admitted. This snapshot preserves that distinction rather than treating the still-open PRs as if their source-evidence gate were still pending or as if preservation-branch source-evidence admission were a `main` proof admission.

## Run 005 boundary

At the repository coordinate used for this snapshot, PR #178 records `EXTERNAL_ADJUDICATION_DISPATCH_PREPARED_NOT_RETURNED`. No external result is represented as repository-preserved or admitted, Stage 3 gains no adjudication, and the synthetic lane remains unopened. Any off-repository return is outside this snapshot until separately preserved.

```text
OPEN != CURRENT_STANDING
OPEN != REVIEW_PENDING
MERGEABLE != MERGE_AUTHORIZED
SOURCE_EVIDENCE_ADMITTED != PROOF_PACKAGING_ADMITTED
PRESERVATION_BRANCH_ADMISSION != MAIN_BRANCH_ADMISSION
OFF_REPOSITORY_RETURN != REPOSITORY_STANDING
```
