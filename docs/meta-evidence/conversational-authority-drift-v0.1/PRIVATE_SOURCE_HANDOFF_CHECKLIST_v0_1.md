# Private Source Handoff Checklist v0.1

Status: `REVIEW_SUPPORT_NOT_PUBLICATION`

Before transmitting the private CAD-004 source package:

- place all 21 exact artifacts in a new folder without renaming or editing them;
- include copies of `SOURCE_MANIFEST_v0_1.json` and `SOURCE_MANIFEST_SUPPLEMENT_001_v0_1.json`;
- create an archive only after the loose-file hashes have been confirmed;
- record the archive filename, byte length, and SHA-256 separately;
- use a channel already agreed with the reviewer;
- do not place credentials, unrelated private conversations, or unregistered files in the archive;
- tell the reviewer that the raw package remains private and is supplied only for bounded review;
- ask the reviewer to recompute the loose-file hashes after extraction;
- require the exact reviewed PR head SHA in the returned verdict;
- preserve the original transmission message and returned review unchanged.

The archive digest identifies the transmitted package. It does not replace the per-file digest comparison and does not establish truth, authorship, or technical validity.
