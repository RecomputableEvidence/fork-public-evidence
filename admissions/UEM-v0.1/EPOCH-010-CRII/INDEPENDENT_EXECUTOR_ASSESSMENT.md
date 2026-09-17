# Epoch 010 Independent Executor Assessment

Input handoff integrity: **PASS** — all 88 files listed by the supplied `SHA256SUMS` verified.

Executor result schema: **PASS** against the supplied `EXECUTOR_RESULTS_SCHEMA.json`.

Important interpretation: result `validation` values are not compared to source-record `validation` values because the supplied closed CRII rule registry does not define such an equality rule. Identity is never inferred from position or repaired by alias mapping.

| Fixture | Verdict | Violated rule(s) |
|---|---|---|
| UEM-E10-FX-001 | ACCEPT | — |
| UEM-E10-FX-002 | ACCEPT | — |
| UEM-E10-FX-003 | ACCEPT | — |
| UEM-E10-FX-004 | ACCEPT | — |
| UEM-E10-FX-005 | REJECT | CRII-006 |
| UEM-E10-FX-006 | REJECT | CRII-005 |
| UEM-E10-FX-007 | REJECT | CRII-009, CRII-010 |
| UEM-E10-FX-008 | REJECT | CRII-009 |
| UEM-E10-FX-009 | REJECT | CRII-009 |
| UEM-E10-FX-010 | REJECT | CRII-009 |
| UEM-E10-FX-011 | REJECT | CRII-011 |
| UEM-E10-FX-012 | REJECT | CRII-008 |
| UEM-E10-FX-013 | REJECT | CRII-010 |
| UEM-E10-FX-014 | REJECT | CRII-007, CRII-013 |
| UEM-E10-FX-015 | REJECT | CRII-012 |
| UEM-E10-FX-016 | REJECT | CRII-004 |

## Rejection rationale

- **UEM-E10-FX-005** — CRII-006: source embedded candidate_id does not equal canonical candidate_id.
- **UEM-E10-FX-006** — CRII-005: source filename stem does not equal canonical candidate_id.
- **UEM-E10-FX-007** — CRII-009: result population differs from the manifest population or duplicates an ID; CRII-010: a result record violates the supplied result-record field/schema constraints.
- **UEM-E10-FX-008** — CRII-009: result population differs from the manifest population or duplicates an ID.
- **UEM-E10-FX-009** — CRII-009: result population differs from the manifest population or duplicates an ID.
- **UEM-E10-FX-010** — CRII-009: result population differs from the manifest population or duplicates an ID.
- **UEM-E10-FX-011** — CRII-011: result rows are not sorted lexically by candidate_id.
- **UEM-E10-FX-012** — CRII-008: results envelope does not bind the exact manifest SHA-256.
- **UEM-E10-FX-013** — CRII-010: a result record violates the supplied result-record field/schema constraints.
- **UEM-E10-FX-014** — CRII-007: results envelope does not have the exact permitted top-level shape; CRII-013: an explicit prohibited identity mapping/adapter construct is present.
- **UEM-E10-FX-015** — CRII-012: manifest/results bytes are not in the required canonical JSON byte form.
- **UEM-E10-FX-016** — CRII-004: source bytes do not match the manifest SHA-256.

### Rule-attribution notes

- Array ordering is attributed to the dedicated ordering rules (`CRII-002` for manifests and `CRII-011` for results); `CRII-012` is used for byte-level canonical JSON encoding/key-order/separator/BOM/newline failures.
- `UEM-E10-FX-007` also violates `CRII-010` because `X1` fails the candidate-ID pattern in the supplied `RESULTS_ENVELOPE_SCHEMA.json`, in addition to violating exact population identity (`CRII-009`).
- `UEM-E10-FX-014` violates both exact envelope shape (`CRII-007`) and the explicit no-mapping rule (`CRII-013`) because it contains a top-level `mapping` object.
