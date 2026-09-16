# Recompute / Review Notes

Raw confirmatory ZIPs are not duplicated inside this package. Their exact archive and member hashes are bound in `FORK-VOS-001-E002-STIM02-CONFIRMATORY-PAIR-001.json`.

Confirmatory pair selection is fixed:
- first valid STIM02 oblique burst = `attachments (24).zip`
- first valid STIM02 centered burst = `attachments (28).zip`

Do not substitute the later supplemental oblique burst into the scorer.

The scoring vector is inherited only from the frozen pre-capture test register:
SOURCE_TILE_POPULATION / CAPTURE_TILE_OBSERVATION_STATE / ANALYZER_TILE_DETECTION_STATE / NEAR_BLACK_RANK / NEAR_WHITE_RANK / SPATIAL_FREQUENCY_MODULATION_1_2_4_8PX / CENTERED_VS_OBLIQUE_DELTA / LOCAL_REFLECTION_FIELD.

The supplied homographies are analysis receipts. Independent reviewers may recompute registration, but alternate registration does not silently replace this execution record.

No GPS/location coordinates are included in derived records.
