# Placement Profile Normalized Output Comparison Guide v0.1.1

Status: comparison guidance  
Scope: normalized checker outputs for AI Governance System Placement Profile checker v0.1.1

---

## Purpose

Normalized outputs support recomputable comparison across local environments. They preserve checker substance while excluding environment-specific metadata.

---

## Semantic fields retained

The normalized output retains:

- `checker_id`;
- `checker_version`;
- `record_id`;
- `system_id`;
- `overall_status`;
- `claim_boundary`;
- `non_claims`;
- sorted `checks` with `check_id`, `status`, `error_code`, `message`, and `details` where present.

These fields should match for substantive equivalence.

---

## Environment-specific fields excluded

The normalized output excludes:

- `checked_at_utc`;
- `environment`;
- `record_path`;
- `schema_path`.

These fields may differ between machines and should not be used to determine substantive checker equivalence.

---

## Comparison procedure

To compare two checker runs:

1. Generate `--normalized-output` for both runs.
2. Compare the normalized JSON files byte-for-byte.
3. Treat a mismatch as a substantive checker-output difference unless explained by an intentional version change.

The normalized result does not prove the underlying placement claim is true. It only supports deterministic comparison of the checker result.