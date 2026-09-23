# LS-MDRC-002 construction freeze 001: reconciliation observation 001

Date: 2026-09-23. Disposition: **PRESERVED_WITH_UNRESOLVED_FREEZE_IDENTITY_DISCREPANCIES**.
PR #162 remains unmerged. This observation records discrepancies and a new diagnostic
execution; it neither repairs nor qualifies the historical construction freeze.

## Coordinates and preservation

- Original PR: https://github.com/RecomputableEvidence/fork-public-evidence/pull/162
- Exact original commit: `ca28599b7ca411060e1fc3667ef97596244ed9bb`.
- Preservation branch: `preservation/pr162-construction-freeze-001-ca28599`, created
  at that exact commit. The commit ID is authoritative; a branch name alone is mutable.
- Original package: `docs/experiments/lens-shift-mdrc-002/` at that commit.
- Source-evidence commit: `2dab684fc904f43ca0d35d1c1bbc500e92156ec4`.
- Historical admission base: `d9e17deefec2b844e5f5b82c84986e085e077d58`.
- This reconciliation branches from merged main `760ca57e02f252327c4b138c9c72e37ed3c65915`.

No original package file, receipt, manifest, PR branch, rubric, or source commit
was changed. All 30 original blobs are bound by path, Git blob ID, byte length,
and SHA-256 in `OBSERVED_PACKAGE.json`. The additional preservation branch retains
the original commit and its history even if the working PR branch is later deleted.
Neither branch preservation nor admission of this observation establishes freeze validity.

## Findings

| Item | Declared | Observed | Disposition |
| --- | --- | --- | --- |
| Original manifest verification | Freeze receipt: 28 entries checked, all verified | Manifest contains 29 entries; 28 match, one does not | Historical all-verified assertion not established for committed bytes |
| `receipts/testing/TEST_RECEIPT.json` | SHA-256 `c246327a96573c2c702293cb5b2efc56db8efd734077a5f13cf8f7edb76f9077` in manifest and freeze receipt | SHA-256 `4d4d89c77693b75442ef1d782e59bbf4827cf8468fb3b7582fa19d10019f03a4` | Unresolved historical receipt identity |
| `SHA256SUMS` | Freeze receipt binds `18471330226efaf12ef7b49dfd76a6026d1ebbd2fa81b132e2785522438237b7` | Raw committed bytes hash to `0b4776cda0c476230cde0d93b62f37a4eaa0e0439712f0e13eb3a911aef6f8dd` | Unresolved historical manifest binding |
| Physical population | Explicit including/excluding fields: 30/29 | 30 files including manifest; 29 excluding it | Explicit counts match |
| Unsuffixed population count | `package_population_count: 29` | Associated list has 30 entries, including manifest, and exactly matches tracked paths | Inconsistent field; no missing tracked file inferred from this count alone |
| PR body component tally | 7 ordinary fixture files, plus sentinels and holdout manifest | 6 ordinary fixture files, 3 sentinels, 1 holdout manifest | Listed PR components total 31; actual population is 30. File counts must not be confused with conceptual fixture counts |

The original manifest has a UTF-8 BOM. Parsing uses `utf-8-sig`; hashing always
uses exact raw bytes, including the BOM. The BOM is not counted as a second hash
mismatch. The manifest covers all other package files exactly once.

The freeze receipt binds the manifest while the manifest binds the freeze receipt.
The receipt's own key binding is prose referring back to the manifest, not a digest.
This circular dependency cannot be repaired by repeatedly regenerating the two
files. Any successor should specify an acyclic binding order and explicit exclusions;
this observation makes no alteration to the original binding scheme.

## What the diagnostic establishes

After reviewing the runner's read/write behavior, the exact 30 source blobs were
materialized into a disposable directory. The unchanged runner was executed with
Python 3.12.14 on Linux, UTF-8 mode enabled. It returned **222/222 passed**, exit 0.
The raw output, new receipt, environment, and comparison are retained alongside this file.

