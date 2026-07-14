# Fork Meta-Evidence Corpus 001 Admission Protocol v0.1

**Package:** `FORK-META-EVIDENCE-CORPUS-001-ADMISSION-INFRASTRUCTURE-v0.1`<br>
**Lifecycle state:** `DRAFT_SELECTION`<br>
**Canonical ledger:** JSON validated by schema and canonicalized under JCS RFC 8785<br>
**Ledger digest:** detached SHA-256 over canonical JCS bytes<br>
**Source admission authority:** none conferred by this installer<br>
**Commit, publication, release, DOI, and push authority:** none

## Purpose

This package initializes the controlled source-admission infrastructure for the
first real Fork Meta-Evidence corpus. It does not admit evidence and does not
execute the final Corpus 001 experiment.

Corpus 001 asks whether Fork can preserve real favorable, unfavorable, mixed,
null, ambiguous, and corrected observations without promoting, demoting,
overwriting, or resolving their evidentiary standing based on desirability.

## Canonical and derived domains

The readable JSON ledger is authoritative as structured data. Its integrity
digest is computed over deterministic JCS canonical bytes and stored in a
detached digest file. The ledger does not contain its own digest.

Original source files are hashed over exact source bytes. No normalization,
transcription, redaction, line-ending conversion, or metadata projection is part
of the source-artifact digest domain.

Markdown output produced by the renderer is a non-canonical projection. It is
not evidence, does not alter the ledger, and does not expose private locators.

## Initial observations

- `OBS-001`: `FAVORABLE`, `CANDIDATE`
- `OBS-002`: `UNFAVORABLE`, `CANDIDATE`
- `OBS-003`: `MIXED`, `CANDIDATE`
- `OBS-004`: `NULL`, `OPEN_SLOT`
- `OBS-005`: `AMBIGUOUS`, `CANDIDATE`
- `OBS-006`: `CORRECTED`, `CANDIDATE`

All observations begin with `admitted: false`. The null slot remains open until
a genuine bounded null observation is located. Weak, declined, unfavorable, or
ambiguous evidence may not be relabeled as null merely to complete the cohort.

## Private workspace

The installer creates empty `incoming` and `canonical` directories for all six
observations, plus `derived`, `manifests`, and `packet` directories under the
operator-supplied private workspace root.

The private workspace is outside the public repository. The installer never
writes a source file there. Existing private files must remain byte-identical
before and after execution.

A public ledger may contain only an opaque relative private locator in the form:

`PRIVATE_CORPUS_001/OBS-000/example.ext`

It may not contain a drive letter, UNC path, home-directory path, file URI, or
other absolute local path.

## Admission gates

An observation may not become `ADMITTED` unless it has:

1. an immutable source-artifact identifier;
2. an opaque private locator;
3. media type and exact byte length;
4. SHA-256 over exact source bytes;
5. acquisition timestamp and acquisition actor;
6. temporal status;
7. confirmed eligibility;
8. admission-decision actor and timestamp;
9. a non-pending disclosure treatment;
10. attribution authorization records for any affirmative authorization flag.

The corpus may not enter `ADMISSION_FROZEN` or any later lifecycle state while
an open slot remains or while any required stratum lacks an admitted source.

## Authority boundary

Candidate selection does not establish truth, validation, endorsement,
partnership, adoption, publication permission, legal sufficiency, compliance,
risk classification, or institutional authority.

The installer does not copy evidence, infer authorization, manufacture a null
case, admit a source, advance the lifecycle, stage files, commit, tag, release,
create a DOI, publish, or push.
