# FIVE-LAYER-HISTORICAL-LIVE-RUN-001-PACKAGING-REPAIR-001

**Object class:** successor packaging/reproducibility repair  
**Predecessor modified:** no  
**Run 001 corrected in place:** no  
**Status:** `SUCCESSOR_PACKAGING_REPAIR_OPEN`  
**Next gate:** `SEPARATE_RECOMPUTATION_OF_SUCCESSOR_PACKAGING_REPAIR`

This successor introduces exactly four bounded changes discovered by the separate recomputation. It does not add a new semantic finding population or Stage 3 adjudication.

## 1. Formal M11–M25 detector specifications

Global detector states are:

- `TRIGGERED`
- `CRITERIA_NOT_SATISFIED_IN_EVALUATED_SCOPE`
- `EVALUATION_ABSTAINED`

A trigger is a measurement event, not model failure or contemporaneous protocol violation. A scoped non-trigger is not global absence. Insufficient ontology mapping requires abstention rather than a valid non-trigger.

| ID | Failure class | Formal decision rule |
|---|---|---|
| M11 | Spec-to-execution equivalence | Trigger only when executed standing is asserted from declaration/specification support without required execution evidence; abstain when declared/executed/reconstructed basis is unresolved. |
| M12 | Surface boolean collapse | Trigger when a surface that requires non-binary states is represented only by boolean satisfaction at that surface; abstain if a required companion state field may preserve the distinction but its binding is unresolved. |
| M13 | Uncertainty promoted to violated | Trigger only when a preserved rule or concrete transition maps UNDETERMINED/UNMEASURABLE/unreached standing to VIOLATED; architectural risk alone is insufficient. |
| M14 | Structured-role set operator without declared semantics | Trigger when structured proposition vectors/tuples receive subset, superset, intersection, or empty-set semantics without a declared set denotation or boundary-scoped ordering relation. |
| M15 | Retroactive native identity | Trigger when later reconstruction is assigned contemporaneous native standing without separately preserved native evidence. |
| M16 | Implementation promoted to execution | Trigger when static implementation supports an executed/enforced claim while invocation, execution, or operational-effect evidence required by the claim is absent. |
| M17 | Non-violation promoted to conservation | Trigger when CONSERVED/TRUE is asserted while required operational surfaces are blocked, unexecuted, not evaluated, or unresolved. |
| M18 | Concept-schema state mismatch | Trigger when an operative analytical state is absent from the governing schema enum or otherwise unrepresentable at the required schema location. |
| M19 | Analytical identifier collision | Trigger when the same identifier denotes both historical artifact representation and analytical reconstruction in the same evaluated context without explicit disambiguation. |
| M20 | Execution-only equivalence | Trigger when full boundary equivalence is inferred from execution-transition equivalence without separately establishing evidentiary equivalence. |
| M21 | Example receipt promotion | Trigger when a binding-shaped hash/offset/receipt is presented as empirical even though preserved provenance establishes it was illustrative/unexecuted or not computed from the bound bytes; abstain if computation provenance is unresolved. |
| M22 | Target-conditioned extraction | Trigger when Stage 1A structural extraction itself is semantically filtered, or when conditioned Stage 1B selection lacks a separate selection record naming query/scope. Documented conditioning prevents silent selection leakage but does not establish selection neutrality or epistemic independence. |
| M23 | NOT_ESTABLISHED collapsed to false | Trigger when unknown/unadjudicated/not-performed standing is encoded as boolean false where false carries substantive negation. |
| M24 | Non-trigger promoted to absence | Trigger when a scoped non-trigger/criteria-not-satisfied result is used to assert global absence beyond evaluated scope. |
| M25 | Mapping-detection collapse | Trigger when detector evaluation lacks a separately identifiable mapping state/reference and mapping failure or unknown can flow to a valid non-trigger. Procedural separation does not by itself establish epistemic independence. |

M11–M20 formalize the later Source-12 descriptions in the supplied parent compilation. M21–M25 are successor formalizations of the Source-13 matrix and therefore do not claim these exact executable decision rules existed during Run 001.

## 2. Parent compilation and binding

The exact supplied parent compilation is preserved through a deterministic gzip + Base64 transport representation so the repository can carry the full parent without silently truncating large text writes.

Expected reconstructed parent:

- bytes: `334735`
- lines: `5317`
- SHA-256: `c9ba196efa8709279d8967716ec690bbc5f3112ab5d38e67683768ebe1f62bbf`

Transport representation:

