# Independent Verification Report â€” Boundary-State Interoperability Checker v0.1.1 / Evidence Packet v0.1.1

Generated: 2026-07-07T11:53:07Z
Verifier role: foreign verifier (fresh environment, no access to prior run state)
Inputs: `boundary_state_interop_checker_v0_1_1.zip`, `boundary_state_interop_evidence_packet_v0_1_1.zip` as uploaded

## Scope

This is a recomputation pass over the two uploaded artifacts, followed by an
adversarial extension answering the two open questions in
`docs/INDEPENDENT_REVIEWER_NOTE_v0_1_1.md` that the shipped evidence doesn't
yet address (Q5, Q6). Everything below was re-executed in this environment
from the uploaded zips â€” nothing here is taken on the word of the packaged
receipts.

## 1. Integrity verification (SHA256)

| Check | Result |
|---|---|
| Evidence packet top-level `SHA256SUMS.txt` (87 entries) | **87/87 OK** |
| `checker_v0_1_1/SHA256SUMS.txt`, verified from extracted `source_artifacts/boundary_state_interop_checker_v0_1_1.zip` | **All OK** |
| `adversarial_payload_pack_v0_1_0/SHA256SUMS.txt`, verified from extracted source zip | **All OK** |
| `source_artifacts/*.zip` hashes vs. `EVIDENCE_PACKET_MANIFEST_v0_1_1.json` | **All 3 match exactly** |
| Standalone uploaded checker zip vs. checker embedded in evidence packet's `source_artifacts/` | **Byte-identical** (`diff -rq` empty; `check_boundary_state_interop_v0_1_1.py` sha256 `18fc4b93â€¦1d21dcf` in both) |

No tampering, substitution, or drift between the two uploaded files. The
standalone checker you sent is exactly the checker the evidence packet's
hash chain refers to.

## 2. Suite reproduction

Ran the exact commands in `docs/REPRODUCTION_GUIDE_v0_1_1.md` against the
checker extracted from `source_artifacts/`, `jsonschema` installed fresh:

| Suite | Claimed | Reproduced | Receipt match |
|---|---|---|---|
| Canonical (`profile_v0_1_4/fixtures`) | 18/18 | **18/18** | byte-identical to `receipts/canonical_run_receipt_v0_1_1.json` (sha256 match) |
| Adversarial (`adversarial_payload_pack_v0_1_0/payloads`) | 15/15 | **15/15** | byte-identical to `receipts/adversarial_run_receipt_v0_1_1.json` (sha256 match) |
| Reviewer regression (`reviewer_regressions/fixtures`) | 1/1 | **1/1** | byte-identical to `receipts/reviewer_regression_run_receipt_v0_1_1.json` (sha256 match) |

"Byte-identical" means the full `--json` output, not just the pass count â€”
every `violation_type`, `details` string, and outcome matches the shipped
receipt exactly.

## 3. Methodology probes

- **Accept-outcome echo probe**: ran `RWF_PROBE_accept_outcome_must_not_echo_expected_v0_1_1.json` directly. Computed `outcome` is `ATTESTATION_REFERENCED_AS_EXISTENCE_EVIDENCE_ONLY`; the fixture's poisoned `expected_checker_result.outcome` (`RWF_SHOULD_NOT_BE_ECHOED`) is not echoed. Field-for-field match against `receipts/accept_outcome_echo_probe_receipt_v0_1_1.json`. **Confirmed.**
- **PYTHONHASHSEED determinism probe**: ran fixture `13_invalid_authority_alias_reference_v0_1_4.json` under `PYTHONHASHSEED=1,2,3` and three separate default-seed invocations (6 runs total). Identical output hash on all 6. Result object matches the packaged `representative_result` field-for-field. **Confirmed.**
- Shipped unit tests (`tests/test_boundary_state_interop_checker_v0_1_1.py`, 2 tests) pass. `tests/test_boundary_state_interop_checker_v0_1_0.py` also passes once its tool module is put on `PYTHONPATH` â€” minor packaging note, not a defect: the `tests/` folder isn't self-contained for that one file (no conftest.py shim), so a reviewer running `pytest tests/` from the checker root without adjusting path gets a collection error on the v0.1.0 file only.

## 4. Independent Reviewer Note â€” answers

Directly answering the six questions in `docs/INDEPENDENT_REVIEWER_NOTE_v0_1_1.md`, each checked against actual execution rather than the source code alone:

| # | Question | Answer |
|---|---|---|
| 1 | Does RWF_ADV_A now reject for the right semantic reason? | **Yes.** Rejects via `NONOPERATIVE_EXTENSION_FIELD_CONTAINS_PROTECTED_SEMANTICS` on the `x-review.review_note` text specifically â€” confirmed by re-running, not just reading the receipt. |
| 2 | Are accepted outcomes computed independently of `expected_checker_result.outcome`? | **Yes.** `_accepted_outcome()` derives outcome only from `declared_boundary_effect` / presence of `extensions`; confirmed the echo probe's poisoned value is ignored. |
| 3 | Are authority-alias violation details deterministic across `PYTHONHASHSEED`? | **Yes.** `_authority_alias_violations` selects the fragment via `sorted(fragments, key=lambda f: (-len(f), f))`, a total order independent of set iteration order. Confirmed identical output across 6 runs / 4 distinct seed conditions. |
| 4 | Do the canonical and adversarial suites continue to reproduce? | **Yes.** 18/18 and 15/15, byte-identical to shipped receipts. |
| 5 | Does the stronger paraphrase lint over-reject any legitimate non-operative metadata? | **Yes â€” demonstrated.** See Â§5. |
| 6 | Are there additional schema-valid paraphrases that should become reviewer-generated regression payloads? | **Yes â€” demonstrated.** See Â§5. |

