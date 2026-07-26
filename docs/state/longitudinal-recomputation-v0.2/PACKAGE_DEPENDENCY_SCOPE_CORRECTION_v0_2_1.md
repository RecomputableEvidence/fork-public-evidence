# Longitudinal replay package dependency scope correction v0.2.1

## Preserved negative evidence

`PACKAGE_MANIFEST_v0_2.json` included two repository-wide moving surfaces:

- `receipts/claim-admission/FORK_CLAIM_ADMISSION_HARDENING_SELF_CHECK_RECEIPT_v0_1.json`;
- `docs/state/README.md`.

The first changes whenever the tracked-tree inventory changes. The second
accumulates routing for successor state candidates. Treating either file as an
immutable member of the v0.2 package makes an honest successor appear to
corrupt its predecessor.

The original v0.2 manifest remains unchanged at its PR #91 source coordinate.
The v0.2.1 manifest narrows package membership to versioned v0.2 artifacts and
records both shared files as external moving dependencies. Their owning
checkers still validate them; they are no longer misrepresented as frozen
v0.2 package bytes.

## Standing

This is a package-scope correction, not a correction to the replayed state,
event classification, Git interval, review standing, or non-effects.

It does not confer admission, publication, merge authority, provider
authority, retry authority, readiness, execution permission, or truth.