- gzip compression level: `9`
- gzip `mtime`: `0`
- gzip filename: empty
- gzip bytes: `75370`
- gzip SHA-256: `8c9a6d3d1c0886cce5f0a8639be860ebde44d79c77326ff888024b9ab4be9939`
- Base64 characters: `100496`
- Base64 alphabet: RFC 4648 standard alphabet
- Base64 part files contain no inserted line terminators.

Reconstruct by concatenating the following ASCII part files in ascending order with **no inserted separators**, Base64-decoding the result, then gzip-decompressing the decoded bytes:

| Part | ASCII bytes | SHA-256 |
|---|---:|---|
| part-001.b64 | 12560 | `0bf73f1c1e29ba1af1364bf7cd5b1fe08c0ac5e1fd60712604b23d0610b2af4b` |
| part-002.b64 | 12560 | `c4a82651b17f0adae5fa70de8ac71fc1f00b5ffc49d11f2c245e762a79bbf9b9` |
| part-003.b64 | 12560 | `c59668f016a15a45db38d5edee36cc1fd6c6820114e66dd05bc4e9ab1e63ac43` |
| part-004.b64 | 12560 | `5d42f632b83aea5150a67f0de91eef6188fa9ad3c61fae650080098f9aa9ef61` |
| part-005.b64 | 12560 | `5a7d52135fcb2f9ac7899b375d934adf7a52c98eca3ae8317b489c9ae49aeeb6` |
| part-006.b64 | 12560 | `626077dd5d331c7886fe3ef4c0af8d712f66cd74d52e859e4559a3121f2a7be3` |
| part-007.b64 | 12560 | `66dd32da0de3f9ee07b47a75c658d3360526ccd5f2b8ed7e7c80d521579a2cba` |
| part-008.b64 | 12560 | `d6f8c8968877f877e53a34f5d3f4c89384b3086cba055e6884a62932af309b8e` |
| part-009.b64 | 16 | `5d70b9eac1627277d4b689373024e8d3012a602577e9762f433ff31c23da4b25` |

The decompressed bytes must equal the parent identity above.

Run 001 target extraction is the concatenation of parent lines 1–4026 inclusive with original UTF-8 line endings:

- target bytes: `262318`
- target SHA-256: `a35124bb73fb3ac81bc01e66c60a68fe875f912f377f9aa02ef617d066f33583`

The reconstructed parent establishes the Source-10 marker at line 4028:

`SOURCE 10: Pasted markdown(20260923-131442).md`

This repairs package verifiability of the cutoff. It does not establish original standalone-source byte identity; the compilation remains a later transport container.

## 3. Explicit Stage 1A offset convention

Run 001 was reproducible but under-specified at the terminal line delimiter.

Successor convention:

1. `char_start` / `byte_start` are inclusive.
2. `char_end` / `byte_end` are exclusive.
3. `[start,end)` addresses the exact source slice and includes the block's terminal LF when one is present.
4. `verbatim_text` is the addressed source slice with the terminal LF delimiter removed; no other normalization is permitted.
5. Exact reconstruction uses offsets against the Stage 0 source bytes, not equality between `[start,end)` and UTF-8 bytes of `verbatim_text`.

This documents the exposed convention prospectively. It does not modify historical Stage 1A records.

## 4. Revised M21–M25 self-audit standing

The Run 001 self-audit is not rewritten. Its successor standing is:

| Fixture | Successor standing | Basis |
|---|---|---|
| M21 | `SCOPED_NON_TRIGGER_EXTERNALLY_SUPPORTED` | Real computed hashes were used; no illustrative receipt was promoted as empirical. |
| M22 | `NOT_INDEPENDENTLY_CERTIFIED` | `selection_conditioned=true` and a Stage 1B selection record provide provenance, but do not establish selection neutrality or epistemic independence. |
| M23 | `SCOPED_NON_TRIGGER_EXTERNALLY_SUPPORTED` | NOT_ESTABLISHED/abstention standing is preserved rather than collapsed to false. |
| M24 | `SCOPED_NON_TRIGGER_EXTERNALLY_SUPPORTED` | Non-trigger output remains bounded to evaluated scope and is not promoted to global absence. |
| M25 | `NOT_INDEPENDENTLY_CERTIFIED` | Separate Stage 2A/2B records establish procedural separation; the same exposed analyst authored synthesis/mapping, so epistemic independence is not established. |

## Non-claims

This successor does not establish detector correctness, blind discovery, independent implementation, independent human adjudication, framework validity, prevalence, production readiness, or a new historical protocol violation.

Run 001 remains historical evidence exactly as previously emitted. The recomputation remains a separate sibling record with disposition `MECHANICAL_RECOMPUTATION_PASS_SEMANTIC_PRESSURE_FINDINGS_PRESERVED`.
