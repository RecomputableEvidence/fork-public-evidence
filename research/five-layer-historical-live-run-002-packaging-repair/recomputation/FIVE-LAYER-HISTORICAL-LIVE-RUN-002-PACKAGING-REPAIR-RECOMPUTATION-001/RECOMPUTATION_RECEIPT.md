# FIVE-LAYER-HISTORICAL-LIVE-RUN-002-PACKAGING-REPAIR-RECOMPUTATION-001 — Recomputation Receipt

## Subject

- Subject object: `FIVE-LAYER-HISTORICAL-LIVE-RUN-002-PACKAGING-REPAIR`
- PR: `#174`
- Base commit: `81816bc4daaf0db665ed32b467e1516ae13bc0a6`
- Tested subject commit: `243ece21674dd58602787edc88eed43cda6eb59c`
- Tested subject tree: `996a3bb87152818305bb0966fb48a0845e84df94`
- Branch: `research/five-layer-live-run-001-packaging-repair`

## Disposition

**`PACKAGING_COMPLETENESS_RECOMPUTED_PASS__SEMANTIC_RERUN_NOT_PERFORMED`**

No semantic rerun was performed.

## Attempt history

### Attempt 001

Disposition: `LOCAL_EXECUTION_WRAPPER_FAILURE_BEFORE_SUBSTANTIVE_BYTE_EVALUATION`

The first local reconstruction wrapper resolved the output path outside the repository worktree, so the gzip source/output streams were never created. Follow-on stream operations therefore failed. The use of PowerShell's automatic `$input` variable also collided with the intended stream variable.

The subject repository files were not changed. This attempt has no substantive evidence effect.

### Attempt 002

Only the local wrapper was corrected: paths were anchored to `(Get-Location).Path`, and non-reserved stream variable names were used. No repository subject bytes or specifications were repaired.

## Recomputed checks

### 1. PR population and successor boundary — PASS

The tested subject is PR #174 at `243ece21674dd58602787edc88eed43cda6eb59c`. The successor reports exactly four bounded changes:

- `FORMAL_M11_M25_DETECTOR_SPECIFICATIONS`
- `PARENT_COMPILATION_BINDING_AND_RECONSTRUCTION`
- `EXPLICIT_STAGE1A_OFFSET_CONVENTION`
- `REVISED_M21_M25_SELF_AUDIT_STANDING`

The predecessor is not modified; the semantic finding population and Stage 3 adjudication are unchanged; current program standing effect is `NONE`.

### 2. Parent reconstruction and Run 001 cutoff — PASS

Observed reconstruction:

- ordered Base64 parts: `9`
- part sizes: eight × `12560` bytes plus one × `16` bytes
- Base64 characters: `100496`
- decoded gzip bytes: `75370`
- gzip SHA-256: `8c9a6d3d1c0886cce5f0a8639be860ebde44d79c77326ff888024b9ab4be9939`
- reconstructed parent bytes: `334735`
- parent SHA-256: `c9ba196efa8709279d8967716ec690bbc5f3112ab5d38e67683768ebe1f62bbf`
- LF count: `5317`
- logical line count: `5317`
- line 4028: `SOURCE 10: Pasted markdown(20260923-131442).md`
- exact Run 001 prefix: lines `1–4026`
- prefix bytes: `262318`
- prefix SHA-256: `a35124bb73fb3ac81bc01e66c60a68fe875f912f377f9aa02ef617d066f33583`

The prefix was copied from the reconstructed parent by exact byte position; no text decode/re-encode or newline normalization was used for the hash-bearing extraction.

### 3. Formal M11–M25 detector specifications — PASS

The JSON parsed successfully.

- schema: `FIVE_LAYER_DETECTOR_SPECIFICATIONS_v0_1`
- object: `FIVE-LAYER-HISTORICAL-LIVE-RUN-002-PACKAGING-REPAIR`
- detector count: `15`
- unique detector count: `15`
- first: `M11`
- last: `M25`
- expected-vs-observed population difference: none
- application: prospective
- retroactive effect on Run 001: `NONE`

An initial display query requested nonexistent `detector_id` / `failure_class` properties and printed blank columns. The parsed object itself remained valid; inspection was corrected to `fixture_id` / `name`. No artifact repair was required.

### 4. Stage 1A offset convention — PASS

The successor explicitly states:

- source intervals are half-open `[start,end)`;
- the source interval includes a terminal LF when present;
- `verbatim_text` removes terminal LF characters;
- reconstruction uses the bound source interval rather than requiring byte identity between the interval and UTF-8(`verbatim_text`);
- Run 001 is not rewritten.

### 5. Revised M21–M25 self-audit standing — PASS

- M21: `SUPPORTED_WITHIN_RUN001_PACKAGE`
- M22: `NOT_INDEPENDENTLY_CERTIFIABLE_FROM_RUN001_PACKAGE`
- M23: `SUPPORTED_WITHIN_RUN001_PACKAGE`
- M24: `SUPPORTED_WITHIN_RUN001_PACKAGE`
- M25: `NOT_INDEPENDENTLY_CERTIFIABLE_FROM_RUN001_PACKAGE`

Historical self-audit mutation: `false`. Framework-validity effect: `NONE`.

## Freeze boundary

This receipt freezes packaging-completeness recomputation **before any semantic rerun**.

It does not establish semantic detector correctness on arbitrary inputs, blind discovery, independent implementation, independent human standing, formal Stage 3 adjudication, framework validity, prevalence, production readiness, truth, authority, compliance, or deployment readiness.
