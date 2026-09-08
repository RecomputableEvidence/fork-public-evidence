# Fork CAD Exterior Review Packet v0.1

Status: `DRAFT_REVIEW_PACKET_NOT_ADMISSION`

## Review object

Repository: `RecomputableEvidence/fork-public-evidence`

Pull request: `#84`

Base branch: `preservation/clean-continuance-v0.1`

Review only the exact head supplied at handoff. Do not substitute the mutable branch name in the final verdict.

## Review purpose

Determine whether the candidate accurately preserves a mixed conversational review record without:

- converting contextual presence into technical validity;
- converting model self-report into verified causal mechanism;
- erasing supported findings because other findings were contradicted;
- collapsing claim-level standing into project-level maturity;
- representing the exploratory CAD thread as Pair-001 execution;
- converting review, agreement, or a passing checker into admission.

## Public review surface

Review all files changed by PR #84, with special attention to:

- `FORK_CAD_RESEARCH_PROTOCOL_v0_1.md`
- `MODEL_SELF_REPORT_BOUNDARY_v0_1.md`
- `PR_REVIEW_QUESTIONS_v0_1.md`
- `SOURCE_MANIFEST_v0_1.json`
- `SOURCE_MANIFEST_SUPPLEMENT_001_v0_1.json`
- `SOURCE_ROLE_MAP_v0_1.json`
- `SOURCE_ROLE_MAP_SUPPLEMENT_001_v0_1.json`
- `CLAIM_LEDGER_v0_1.json`
- `OBSERVABLE_EVENT_REGISTER_SUPPLEMENT_001_v0_1.json`
- `FINDINGS_AND_NON_CLAIMS_v0_1.md`
- `tools/check_fork_cad_candidate_v0_1.py`
- `tests/test_fork_cad_candidate_v0_1.py`

## Private source package

The raw sources are not published in the repository. The reviewer should receive the exact 21-artifact package through a separately authorized channel.

Before reviewing content, recompute each artifact's SHA-256 and byte length and compare them to the base and supplemental source manifests.

A mismatch produces `SOURCE_PACKAGE_NON_CONFORMING` or `REVIEW_INCONCLUSIVE`; it must not be silently corrected.

## Clean-clone commands

From a clean checkout of the exact head:

```text
python tools/check_fork_cad_candidate_v0_1.py --root .
python -m unittest tests.test_fork_cad_candidate_v0_1 -v
```

If the environment uses a different Python launcher, record the exact command and version. Do not edit the candidate to make the run pass without separately reporting the change.

## Required review questions

1. Do all manifest digests and byte lengths match the private source package?
2. Does every source have a correct and sufficiently narrow declared role?
3. Is the role of `Txtbngsntnscrnshot.txt` preserved accurately?
4. Is the Markdown availability claim contradicted by the visible and later-read record?
5. Is the mocked Fracture concurrency finding supported by the exact Markdown bytes?
6. Is the register-weighted authority finding supported, partially supported, or overinterpreted?
7. Does the candidate avoid claiming knowledge of provider-internal mechanisms?
8. Does it distinguish textual revision from internal standing reset?
9. Does it retain the artifact-grounded PR #84 Pair-001 correction without treating the CAD thread as Pair-001?
10. Does the claim-level vocabulary duplicate, overlap with, or remain distinguishable from existing Fork or Synergenesis maturity vocabularies?
11. Can the checker be bypassed through unknown source references, duplicate source IDs, missing roles, canonicalization flags, or a self-report marked as mechanism-verified?
12. Is any favorable or adverse finding incorrectly accused, overstated, or missing?

## Required verdict

Return one of:

- `REPRODUCED_WITHIN_DECLARED_SCOPE`
- `REPRODUCED_WITH_CORRECTIONS_REQUIRED`
- `NOT_REPRODUCED`
- `REVIEW_INCONCLUSIVE`

The verdict must include:

- exact reviewed head SHA;
- environment details;
- commands and outputs;
- source-package digest result;
- claim-by-claim findings;
- dissent and unresolved questions;
- explicit non-endorsement and no-admission language.

## Effects

Exterior review does not merge, admit, publish, authorize provider calls, change Pair-001 standing, or certify Fork. Any amendment must occur on the candidate branch and receive a new exact-head review. Admission, if later warranted, requires a separate append-only act.
