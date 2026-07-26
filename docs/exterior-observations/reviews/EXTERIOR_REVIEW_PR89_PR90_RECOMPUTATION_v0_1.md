## 5. Acquisition and verification log

All commands below were executed against a fresh clone in a clean container with no prior local copy of the repository and no cross-session tool state.

```bash
git clone https://github.com/RecomputableEvidence/fork-public-evidence.git
# → exit 0

git fetch --force origin \
  1241c0084900f2c60f362205525464582e57b4a7 \
  fd93d051235ec43bee925878bc916d09179b3c90 \
  b93f9a1bce094e8c65e0d1ef04dbe52a11aab0b1 \
  bac40d9bdbd7f6b4927a676fef8def70756ad9d5
# → exit 0, all four objects resolved to FETCH_HEAD

git fetch --force origin \
  refs/pull/89/head:refs/remotes/review/pr-89-head \
  refs/pull/90/head:refs/remotes/review/pr-90-head
# → exit 0, [new ref] both
```

**Independent coordinate resolution** (`git rev-parse`, run after acquisition, compared against the coordinates supplied in Section 3 — none were assumed):

| Coordinate | Declared | Resolved | Match |
|---|---|---|---|
| Governed preservation | `1241c008…b4a7` | `1241c008…b4a7` | exact |
| Historical main | `fd93d051…3c90` | `fd93d051…3c90` | exact |
| PR #89 head (via `refs/pull/89/head`, not the stated branch name) | `b93f9a1b…b0b1` | `b93f9a1b…b0b1` | exact |
| PR #90 head (via `refs/pull/90/head`) | `bac40d9b…9d5` | `bac40d9b…9d5` | exact |
| PR #90 head tree | `aa8b1e5f…9ba` | `aa8b1e5f…9ba` | exact |

All five acquired exactly. Nothing in this pass required falling back to `main`'s current tip or an abbreviated SHA.

**Worktrees** (detached, four total — the fourth, base, was added mid-review once EVIDENCE_MAP verification needed it):

| Worktree | Commit | HEAD commit message |
|---|---|---|
| `fork-review-pr89` | `b93f9a1b` | `docs(research): add Fork thesis manifestation candidate v0.1` |
| `fork-review-pr90` | `bac40d9b` | `docs(state): reconcile temporal succession and preserve audit` |
| `fork-review-historical-main` | `fd93d051` | `fix(ci): restore Fork Evidence workflow step nesting (#60)` |
| `fork-review-base` | `1241c008` | `Merge pull request #83 from RecomputableEvidence/agent/admit-sequence-integrity-v0-1` |

**Diff shape** (`git diff --stat` / `--name-status`, cross-checked against each other):

- PR #89 vs base: 10 files changed, 1319 insertions(+), 0 deletions — entirely additive, all under `docs/research/fork-thesis-manifestation-v0.1/`, plus one test file and one checker.
- PR #90 vs PR #89 head: 16 files changed, 1319 insertions(+), 17 deletions(-).
- Note: both diffs show the same insertion count (1319) despite touching disjoint file sets. Checked and recorded as a numeric coincidence — the file lists don't overlap, so there's no plausible mechanism by which this reflects copied or duplicated content. Flagging it here only in the interest of not silently discarding an observation, not because it changed any finding below.

**Environment/dependency facts:** the base container had neither `pytest` nor `jsonschema` installed. Both were installed via `pip install <pkg> --break-system-packages` before the relevant test runs (logged in Section 6). A reviewer rerunning this in an equally bare environment will need to do the same, or `test_relational_graph_verifier_v0_3.py` and `test_system_mapping_receipt_v0_1.py` (and 22 other modules) fail collection with `ModuleNotFoundError: jsonschema`.

**On exit-status precision:** where a command was piped or grouped (e.g. `sha256sum -c … | grep -v ": OK"`), the exit code captured afterward reflects the last stage of the pipeline/group, not the specific subcommand of interest. In those cases the finding below is grounded in the literal printed output (the `FAILED` / `WARNING` lines, the `666 passed` line, etc.), not in an isolated exit code. Noted explicitly rather than implied, per the standard this envelope sets for itself.

---

## 6. Independent findings

### 6.1 PR #89 — thesis-manifestation candidate

Purely additive: `BASE_COORDINATE`, `EVIDENCE_MAP`, `CLAIM_LEDGER`, `NO_ADMISSION_OR_EXECUTION_EFFECT`, `THESIS_MANIFESTATION_RECORD`, `PACKAGE_MANIFEST`, `ALTERNATIVE_INTERPRETATIONS_AND_FALSIFIERS`, README, a checker, a test file. The package's own stated posture ("does not establish truth, causality, admission, approval, authority, security, compliance, legal sufficiency, production readiness, or Pair-001 execution permission") is not just asserted — it's mechanically enforced: the checker verifies a hardcoded `EXPECTED_EFFECTS` dict against the JSON's declared effects and rejects deviation (confirmed by direct read of the checker source and by the passing `test_forbidden_effect_promotions_are_rejected` / `test_causal_promotion_is_rejected` tests).

