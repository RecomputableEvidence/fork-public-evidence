# Fork Line Ending Canonicalization v0.1

Status: INTERNAL_PRESERVATION_HARDENING

## 1. Purpose

This hardening layer locks evidence-relevant text artifacts to LF line endings.

Fork relies on recomputation, manifests, hashes, verification receipts, and deterministic artifact handling. Line-ending drift between Windows and Unix-like environments can change file bytes and therefore change hashes, even when the visible text appears unchanged.

This branch makes line endings explicit.

## 2. Rule

Evidence-relevant text artifacts must use LF line endings.

CRLF and bare CR line endings are defects for governed text artifacts.

## 3. Scope

The canonicalization policy applies to common Fork text artifacts, including:

- Markdown documentation
- JSON and JSONL artifacts
- Schemas
- Python tools and tests
- PowerShell and shell scripts
- YAML/TOML metadata
- CSV/TSV fixtures
- CFF citation metadata
- Root metadata files such as LICENSE, COPYRIGHT, and SHA256SUMS

Binary artifacts are explicitly marked binary in `.gitattributes`.

## 4. Enforcement

The enforcement tool is:

    python tools/check_line_endings.py

It scans repository text candidates and fails if CRLF or bare CR line endings are present.

The normalization tool is:

    python tools/normalize_line_endings.py

It converts governed text candidates to LF.

## 5. Preservation Boundary

This branch does not change prior tags or historical release commits.

If line-ending normalization changes bytes in any artifact that is itself covered by a manifest or hash receipt, the relevant receipt must be regenerated or the artifact must remain excluded from normalization until a bounded migration is performed.

## 6. Invariant

Fork text artifacts that participate in recomputation, schema validation, release metadata, receipts, or reviewer-facing evidence must not depend on platform-specific line endings.