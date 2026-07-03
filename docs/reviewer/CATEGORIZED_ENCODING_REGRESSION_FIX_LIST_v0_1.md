# Categorized Encoding Regression Fix List v0.1

## Purpose

This document records the encoding cleanup categories for the public surface cleanup branch.

It avoids embedding literal corrupted glyphs. Example mappings are represented as Unicode codepoint sequences so the repository-wide mojibake detector can remain strict.

## 1. Bulk-fix confirmed mojibake

Representative mappings:

```text
U+00E2 U+20AC U+0153 -> U+201C  LEFT DOUBLE QUOTATION MARK
U+00E2 U+20AC U+009D -> U+201D  RIGHT DOUBLE QUOTATION MARK
U+00E2 U+20AC U+2122 -> U+2019  RIGHT SINGLE QUOTATION MARK
U+00E2 U+20AC U+201C -> U+2013  EN DASH
U+00E2 U+20AC U+201D -> U+2014  EM DASH
U+00C3 U+00A9        -> U+00E9  LATIN SMALL LETTER E WITH ACUTE
U+00C3 U+00A1        -> U+00E1  LATIN SMALL LETTER A WITH ACUTE
U+00C3 U+00B3        -> U+00F3  LATIN SMALL LETTER O WITH ACUTE
U+00C3 U+00B1        -> U+00F1  LATIN SMALL LETTER N WITH TILDE
U+00C3 U+00BC        -> U+00FC  LATIN SMALL LETTER U WITH DIAERESIS
```

## 2. Strip BOMs where safe

Remove leading UTF-8 byte-order marks only from allowlisted files.

## 3. Hard-exclude HTML-escaping false positives

Files named `app.js` are hard-excluded.

Reason: `app.js` can contain intentional HTML escaping strings and unicode escape sequences. These are not mojibake and should not be rewritten by an encoding cleanup script.

## 4. Manual review queue

Files are logged to `encoding_manual_review.log` and not modified if they contain:

- non-UTF-8 bytes;
- unprintable control characters;
- suspicious cases that cannot be safely reduced by deterministic replacement;
- path escape or control-byte corruption.

## 5. Documentation examples

Do not mutate files merely because they display example corruption patterns.

However, do not blanket-exclude the entire `docs/` or `examples/` directories. Several real public-surface defects live there.

This cleanup uses an explicit allowlist, not broad path-based mutation.

## Non-claims

This cleanup does not establish correctness of the underlying prose.

This cleanup does not establish compliance, legal sufficiency, admissibility, production readiness, execution eligibility, fault, negligence, or excuse.

This cleanup only addresses encoding integrity in the public surface.
