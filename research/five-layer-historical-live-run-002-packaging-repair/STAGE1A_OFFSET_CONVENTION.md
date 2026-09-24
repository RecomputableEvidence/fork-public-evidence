# Stage 1A Offset Convention v0.1

This successor clarifies the convention used by Run 001 without rewriting Run 001.

For each Stage 1A structural block:

- `char_start` / `char_end` and `byte_start` / `byte_end` define a half-open source interval `[start,end)` over the preserved synthesis bytes/text.
- The source interval **includes the terminal LF delimiter** when the block ended with an LF in the preserved synthesis.
- `verbatim_text` contains the block text with terminal LF characters removed by the Run 001 serializer.
- Therefore `[byte_start, byte_end)` is not asserted to be byte-identical to UTF-8 encoding of `verbatim_text`; reconstruction must use the source interval against the bound synthesis object.

Run 001 is internally reproducible under this convention; this file only makes the previously implicit delimiter rule explicit.
