# Independent Assessment and Recomputation

Package: `FIVE-LAYER-HISTORICAL-LIVE-RUN-001.zip`  
Package SHA-256: `3ec4e66730fd8b6c3ef99803e298285aa959ad3d1b4f2a51813438f1f563cba0`

## Bottom line

The package is mechanically internally consistent. All 11 hashes listed in `SHA256SUMS.txt` verify against the supplied bytes; all JSON files parse; the stage-to-stage input hashes match; the target is exactly 262,318 bytes and 4,026 lines; and the recursive synthesis is exactly 8,812 bytes.

An independent reconstruction of the stated Markdown segmentation reproduces Stage 1A exactly: 45 blocks = 12 headings + 28 prose paragraphs + 5 list items. Applying the declared Stage 1B prefix rule independently selects exactly nine blocks, `F01` through `F09`, leaving 36 excluded blocks.

Stage 2B's recorded outcome counts also recompute arithmetically to 3 `TRIGGERED`, 2 `EVALUATION_ABSTAINED`, and 5 `CRITERIA_NOT_SATISFIED_IN_EVALUATED_SCOPE`. Stage 3 contains zero formal adjudications, as reported.

The semantic detector layer is not fully reproducible from this package alone, because no formal criteria/specifications for M11-M25 are supplied—only detector names, mappings, results, and reasons. The semantic reassessment below therefore interprets the detector names and checks the cited evidence directly against Sources 01-09.

## Recomputed mechanical results

| Item | Reported | Recomputed | Result |
|---|---:|---:|---|
| Target bytes | 262,318 | 262,318 | Match |
| Target lines | 4,026 | 4,026 | Match |
| Synthesis bytes | 8,812 | 8,812 | Match |
| Stage 1A blocks | 45 | 45 | Match |
| Headings | not summarized | 12 | Recomputed |
| Prose paragraphs | not summarized | 28 | Recomputed |
| List items | not summarized | 5 | Recomputed |
| Stage 1B selected | 9 | 9 | Match |
| Stage 1B excluded | 36 | 36 | Match |
| M11-M20 triggered | 3 | 3 | Match |
| M11-M20 abstained | 2 | 2 | Match |
| M11-M20 scoped non-triggers | 5 | 5 | Match |
| Formal Stage 3 adjudications | 0 | 0 | Match |

## Integrity checks

- Every entry in `SHA256SUMS.txt` verifies.
- Stage 0 object hashes and byte counts verify.
- Stage 1B correctly binds the actual Stage 1A file hash.
- Stage 2A correctly binds the actual Stage 1B file hash.
- Stage 2B correctly binds the actual Stage 2A file hash.
- Stage 3 correctly binds the actual Stage 2B file hash.
- The nine source markers in the supplied target occur at the declared start lines: 9, 148, 591, 1077, 1430, 1886, 2427, 3006, and 3645.
- No M11-M25 labels occur in the supplied target, supporting the narrow claim that the target prefix itself predates those labels.

What cannot be independently verified from the package is the parent compilation's stated 334,735-byte SHA-256 binding or the assertion that Source 10 begins at line 4028, because the full parent compilation is not included.

## Semantic reassessment of M11-M20

### M14 — `TUPLE_SUBSET_WITHOUT_PARTIAL_ORDER`: TRIGGERED (strong)

Source 09 defines both native and retrospective propositions as structured 4-component vectors/tuples, then defines `ROLE_NARROWED` and `ROLE_BROADENED` using raw subset relations. No set denotation or boundary-scoped partial order is defined first. Under ordinary mathematical typing, subset is a relation on sets, not ordered tuples. The same issue also appears in `ROLE_REINTERPRETED`, which applies set intersection and the empty-set test to those structured proposition vectors. This strengthens F07: the seam is broader than ordering alone and includes undeclared set-operator semantics on structured role vectors.

### M12 — `SURFACE_BOOLEAN_COLLAPSE`: TRIGGERED, with scope caveat

Earlier source material explicitly preserves non-binary boundary states including not expressed, undetermined, blocked upstream, unmeasurable, and expressed ambiguously. Source 09 later requires `surface_satisfaction` to be boolean for each surface evaluation. The boolean field by itself cannot encode those local states. This supports a schema-granularity trigger.

