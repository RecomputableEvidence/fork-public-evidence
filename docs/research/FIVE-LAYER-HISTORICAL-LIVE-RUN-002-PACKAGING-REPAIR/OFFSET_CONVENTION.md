# Stage 1A Offset Convention v0.1

This successor packaging rule makes explicit a convention that was under-specified in Run 001.

For each Stage 1A block:

- `char_start` and `byte_start` are inclusive.
- `char_end` and `byte_end` are exclusive.
- The `[start,end)` source slice **includes the block's terminating line-feed delimiter when one is present in the source**.
- `verbatim_text` preserves the block content **without that terminal line-feed delimiter**.
- Therefore `[byte_start, byte_end)` is not required to be byte-identical to `verbatim_text.encode("utf-8")`; when a terminal LF exists, the source slice is exactly `verbatim_text.encode("utf-8") + b"\n"`.
- No other whitespace normalization is permitted.

This convention describes successor packaging behavior only. It does not rewrite Run 001 offsets or text.