Questions 1â€“4 were answerable from the shipped evidence plus recomputation.
Questions 5â€“6 were open, so I built test cases rather than reason about it
abstractly.

## 5. New findings (adversarial extension beyond the shipped evidence)

Both findings below come from 9 new fixtures, each a structural clone of
`RWF_ADV_A_nonoperative_extension_genuine_paraphrase_no_trigger_tokens.json`
with only `handoff_id` and `extensions.x-review.review_note` changed â€” so any
behavior difference is attributable solely to that one string. All 9 are
schema-valid (`validation_phase` was `ACCEPT` or `SEMANTIC`, never `SCHEMA`,
for every one). Full fixtures, receipt, and a README are in the attached
`candidate_regression_payloads_v0_1_1` package.

### 5a. Residual paraphrase bypass class (Q6) â€” 5/5 constructed cases bypassed

`PROTECTED_TEXT_PATTERNS` in v0.1.1 is a fixed list of ~20 regexes, expanded
specifically to catch RWF_ADV_A's exact wording ("fully vetted... end-to-end,"
"consider it sound," "cleared for downstream consumption," "without further
gating," "may proceed on this basis"). It's pattern-matching against known
phrasing, not a general semantic detector, so it's bypassable by any
paraphrase outside the list. Five constructed here, none sharing a trigger
word with RWF_ADV_A or with each other:

- *"Nothing further stands in the way here â€” the team gave this a thumbs up and downstream consumers can build on it as final."*
- *"This has cleared every internal checkpoint, and there's no reason to hold it back before downstream teams start using it."*
- *"We're comfortable putting this in front of downstream consumers exactly as-is; no additional sign-off is needed on our end."*
- *"This one's good â€” ship it downstream, no notes."*
- *"It meets the bar we hold internally, so treat it as settled and move forward with it downstream."*

All 5: `HANDOFF_ACCEPTED` / `DECLARED_NONOPERATIVE_EXTENSION_METADATA_IGNORED_FOR_POSITIVE_VALIDATION`,
zero violations. A sanity control (candidate-B text with the literal word
"reliance" appended) was correctly rejected, confirming the lint path is
actually exercised and these 5 aren't a harness artifact.

### 5b. Over-rejection / false-positive class (Q5) â€” 4/4 constructed cases wrongly rejected

The same regexes match on bare word boundaries with no surrounding-context
check, so ordinary technical usage of a trigger word in an unrelated sense
also rejects:

| Benign text (unrelated meaning) | Word that fires | Result |
|---|---|---|
| "...the payload is JSON-schema **compliant**; timestamps use RFC 3339 format." | `compliant` | Rejected |
| "...the request URI's **authority** component must include the port when non-default." | `authority` | Rejected |
| "The example below is syntactically **correct** JSON..." | `correct` | Rejected |
| "The retry_enabled flag in this example is set to **true** for illustration only." | `true` | Rejected |

All 4: `HANDOFF_REJECTED` / `UNDECLARED_EXTENSION_SEMANTIC_EXPANSION_ATTEMPTED`
via `NONOPERATIVE_EXTENSION_FIELD_CONTAINS_PROTECTED_SEMANTICS`, even though
none of these sentences assert anything about the handoff's reliance,
approval, or compliance status.

### Framing

Both are the same root cause from opposite directions: `_value_has_protected_semantics`
is a bare regex-over-free-text match with no subject/context disambiguation
(no check that the protected term is actually predicated of the handoff
itself). That architecture will always trade off recall against precision â€”
tightening it to catch more paraphrases (5a) will tend to catch more
technical false positives too (5b), and vice versa, unless context-scoping is
added. `03_CHECKER_REQUIREMENTS_v0_1_4.md` requires only that the checker
"scan the field value for protected semantic language" â€” the specific
pattern list is a checker-layer choice, not a frozen-profile constraint, so
there's room to iterate here without touching Profile v0.1.4. I'm not
proposing a specific fix; that's an architecture call for you to make. Two
directions worth weighing, for what it's worth: requiring the matched term to
co-occur with self-referential language about the handoff/payload itself
(cuts 5b, doesn't fully close 5a), or accepting that free-text semantic
linting is inherently open-ended and formally scoping this pass as
best-effort/non-exhaustive in the checker's own non-claims rather than
implying phrase-list coverage is the target state.

## 6. What this does not establish

Same posture as your own `NON_CLAIMS_v0_1_1.md`: this does not establish that
the checker is broken, unsuitable for its stated private-research/prototype
scope, or that 9 constructed cases characterize the full paraphrase space in
either direction. It documents concrete, reproduced, schema-valid cases for
triage â€” the same status RWF_ADV_A had before it became a v0.1.1 regression
fixture.

## Deliverables

- This report.
- `candidate_regression_payloads_v0_1_1/` â€” 5 bypass candidates, 4
  false-positive candidates, a receipt of the actual run against unmodified
  v0.1.1, `SHA256SUMS.txt`, and a README, structured to drop into
  `reviewer_regressions/` the way RWF_ADV_A was.