The caveat is that `surface_notes` and `token_interpretation_record_id` could carry additional information outside the boolean field. Therefore the evidence establishes local schema compression, not necessarily irreversible loss throughout the entire data model.

### M18 — `CONCEPT_SCHEMA_STATE_MISMATCH`: TRIGGERED (same underlying seam as M12)

This is supported by the same F08 evidence and is not an independent third defect. There is also a stronger direct mismatch not called out in the supplied synthesis: Source 09's global `global_conservation_status` enum includes `PRESERVED`, `VIOLATED`, `OMITTED`, `UNEXPRESSED`, `EXPRESSED_AMBIGUOUSLY`, and `UNDETERMINED`, but omits earlier explicit states `BOUNDARY_BLOCKED_UPSTREAM` and `BOUNDARY_UNMEASURABLE`. Thus the final schema does not preserve the entire earlier named state space at the global level either.

### M13 — `UNCERTAINTY_PROMOTED_TO_VIOLATED`: EVALUATION_ABSTAINED

The abstention is justified. Rule 3 sends `OPERATIONAL_BINDING` plus `surface_satisfaction=false` to global `VIOLATED`, but the target does not define a concrete mapping from `UNDETERMINED`, `UNMEASURABLE`, or another uncertainty state to boolean false. The schema creates the risk, but an actual uncertainty-to-violation promotion is not established.

### M11 — `SPEC_TO_EXECUTION_EQUIVALENCE`: EVALUATION_ABSTAINED

The abstention is reasonable. Source 09's `Phi^native` mixes role, proposition, execution impact, and evidence, and sometimes uses language such as what a token "natively executed," which makes the boundary worth scrutiny. But the supplied target does not provide a concrete instance where declaration/specification alone is demonstrably promoted to an executed event. F09's `PARTIAL_NOT_ESTABLISHED` status is therefore appropriate.

### M15-M20 other recorded non-triggers

M15, M16, M17, M19, and M20 are consistent with the selected synthesis and cited target passages. Their recorded state should still be read strictly as a scoped non-trigger, not as global absence.

## Unique-seam recomputation

The reported `3 TRIGGERED` detector events correspond to **two unique underlying seams**, not three independent defects:

1. Structured-role operator/ordering semantics: M14 / F07.
2. State-space/schema compression: M12 + M18 / F08.

M12 and M18 are two detector views of the same F08 evidence.

## Assessment of the M21-M25 self-audit

The supplied evidence strongly supports the narrow file-level claims for M21, M23, and M24: real hashes are used; `NOT_ESTABLISHED` is preserved as partial/abstained rather than false; and scoped non-trigger language is preserved.

M22 and M25 should not be independently certified from this package alone. Stage 1B explicitly states `selection_conditioned: true` and selects blocks that were already authored as `FINDING-Fxx` in an analyst-derived synthesis. Declaring that conditioning is good provenance, but it does not make the extraction unconditioned. Likewise, separating mapping and detection into two files demonstrates procedural separation, not epistemic independence: the same exposed analyst produced the retrospective synthesis and mapping with knowledge of the later detector vocabulary. Whether M22 or M25 should formally trigger depends on their missing formal criteria.

## Small implementation issue

Stage 1A's `char_end` and `byte_end` values include the terminal line-feed byte/character, while `verbatim_text` omits that terminal newline. The convention is internally consistent and was exactly reproducible, but it is under-specified. A consumer assuming that `[start,end)` equals the bytes/chars of `verbatim_text` will observe a one-character/one-byte mismatch at each block boundary. The schema should state explicitly whether offsets include the terminating line delimiter.

## Overall assessment

The run is strong as a **dependent retrospective, provenance-preserving analysis** and its mechanical claims recompute cleanly. The supplied evidence supports the stated two concrete historical seams, with F07 actually somewhat broader than described and F08 additionally supported by omissions in the global status enum.

It should not be presented as an independently reproducible detector experiment yet. To reach that standard, the package needs the exact M11-M25 detector specifications/decision rules, the parent compilation (or a verifiable binding to it), and ideally an adjudication/mapping pass by an analyst who did not author the finding synthesis.
