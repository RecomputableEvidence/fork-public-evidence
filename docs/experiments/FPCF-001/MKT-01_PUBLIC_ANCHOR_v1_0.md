# FPCF-001 / MKT-01 — Public commitment anchor v1.0

**Status:** Public prospective candidate; independent GitHub server-time test required.
**Prediction (exact original text):** The FOMC increases both bounds of its target federal funds range by at least 25 bps at the Oct 28, 2026 decision
**Original probability:** P(YES)=0.50; P(NO)=0.50.
**Baseline:** 2026-09-16 FOMC target range 3.75%-4.00%.
**Decision source:** Official Federal Reserve October 28, 2026 FOMC statement; scheduled announcement October 28 at 14:00 Eastern (18:00Z).
**YES:** October 28 official statement raises both September 16 baseline rate-range bounds by >=0.25 percentage points. **NO:** Official October 28 decision does not satisfy YES. **UNRESOLVED:** No official scheduled decision/ambiguous supersession.
**Scientific standing:** This does not prove Fed direction prediction skill, Lens method advantage, or production capabilities. The original catalog had this exact statement and probability before this anchor, but the catalog's own claimed date is not an independent timestamp.

## Externally pinned SHA-256 digests (full bytes distributed in FPCF-001 MKT-01 packet)

- `MKT-01_FORECAST_COMMITMENT.json`: `ad959d88d1deccaea10dbf65a5ea7de56315771e922ff387681d3716d62681b8`
- `MKT-01_ORIGINAL_CANDIDATE.json`: `bab376cc66b280a2e2c78ee64df26798b7e50498bda0e0513f85aa6ad681f03f`
- `MKT-01_SOURCE_BASELINE.json`: `2a04ec89c68af5f7b30c259b82133949eb60f58306d7756e9c2e802eaea7521c`
- `MKT-01_SOURCE_LINEAGE.json`: `e6e5d306d22f3e64d0a5edde235bf28239122ac09979b7227c4890157e6b2e66`
- `MKT-01_MANIFEST.json`: `151978ac26737798f4645ba151f3d39f64a969bbb31fab2dbd8b006cbe3d70bd`

## Source references and limitations

- September statement: https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm
- 2026 decision dates: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
- Release calendar: https://www.federalreserve.gov/newsevents/2026-october.htm
- Curated source excerpts and provenance are included in locally preserved `MKT-01_SOURCE_BASELINE.json`; **the original HTML response bytes were not captured**.
- Local check: 9/9 fixture assertions matched expectation, including the negative demonstrating that a coordinated re-seal passes an internal checker but fails when compared against this independently fixed manifest digest. The local test is not an external validation.
- A GitHub server `created_at` on a pull request naming a fixed commit, together with this file's pinned SHA-256 content, is a **public third-party time witness**, not an RFC3161 qualified timestamp token or an infallible archive. Commit author/committer dates are NOT accepted as trusted timestamps. Future edits/branch movement cannot revise the originally pinned commit without detection, but deletion, suppression and GitHub trust remain limitations.
- Do not modify this original forecast when publishing future outcomes; publish an additive resolution document, showing both event and source publication times.