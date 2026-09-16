# FORK-VOS-001 E002 Confirmatory Closeout 001

**Target:** `E002_STIMULUS_02_SPATIAL_IDENTITY_MISSINGNESS.png`  
**Frozen target SHA-256:** `7b39c369875bf1fa23edac6a5919847410a06e60e78cb3d6e99cb07e8d7c1718`  
**Execution:** `CONFIRMATORY_EXECUTION_COMPLETE`  
**Disposition:** `CLOSED_WITH_BOUNDED_STANDING_VECTOR`

## Pair discipline

The confirmatory scorer uses exactly:

- **Oblique:** `attachments (24).zip` — first valid STIM02 oblique burst.
- **Centered:** `attachments (28).zip` — first valid STIM02 centered burst.

`attachments (27).zip` is a later valid oblique burst and is preserved but excluded from confirmatory scoring to avoid post-outcome selection.

The earlier `attachments (25).zip` intake does not satisfy the centered condition because its photo-byte population belongs to the prior STIM01 centered acquisition.

## Frozen vector result

| Dimension | Standing |
|---|---|
| Geometry | `ESTABLISHED_FOR_DECLARED_PAIR` |
| Luminance | `CONDITION_DEPENDENT_PARTIAL` |
| Reflection | `SPATIALLY_NONUNIFORM_AND_VANTAGE_DEPENDENT` |
| Spatial frequency | `FREQUENCY_DEPENDENT_NOT_EQUIVALENT_TO_COARSE_FIDELITY` |
| Missingness | `NO_TILE_LOSS_OBSERVED_BUT_ABSENCE_SEPARATION_NOT_FULLY_CHALLENGED` |
| Independence | `NOT_ESTABLISHED` |

## Confirmatory observations

### Geometry

The declared centered and oblique capture conditions remained materially different in the confirmatory pair:

- centered perspective index: **0.122**
- oblique perspective index: **0.587**

This establishes the manipulation for this pair; it does not establish a universal geometry threshold.

### Tile population and identity

The source contains **9** distinct coded tiles.

- Centered capture: **9/9** tile regions visibly present.
- Oblique capture: **9/9** tile regions visibly present.
- Registered analyzer identity ranking: **9/9 correct identities ranked first centered; 9/9 oblique**.

No source tile is absent in STIM02, so this round does **not** convert the missingness dimension into a general source-absence test.

### Near-black / near-white

Near-black ordering is strong:

- centered: median Spearman **1.0**, minimum **1.0**, 9/9 perfect-rank tiles.
- oblique: median Spearman **1.0**, minimum **0.548**, 6/9 perfect-rank tiles.

Near-white behavior diverges sharply by condition:

- centered median ladder dynamic range: **1.65** digital units — substantial highlight compression/clipping.
- oblique median ladder dynamic range: **28.49** digital units, median rank Spearman **1.0**.

This confirms that preservation of one luminance regime does not imply preservation of another.

### Spatial frequency

Median modulation `(P95-P5)/(P95+P5)`:

| Source stripe width | Centered | Oblique |
|---:|---:|---:|
| 1 px | 0.025 | 0.082 |
| 2 px | 0.023 | 0.086 |
| 4 px | 0.218 | 0.310 |
| 8 px | 0.341 | 0.469 |

The supported conclusion is **frequency dependence**. Because projected scale and aliasing can themselves generate modulation, the larger oblique values are **not** interpreted as greater fidelity.

### Reflection field

Across source-black pixels, the span of the nine tile-median captured luminances was:

- centered: **5.50**
- oblique: **33.87**

The physical capture environment is therefore demonstrably spatially nonuniform and vantage dependent in this execution.

## Closeout

E002 can close now. No additional photographs are required for this epoch.

What E002 supports is bounded:

> A physical display → environment/reflection → camera chain can preserve some declared visual distinctions while preserving others only conditionally, attenuating high-frequency structure, compressing luminance regimes, and introducing position/vantage dependence that must remain explicit in later reconstruction.

What E002 does **not** establish includes general camera reliability, source completeness, semantic correctness, legal/evidentiary sufficiency, independent replication, or temporal/contextual continuity.

Any successor such as VOS-TC receives only explicitly declared constraints or inputs. It does not inherit stronger standing from E002 closure.
