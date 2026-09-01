# Fork Public Technical Disclosure — Version Routing

## Current repository successor candidate

Use:

`v0.1.2/README_VERIFY_PUBLIC_DISCLOSURE_v0_1_2.md`

v0.1.2 preserves the exact v0.1.1 verification payload as its inherited layer and adds a versioned repair overlay for the Windows instruction defect that could not be corrected in place without invalidating the v0.1.1 integrity inventory.

The v0.1.2 repository successor is **not yet a detached bundle release**. A detached v0.1.2 ZIP requires its own post-freeze digest and detached receipt.

## Historical predecessor

The root v0.1.1 files remain preserved for historical recomputation:

- `README_VERIFY_PUBLIC_DISCLOSURE_v0_1_1.md`
- `PUBLIC_DISCLOSURE_MANIFEST_v0_1_1.json`
- `SHA256SUMS.txt`
- `verify_public_disclosure.py`

Do not edit the inventoried v0.1.1 README in place. The frozen adoption candidate `a16b1905923354538d6bed1d231fdc810e3d531f` demonstrated why: the legitimate documentation edit caused the predecessor integrity verifier to reject the changed bytes.

## Boundary

Version routing does not create admission, validation, production readiness, legal/compliance sufficiency, pilot authorization, execution authority, or institutional authority.
