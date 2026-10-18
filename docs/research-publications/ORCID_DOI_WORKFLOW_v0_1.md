# DOI and ORCID registration workflow v0.1

**Status:** candidate operational publication procedure. **No deposit, DOI registration, ORCID modification, peer review, endorsement or standing promotion is performed by this document.**

## Distinct functions

- **ORCID** is the persistent person identifier and research-output list for Ryan Feller: https://orcid.org/0009-0000-7863-5792. A public ORCID Works entry associates a researcher with a work; it is neither a DOI issuer nor a scientific validation.
- **Fork GitHub** provides inspectable source and reviewer navigation, not by itself a scholarly archival guarantee.
- **Zenodo** can publish datasets, reports and software, register a DOI at publication, and archive GitHub releases when GitHub integration is enabled. Avoid duplicate deposits of the same object where a DOI already exists.
- A **version DOI** refers to a specific archival version; version relationships must not rewrite frozen predecessors.

Official help: https://help.zenodo.org/docs/get-started/quickstart/ ; https://help.zenodo.org/docs/github/enable-repository/ ; https://help.zenodo.org/docs/github/archive-software/github-upload/ ; https://help.zenodo.org/docs/deposit/manage-versions/ ; https://info.orcid.org/new-features-alert-improvements-to-adding-and-grouping-works/

## Per-output metadata packet (required before deposit)

```text
object_id / exact version:
title / abstract (bounded):
output_type (report | dataset | software | preprint | other):
original date / exact version release date:
creators (actual contributors, roles and authenticated ORCID if available):
rights, sensitive material and permissions:
immutable bytes and SHA-256 manifest:
run environment and reproduction commands:
control and negative-case receipts:
evaluation outcome / verification independence class:
limitations, failed predecessors and withholding decisions:
repository source commit / release tag:
related-object IDs and typed relations:
DOI (none until issued):
ORCID work status (not checked until verified):
```

## Registration sequence

1. Search existing GitHub releases, Zenodo records and the researcher's ORCID Works for duplicates and predecessor identifiers.
2. Examine and validate the exact files and metadata locally. Keep historical packages unchanged. Publish a derivative public redaction only as a separately identified object.
3. For software, reconcile repository `CITATION.cff` and any `.zenodo.json` *before* connecting a release. At the base commit inspected here, `CITATION.cff` identifies the article **Reconstructive Fidelity in the Age of AI**, `type: article`, `version: 1.0`; it is not appropriate to silently reuse as metadata for every experimental software artifact. Zenodo gives precedence to `.zenodo.json` if both are present.
4. For a discrete research report or dataset, create a separately typed Zenodo upload and verify actual creator/ORCID information, version, related identifiers and publication rights. For a software release, use the explicit GitHub-to-Zenodo integration after checking how release metadata applies.
5. Publish only the selected and checked material. Obtain the actual DOI from Zenodo's resulting record (or use the existing DOI where appropriate); never invent or predict a DOI. Verify record landing page and manifest hashes after publication. Zenodo published files cannot normally be replaced in-place; use versioning for substantive changes.
6. In the authenticated ORCID record, use Works > Add > Add DOI where supported, import via an authorized service, or add a work manually with its exact URL and metadata; confirm the actual Work entry and visibility.
7. Update the public Fork index with `DOI_REGISTERED` / `ORCID_LISTED` **only after direct confirmation**. Record DOI URL, citation date, version, deposited SHA-256, ORCID Work identity or publicly retrievable result, and checking actor/time.
8. Later outcomes and repairs become named successors or revisions with explicit typed relations, not amendments to previous experimental facts.

## Release gate

No publication without recorded results of (a) byte/hash verification, (b) work/claim separation, (c) attribution/permissions and open-source compatibility, (d) private or sensitive content review, and (e) DOI deduplication. Publish bounded failures with their real classification when legally/disclosurally eligible. Do not remove failed predecessors. An independent review must identify its actual independence class.

## Citation correction task

Before any Zenodo GitHub integration is enabled for an additional release, make an object-specific citation decision. Consider a distinct research repository software citation and preserved article-specific preferred citation, or separately deposited research objects. Do not silently replace the 2026 article's existing `CITATION.cff` historical attribution, and do not release a mismatched new package.
