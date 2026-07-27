# Architecture v0.1.1 corrected normative excerpts

These excerpts are the five bounded changes represented by `ARCHITECTURE-v0_1_1-CHANGESET.json`. The complete successor Markdown is bound by `ARCHITECTURE-PUBLIC-BINDING.json` and is not silently reconstructed from these excerpts.

## §28 — Required envelope field

| Group | Field | Description |
|---|---|---|
| Status | `evidence_processing_status` | One top-level §32 evidence-processing status |
| Scope | `completeness_basis` | Basis for any completeness statement |

## §29 — Illustrative envelope corrections

```json
{
  "record_type": "OBSERVATION",
  "evidence_processing_status": "CAPTURED",
  "scope": {
    "capture_scope": ["declared audit event categories"],
    "known_exclusions": ["human intent not directly observed"],
    "completeness_basis": "SOURCE_STREAM_CONFIGURATION_AND_OBSERVED_CURSOR_ONLY"
  },
  "verification_status": "NOT_RECOMPUTED"
}
```

## §33 — Failure-state baseline

| Code | Name | Required interpretation |
|---|---|---|
| `FS-000` | `NONE` | No known failure within the declared processing attempt |

## §49 — DHM-004 acceptance control

| ID | Acceptance check | Method | Required result |
|---|---|---|---|
| `EA-DAT-011` | DHM-004 exception record binds explicit authorization, named purpose, approved source/field scope and destination, legal/privacy review where required, retention schedule, and deletion procedure | Exception-record and control-receipt inspection | `PASS` or `NOT_APPLICABLE` when DHM-004 is not selected |

## Non-claim

These excerpts do not replace the full architecture artifact and do not constitute admission, schema implementation, production authorization, or compliance determination.
