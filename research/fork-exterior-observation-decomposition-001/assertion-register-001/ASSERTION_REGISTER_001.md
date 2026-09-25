# FEOD-001 ASSERTION-REGISTER-001

**Standing:** `INSTANTIATED_FROM_FROZEN_SOURCE`  
**Source:** `SOURCE-REVIEW-001`  
**Source SHA-256:** `6bdde2c51003e024c24ae67cb605785d7a3a92a56be626f2fa431493e7723f98`  
**Source preservation commit:** `273bca9fe9e74d3b2c8e8f310eb2305ccfcf9af7`  
**Source/criteria binding commit:** `58dbec5b85a79f8772005aecf89b6043f430de49`  
**Review-observed coordinate:** `UNRESOLVED_ATOMIC_COORDINATE`  
**Assertions:** `56` (`24` technical-eligible; `32` nontechnical)

Source spans are zero-based UTF-8 byte ranges with an exclusive end offset in the frozen canonical `SOURCE_REVIEW_001.md` bytes.

```text
DECOMPOSED != TRUE
TECHNICAL_ELIGIBILITY != REPRODUCED
RECOMMENDATION_PRESERVED != RECOMMENDATION_AUTHORIZED
EXTERIOR_EVALUATION_PRESERVED != FORK_SELF_STANDING
REVIEW_OBSERVED_COORDINATE != EVALUATION_TARGET_COORDINATE
```

