# Fork Meta-Evidence CI Hardening v0.1.1

**Package ID:** `FORK-META-EVIDENCE-CI-HARDENING-v0.1.1`<br>
**Change class:** `INSTRUMENTATION_ONLY`<br>
**Base package:** `FORK-META-EVIDENCE-v0.1`<br>
**Historical rewrite authority:** `NONE`<br>
**Commit, tag, release, DOI, and push authority:** `NONE`

## Purpose

This patch adds explicit continuous-integration coverage for the published Fork Meta-Evidence v0.1 package without modifying any v0.1 protocol, schema, registry, fixture, checker, test, receipt, or checksum.

## Improvements

1. A deterministic package-integrity checker validates every entry in the frozen v0.1 SHA-256 manifest.
2. A PowerShell 5.1 entry point runs package integrity, the integrated checker, and the bounded test set.
3. A dedicated GitHub Actions workflow executes the package on Linux and Windows with pinned Python versions.
4. The principal evidence and proof-surface workflows explicitly invoke the meta-evidence checks.
5. Node 24 compatible GitHub Actions majors replace the deprecated Node 20 based action majors in the two amended workflows.
6. A bounded receipt and patch checksum manifest record the local installation result.

## Authority boundary

This patch determines only whether the published package remains mechanically retrievable, checksum-consistent, structurally conforming, and test-green in the tested environments. It does not determine truth, correctness, legality, fairness, safety, compliance, legitimacy, risk classification, impact-assessment sufficiency, institutional authority, production readiness, or evidentiary weight beyond the declared package rules.

## Preservation rule

The v0.1 package is treated as immutable historical material. Any later defect, correction, or interpretation must be represented through a new linked artifact rather than by silently rewriting v0.1.