# Parent reconstruction procedure

1. Concatenate `parent.gzip.base64.parts/part-001.b64` through `part-009.b64` in ascending filename order with no inserted separators or line terminators.
2. Base64-decode the concatenated ASCII bytes using the RFC 4648 standard alphabet.
3. Gzip-decompress the decoded bytes.
4. Verify the resulting byte stream is exactly 334,735 bytes and SHA-256 `c9ba196efa8709279d8967716ec690bbc5f3112ab5d38e67683768ebe1f62bbf`.
5. Interpret the reconstructed parent as UTF-8 only after the byte identity check.
6. Run 001's historical target is parent lines 1–4026 inclusive with original line endings; it must hash to `a35124bb73fb3ac81bc01e66c60a68fe875f912f377f9aa02ef617d066f33583` and contain 262,318 bytes.
7. Verify the Source 10 marker begins at parent line 4028.

No normalization, newline conversion, inserted separator, reserialization, or content repair is permitted during reconstruction.
