# Reviewer disclosure mutability contract

The immutable envelope contains only `DISCLOSURE/REVIEWER-DISCLOSURE-TEMPLATE.json`.

Before target examination, the reviewer copies and completes that template at:

`MUTABLE/REVIEWER-DISCLOSURE.completed.json`

`MUTABLE/` is a declared runtime-generated path and is not part of the immutable envelope content manifest. Each attempt copies the completed disclosure into its own attempt directory and binds its SHA-256 in that attempt receipt. No manifest-listed file must be edited.