All 222 result records match the committed receipt when compared by unique test ID;
their array order differs. Timestamps and the absolute package path also differ.
Only `receipts/testing/TEST_RECEIPT.json` changed in the disposable copy. The
original Git blobs and holdout manifest remained unchanged. No holdout content was
opened or instantiated, and no MEASURE execution was performed. The manifest's
SEALED declarations do not independently establish the existence or secrecy of
holdout contents outside the reviewed package.

Each manifest entry says its holdout file is committed, but the named HO-001,
HO-002, and HO-003 content files are absent from the 30-file tree. The entries also
omit `opened_at` and `consumed_at`, rather than explicitly storing null values.
These are additional representation gaps, not permission to construct or open holdouts.

This is a separately labeled diagnostic after an integrity mismatch, not completion
of the original recomputation instructions, which direct the operator to stop on
a hash failure. The runner does not verify the package manifest. Its write routine
overwrites the test receipt, so a structural pass cannot establish manifest closure.
The observed overwrite mechanism is compatible with receipt drift, but does not
prove the historical cause, timing, or the freeze receipt's claim of timestamp-only change.

## Provenance and remaining limits

The locally fetched reachable history for this package contains one package commit
and 30 distinct blobs. Neither missing expected SHA-256 identity was recovered
within that scope (`PROVENANCE_SEARCH.json`). Constructor-local files, conversations,
external archives, and unreachable Git objects were not searched. No historical
receipt has been reconstructed or inferred from the expected digest.

The package is absent at both the source-evidence commit and the admission base.
The original instructions' checkout of the source-evidence commit therefore does
not, by itself, retrieve the later construction package. Source evidence and package
identity require separate coordinates. The original recomputation receipt itself
describes the package as untracked at that source coordinate.

The normative prompt §§1–24 is required by the original instructions but is not
included in this 30-file population. The README lists `SPECIFICATION/`, but there
are no tracked files there. Full normative recomputation is consequently not claimed.

The historical first-run failure survives as narrative in the reviewed receipts;
its original failing package and raw run output were not recovered in this review.
The same-Bob-session limitation and AMB-001 through AMB-008 remain unresolved.

Limited runner review also found that the implemented BSR tolerance is `< 0.01`,
where the instructions state `0.001`; T15 checks SEALED status but not the null
timestamps specified in the instructions; and the mutation checks use local
predicates rather than exercising a complete external admission checker. These
observations narrow interpretation of the 222-pass result. They are not a full
rubric audit and do not authorize changes to this frozen object.

## Disposition and next decision

1. Preserve PR #162 and its exact bytes; do not merge it under the original
   `CONSTRUCTED_AND_STRUCTURALLY_CLOSED / RECOMPUTED_MATCH` admission description.
2. Admit this reconciliation only as an observation, if approved. It does not admit
   the original package, resolve its ambiguities, promote standing, or begin MEASURE.
3. If the original receipt and manifest bytes can be supplied, check their exact
   SHA-256 identities and provenance in a subsequent additive record. Finding matching
   bytes would establish identity, not automatically the order or validity of the freeze.
4. If they cannot be recovered, preserve that unresolved fact. A separately named
   successor can use explicit population accounting, separately bound source and
   package coordinates, external run receipts, and acyclic digest bindings. It must
   retain the original discrepancy and receive its own review before qualification.

No rewrite, rebase, squash, reseal, or replacement of the original commit is needed.
No fresh blind-context, scientific-validity, or institutional-reliance claim follows
from the diagnostic pass.

## Verify this observation

From a clone containing this reconciliation:

```sh
git fetch origin preservation/pr162-construction-freeze-001-ca28599
python docs/observations/LS-MDRC-002-FREEZE-001-RECONCILIATION-001/verify.py
```

The verifier reads pinned Git blobs and hashes this observation's artifacts. It
does not run the original suite or modify either package. A successful verification
means the recorded discrepancies are reproduced; it does not mean the original
manifest passes. `SHA256SUMS` here covers every file in this observation except
itself, and is separate from the unchanged original manifest.

For a new diagnostic, create a new disposable detached worktree at the original
commit, run the original runner there, and retain its output externally as a new
observation. Expect its receipt to change. Do not run it in a preserved package
directory or replace this run's retained output with the new run.