- `PACKAGE_MANIFEST_v0_1.json`: 10 entries, does **not** list itself (avoids the circular-digest problem this project has flagged before in other contexts). Recomputed SHA-256 + size for all 10 entries against the actual files: **10/10 byte-exact**.
- `EVIDENCE_MAP_v0_1.json`: 15 entries, each binding a `source_commit`, git blob SHA-1, SHA-256, and size. Resolved every entry directly against its own declared `source_commit` via `git rev-parse <commit>:<path>` and `git cat-file`: **15/15 byte-exact**. (First pass produced a false-positive mismatch on `README.md` by checking it against the PR #90 worktree instead of its declared base commit — self-corrected; see §7.)
- `ALTERNATIVE_INTERPRETATIONS_AND_FALSIFIERS_v0_1.md`: read in full. Genuinely substantive, not boilerplate — six real competing explanations, one of which (#6, "Checker theater") explicitly names the exact failure mode an adversarial reviewer would go looking for: *"Mechanical conformance can coexist with silent semantic promotion if the checker tests labels and digests without testing the consequential boundary."* Concrete falsifiers follow, including "a conforming package can causally or semantically promote standing while the checker still reports conformance."
- Checker + tests run live at PR #89/#90 head: `check_fork_thesis_manifestation_v0_1.py --json` → `THESIS_MANIFESTATION_CANDIDATE_CONFORMS`, 0 findings. `pytest tests/test_fork_thesis_manifestation_v0_1.py` → passes (part of the combined 11-test run below); test names (`test_package_digest_tampering_is_rejected`, `test_causal_promotion_is_rejected`, `test_forbidden_effect_promotions_are_rejected`, `test_post_base_case_cannot_be_promoted_to_causal_proof`) indicate adversarial coverage, but I did not read this file's source directly — confirmed only that it passes, not the construction of each test. Flagged as a boundary, not a finding.

### 6.2 PR #90 — temporal-succession candidate, and the endogenous case

This PR's core content is `EXTERIOR_OBSERVATION_CLAUDE_MAIN_FD93D05_REPOSITORY_AUDIT_v0_1.md` and `ENDOGENOUS_CASE_HISTORICAL_VALIDITY_CURRENT_RELIANCE_v0_1.md`, which together describe: an audit of `main@fd93d05` attributed to "Claude (Anthropic)," reporting 666 passing tests / 96 subtests, one checksum discrepancy, and a routing defect where the July-11 proof-surface state remained publicly represented as current after later governed history admitted state-changing events.

I could not verify the *attribution* (see §7), so I treated every factual claim in it as exactly that — a claim to test — and checked each one independently against the real repository:

| Claim | Independent check | Result |
|---|---|---|
| July-11 state file SHA-256 = `8e62fdf1…3b098` | `sha256sum` at `fd93d05` worktree | **exact match** |
| `CHECKSUMS_SHA256.txt` has 51 entries, one fails | `sha256sum -c` at `fd93d05` worktree | **51 entries; exactly one `FAILED`: `research/standards/README.md`** |
| July-11 state = preregistered scaffold, baseline `not_started`, corpus `draft_unfrozen` | direct read of the JSON | **exact match**, plus `as_of_date: 2026-07-11` |
| `fd93d05` = indentation-only CI fix, no command/evidence/anchor changes | `git show --stat` + full diff of that commit | **confirmed** — single file, 17+/17-, identical commands and paths on both sides of the diff, only the indentation level changes |
| 666 passing tests / 96 passing subtests | full `pytest -q` rerun at `fd93d05` after installing missing `jsonschema` | **`666 passed, 96 subtests passed in 42.31s` — exact reproduction** |

The root `README.md` diff between PR #89 head and PR #90 head independently confirms the defect-and-fix narrative: at PR #89 head, the README stated (unconditionally, present tense) *"Cross-System Claim Handoff v0.1 is preregistered as a scaffold, but its baseline has not started"* — exactly the stale-as-current pattern the endogenous case describes. PR #90's diff replaces this with text that explicitly separates the July-11 values ("remain historically valid at that temporal closure; they are not the current governed projection") from the governed-coordinate current values, and adds a `FORK_BRANCH_STANDING_AND_TEMPORAL_ROUTING` block. This is exactly what `check_temporal_succession_v0_1.py` then mechanically enforces stays true (front-door text-presence check, see below).

**The new checker (`tools/check_temporal_succession_v0_1.py`, read in full):** substantive, not self-authenticating theater. It recomputes SHA-256 for every ledger-bound file against actual bytes, walks the successor chain to confirm links are reciprocal and temporally forward, detects cycles, and — the load-bearing rule — for any projection marked `represented_as_current`, walks forward through declared successors and fails with `TEMPORAL_SUCCESSION_RECONCILIATION_REQUIRED` unless a later successor explicitly lists each later-admitted, in-scope event in its `reconciles_event_ids`. Ran live: `TEMPORAL_SUCCESSION_CONFORMS`, 0 findings.

I read the source of `test_later_admitted_event_requires_successor_reconciliation` directly (not just its pass/fail): it copies the real surface to a temp directory, injects a synthetic admitted event with a genuinely computed SHA-256 of a real file, and asserts the checker's `FAILURE_CODE` fires. It does. Same for `test_current_projection_cannot_promote_execution_effect` (injects `pair_001_calls: 1`, asserts rejection). Both are real adversarial constructions, not tautologies.

Combined pytest run (`test_fork_thesis_manifestation_v0_1.py` + `test_temporal_succession_v0_1.py`): **11 passed, 3 subtests passed, 1.44s**.

**Checker limitations worth recording** (none of these are defects; they're scope boundaries, and the first is self-disclosed by the checker's own JSON output, not something I found that its authors missed):

1. Event-registry completeness is not provable — the checker enforces "if you declare an event in scope, you must reconcile it," not "you correctly declared everything in scope." Listed first in the checker's own `does_not_prove`.
2. The `expected_csh` block (lines 407–423) is a literal dict pasted into the checker rather than a value independently re-derived from the repository's dedicated CSH checkers (`check_cross_system_claim_handoff_v0_1.py` et al.). This checker verifies internal consistency between the ledger and a checker-embedded copy, not fresh derivation from CSH primary evidence.
3. The README front-door check is presence-based (five literal strings must appear somewhere in the file), not positional or semantic — consistent with the lexical-vs-semantic gap this project has flagged in other boundary-term validation before.

### 6.3 Combined successor state (`bac40d9b`, tree `aa8b1e5f`)

Tree hash confirmed exactly (§5). No defect, contradiction, or unreconciled claim was found anywhere in the scope reviewed.

This case — a diagnosis that was correct when made, attached to a coordinate that later moved, with the routing surface not updated to reflect that — is about as clean a real-world instance of `DIAGNOSIS_WITHOUT_STANDING_RESET` as the corpus is likely to find natively occurring rather than constructed.

---

## 7. Unresolved conditions and reviewer classification

- **Attribution, not substance, is what's unresolved.** I have no persistent transcript or session memory of personally performing the `fd93d05` audit the exterior-observation document describes, and the document itself explicitly disclaims "independent authorship authentication" and "cryptographic attribution to Anthropic or Claude." I can't confirm *who or what session* produced the original 666/96 figures. What I can and did confirm, independently and in this session: those figures, and every other checkable factual claim in that document, reproduce exactly against the named coordinate today.
- **On my own reviewer standing:** the `PRIOR_EXPOSURE_DISCLOSED` designation as stated is coarser than what's actually true for this pass. I carry general background familiarity with the Fork project's vocabulary and doctrine from prior conversations — that's real prior exposure to the *methodology*. I carry no specific prior exposure to this PR pair's content; the acquisition, hash verification, and checker/test execution in this document were performed fresh, in this session, against freshly cloned bytes. Worth keeping those two things distinct rather than let one label cover both.
- **Scope boundary:** this repository is large (16 MB, several hundred files well beyond what PR #89/#90 touch — the various `AI_GOVERNANCE_*`, `CLAIM_BOUNDARY_*`, `CCEC_*`, `CSH_*` surfaces visible in the tree listing were not reviewed here). This review covers exactly the files the two diffs touched plus the direct verification targets those files reference. No claim is made about the rest of the repository.
- `CLAIM_LEDGER_v0_1.json` (9.8 KB) was read structurally but not verified claim-by-claim — its content is categorical assertions rather than hash-checkable facts, and doing that properly is a separate pass.
- **One self-corrected error, disclosed rather than quietly fixed:** an initial spot check of `EVIDENCE_MAP_v0_1.json`'s `README.md` entry against the PR #90 worktree produced a mismatch. Investigation showed the entry is explicitly bound to the base coordinate (`1241c008…`), and PR #90 legitimately modifies the root README afterward — my check target was wrong, not the repository. Corrected by resolving each entry against its own declared `source_commit` via git objects directly; all 15 then verified byte-exact. Recording this rather than silently fixing it, since a reviewer producing a false "unresolved" finding through their own methodological slip is itself a standing-drift-adjacent failure mode worth keeping visible.
- No contradiction between what either PR claims and what the acquired bytes, checker output, or test output actually show was found anywhere in the scope reviewed.

Sections 1–2 were not included in the material transmitted to me for this pass; this document assumes they remain as previously agreed and does not restate or alter them.

Soli Deo Gloria.