| ID | Class | Technical | Byte span | Mode | Initial standing | Source-derived assertion |
|---|---|---:|---:|---|---|---|
| ER-001 | `REPOSITORY_METADATA_ASSERTION` | YES | `0:67` | `STRUCTURED_EXTRACTION` | `EXTERIOR_TECHNICAL_ASSERTION` | Fork is a single-author (copyright Ryan Feller) research repository |
| ER-002 | `REPOSITORY_METADATA_ASSERTION` | YES | `69:86` | `STRUCTURED_EXTRACTION` | `EXTERIOR_TECHNICAL_ASSERTION` | created June 2026 |
| ER-003 | `REPOSITORY_METADATA_ASSERTION` | YES | `88:104` | `STRUCTURED_EXTRACTION` | `EXTERIOR_TECHNICAL_ASSERTION` | with 631 commits |
| ER-004 | `REPOSITORY_METADATA_ASSERTION` | YES | `106:123` | `STRUCTURED_EXTRACTION` | `EXTERIOR_TECHNICAL_ASSERTION` | no stars or forks |
| ER-005 | `REPOSITORY_METADATA_ASSERTION` | YES | `129:155` | `STRUCTURED_EXTRACTION` | `EXTERIOR_TECHNICAL_ASSERTION` | 18 open PRs against itself |
| ER-006 | `RESEARCH_HYPOTHESIS_DESCRIPTION` | NO | `157:286` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | It proposes that explicit "handoff-state" records reduce unsupported inheritance of claims in AI-assisted institutional workflows |
| ER-007 | `IMPLEMENTATION_INVENTORY_ASSERTION` | YES | `292:415` | `STRUCTURED_EXTRACTION` | `EXTERIOR_TECHNICAL_ASSERTION` | ships Python checkers, JSON schemas, synthetic fixtures, a PowerShell verifier, and a very large volume of governance prose |
| ER-008 | `REVIEW_METHOD_DISCLOSURE` | NO | `555:662` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | I did not clone or execute anything, so this is a structural and editorial review, not a correctness audit. |
| ER-009 | `EXTERIOR_EVALUATION` | NO | `680:733` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | The **non-claim discipline is real, not decorative.** |
| ER-010 | `REPRESENTATION_STATE_ASSERTION` | YES | `734:831` | `STRUCTURED_EXTRACTION` | `EXTERIOR_TECHNICAL_ASSERTION` | Every surface states what it does not establish (truth, compliance, legal sufficiency, authority) |
| ER-011 | `REPRESENTATION_STATE_ASSERTION` | YES | `837:968` | `QUOTED` | `EXTERIOR_TECHNICAL_ASSERTION` | CURRENT_STANDING is candid that the central experiment (Cross-System Claim Handoff) has a blocked baseline and no corpus execution. |
| ER-012 | `EXTERIOR_EVALUATION` | NO | `969:1041` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | Most research repos overclaim; this one is careful to the point of pain. |
| ER-013 | `EXTERIOR_EVALUATION` | NO | `1043:1092` | `STRUCTURED_EXTRACTION` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | The engineering scaffolding is more than a sketch |
| ER-014 | `REPOSITORY_METADATA_ASSERTION` | YES | `1094:1129` | `STRUCTURED_EXTRACTION` | `EXTERIOR_TECHNICAL_ASSERTION` | \~60 checker scripts under `tools/` |
| ER-015 | `REPOSITORY_METADATA_ASSERTION` | YES | `1131:1156` | `STRUCTURED_EXTRACTION` | `EXTERIOR_TECHNICAL_ASSERTION` | a matching `tests/` suite |
| ER-016 | `REPOSITORY_METADATA_ASSERTION` | YES | `1158:1185` | `STRUCTURED_EXTRACTION` | `EXTERIOR_TECHNICAL_ASSERTION` | 11 GitHub Actions workflows |
| ER-017 | `IMPLEMENTATION_BEHAVIOR_ASSERTION` | YES | `1316:1357` | `STRUCTURED_EXTRACTION` | `EXTERIOR_TECHNICAL_ASSERTION` | Checkers emit `--json` and use exit codes |
| ER-018 | `IMPLEMENTATION_BEHAVIOR_ASSERTION` | YES | `1406:1495` | `QUOTED` | `EXTERIOR_TECHNICAL_ASSERTION` | The PowerShell verifier is clean, PS 5.1-compatible, and fails loudly on non-JSON output. |
| ER-019 | `EXTERIOR_EVALUATION` | NO | `1521:1573` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | **The repository is mostly about governing itself.** |
| ER-020 | `REPRESENTATION_STATE_ASSERTION` | YES | `1574:1661` | `STRUCTURED_EXTRACTION` | `EXTERIOR_TECHNICAL_ASSERTION` | CURRENT_STANDING v0.9 is an "overlay" on v0.8, which is preserved at its own PR horizon |
| ER-021 | `REPRESENTATION_STATE_ASSERTION` | YES | `1663:1705` | `STRUCTURED_EXTRACTION` | `EXTERIOR_TECHNICAL_ASSERTION` | there's a snapshot classifying 18 open PRs |
| ER-022 | `EXTERIOR_EVALUATION` | NO | `1784:1997` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | A newcomer has to learn a private vocabulary (preservation without inheritance, observance surface, exterior observers, evidence-boundary surface) before they can find out what a Fork artifact actually looks like. |
| ER-023 | `REPRESENTATION_STATE_ASSERTION` | YES | `1998:2025` | `QUOTED` | `EXTERIOR_TECHNICAL_ASSERTION` | The README never shows one. |
| ER-024 | `RESEARCH_RECOMMENDATION` | NO | `2026:2169` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | The single most valuable addition would be a 20-line example handoff record on the first screen, followed by the one checker that validates it. |
| ER-025 | `EXTERIOR_EVALUATION` | NO | `2171:2234` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | **The root directory is a working tree, not a public surface.** |
| ER-026 | `REPOSITORY_METADATA_ASSERTION` | YES | `2235:2519` | `QUOTED` | `EXTERIOR_TECHNICAL_ASSERTION` | Seventeen `README_*` files sit at the top level alongside `encoding_manual_review.log`, `encoding_repair_manifest.json`, `install_phase2_reconciled_to_repo.ps1`, `remote_mapping_system_v0_1_verification_result.json`, a committed `output/` directory, and both `schema/` and `schemas/`. |
| ER-027 | `EXTERIOR_EVALUATION` | NO | `2620:2685` | `STRUCTURED_EXTRACTION` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | the repo's own boundary between scratch and disclosure is blurry. |
| ER-028 | `ARCHITECTURAL_INTERPRETATION` | NO | `2687:2740` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | **Versioning is done with filenames instead of git.** |
| ER-029 | `REPOSITORY_METADATA_ASSERTION` | YES | `2741:2863` | `QUOTED` | `EXTERIOR_TECHNICAL_ASSERTION` | `check_ai_governance_mapping_record_v0_1.py`, `_v0_2.py`, `_v0_2_1.py`, `_v0_2_2.py` all coexist, each with a paired test. |
| ER-030 | `ARCHITECTURAL_INTERPRETATION` | NO | `2864:2974` | `STRUCTURED_EXTRACTION` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | I understand the intent (older receipts must remain recomputable against the exact checker that produced them) |
| ER-031 | `EXTERIOR_EVALUATION` | NO | `2980:3079` | `STRUCTURED_EXTRACTION` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | it multiplies maintenance surface and makes it unclear which version a reviewer should trust today. |
| ER-032 | `RESEARCH_RECOMMENDATION` | NO | `3080:3190` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | Tags plus a `checkers/` index mapping receipt → checker commit would achieve the same with far less clutter. |
| ER-033 | `ARCHITECTURAL_INTERPRETATION` | NO | `3192:3223` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | **Windows-first verification.** |
| ER-034 | `REPRESENTATION_STATE_ASSERTION` | YES | `3224:3269` | `STRUCTURED_EXTRACTION` | `EXTERIOR_TECHNICAL_ASSERTION` | The "one-command" path is a PowerShell script |
| ER-035 | `REPRESENTATION_STATE_ASSERTION` | YES | `3275:3407` | `STRUCTURED_EXTRACTION` | `EXTERIOR_TECHNICAL_ASSERTION` | the docs explicitly classify running the cross-platform Python commands as "manual reconstruction" rather than "verifier execution." |
| ER-036 | `EXTERIOR_EVALUATION` | NO | `3408:3570` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | That is a distinction most Linux/macOS reviewers will find odd, and it puts the canonical path on the platform least used by the audience the project is courting. |
| ER-037 | `RESEARCH_RECOMMENDATION` | NO | `3571:3673` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | A `python -m fork_verify` or a `Makefile` target that the PowerShell script merely wraps would fix it. |
| ER-038 | `REPRESENTATION_STATE_ASSERTION` | YES | `3675:3714` | `QUOTED` | `EXTERIOR_TECHNICAL_ASSERTION` | **Licensing is "all rights reserved."** |
| ER-039 | `REPRESENTATION_STATE_ASSERTION` | YES | `3715:3883` | `QUOTED` | `EXTERIOR_TECHNICAL_ASSERTION` | `COPYRIGHT.md` grants permission only to run the synthetic fixture and public verifier for recomputation; no modification, redistribution, or derivative implementation. |
| ER-040 | `REPOSITORY_METADATA_ASSERTION` | YES | `3938:3982` | `STRUCTURED_EXTRACTION` | `EXTERIOR_TECHNICAL_ASSERTION` | there is no `LICENSE` file GitHub recognizes |
| ER-041 | `EXTERIOR_EVALUATION` | NO | `3988:4111` | `STRUCTURED_EXTRACTION` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | the README's language about contributors and an "Exterior Observance Experiment" implies an openness the terms don't grant. |
| ER-042 | `RESEARCH_RECOMMENDATION` | NO | `4112:4219` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | State the terms in the README's first section so nobody spends an afternoon on it under a false assumption. |
| ER-043 | `RESEARCH_INTERPRETATION` | NO | `4221:4267` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | **The evidence is structural, not empirical.** |
| ER-044 | `IMPLEMENTATION_BEHAVIOR_ASSERTION` | YES | `4268:4372` | `QUOTED` | `EXTERIOR_TECHNICAL_ASSERTION` | What the checkers verify is that fixtures conform to schemas, checksums match, and required files exist. |
| ER-045 | `RESEARCH_INTERPRETATION` | NO | `4373:4467` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | That supports "this pattern can be specified and recomputed," which the README correctly says. |
| ER-046 | `RESEARCH_INTERPRETATION` | NO | `4468:4628` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | It does not yet touch the actual hypothesis — that these records reduce unsupported inheritance — and the one experiment designed to test it hasn't started. |
| ER-047 | `EXTERIOR_EVALUATION` | NO | `4629:4755` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | The README's phrase "initial evidence consistent with the hypothesis" is doing more work than the artifacts currently justify. |
| ER-048 | `RESEARCH_RECOMMENDATION` | NO | `4801:4993` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | 1. Put a real example artifact and its single validating command at the top of the README; move every disclaimer after it into one linked non-claims doc rather than repeating them per section. |
| ER-049 | `RESEARCH_RECOMMENDATION` | NO | `4994:5154` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | 2. Move root `README_*`, logs, result JSONs, and `install_*.ps1` into `docs/history/` or `scratch/`; merge `schema/` into `schemas/`; stop committing `output/`. |
| ER-050 | `RESEARCH_RECOMMENDATION` | NO | `5155:5278` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | 3. Collapse versioned checkers to one current file per checker, with a receipt→commit table for historical recomputation. |
| ER-051 | `RESEARCH_RECOMMENDATION` | NO | `5279:5374` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | 4. Make the Python entry point canonical and cross-platform; keep the `.ps1` as a thin wrapper. |
| ER-052 | `RESEARCH_RECOMMENDATION` | NO | `5375:5501` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | 5. Add a `LICENSE` file matching `COPYRIGHT.md`, and say plainly in the README that this is source-available, not open source. |
| ER-053 | `RESEARCH_RECOMMENDATION` | NO | `5502:5622` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | 6. Either run the CSH baseline or reword the README to say the hypothesis is untested rather than "initially supported." |
| ER-054 | `RESEARCH_RECOMMENDATION` | NO | `5623:5733` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | 7. Rename or explain the repo name — nothing here is a GitHub fork, and "fork-public-evidence" reads as one. |
| ER-055 | `EXTERIOR_EVALUATION` | NO | `5735:5877` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | The underlying idea — recording what a handoff did and did not carry, in a form later reviewers can recompute — is sound and under-served. |
| ER-056 | `EXTERIOR_EVALUATION` | NO | `5878:5991` | `QUOTED` | `SOURCE_DERIVED_NONTECHNICAL_PROPOSITION` | Right now the repository's own volume and self-referential process are the main obstacle to anyone evaluating it. |

## Unopened successor state

```text
EVALUATION_TARGET_COORDINATES = UNOPENED
R0-R3_REPRODUCTION = UNOPENED
FINDING_DISPOSITIONS = UNOPENED
REPAIR = UNAUTHORIZED
ELG_ADMISSION = UNOPENED
RESEARCH_PROMOTION = UNAUTHORIZED
```
