# PR #107 provider-result admission candidate

This directory preserves and classifies the single provider-validation call authorized by PR #107.

## Observed result

- governed merge: `5cf581c7b95c5ea4e9b662e089fc89f5b552696f`
- workflow: `CSH Provider Validation v0.1.2`
- run: `30711931234`
- requested model identifier: `deepseek/DeepSeek-V3-0324`
- request SHA-256: `d2c8aabbdda4f17509395aa8a55f607b2b0d52138a251e8da92bb8384a05bcef`
- observed HTTP status: `410`
- sanitized provider error code: `github_models_retirement_brownout`
- receipt status: `FAIL`
- provider-validation calls: `1`
- Pair-001 calls: `0`

The result differs from the precommitted identical-failure condition of HTTP 500 with body digest `aaa6769a31dd521019993212fa93add5efbcdaadc2e777041173091a03fafc23`. It is therefore classified under `FSS-PAIR001-T016` as a different outcome requiring separate classification.

## Standing and effect

The exact receipt is admitted only if this candidate is reviewed, passes exact-head CI, and is merged into `preservation/clean-continuance-v0.1` as an explicit admission act.

Admission preserves the 410 response as bounded negative evidence. It does not establish why the endpoint returned 410, whether the model exists elsewhere, whether another identifier or endpoint would succeed, or whether the provider's sanitized error code is a complete causal explanation.

The one authorized uppercase retry is consumed. No additional uppercase retry, lowercase diagnostic, endpoint migration, identifier substitution, request-byte modification, Pair-001 execution, or readiness promotion follows automatically.

## Verification

Run:

```bash
python tools/check_pr107_provider_result_admission_v0_1.py
python -m pytest tests/test_pr107_provider_result_admission_v0_1.py -q
```

Expected checker result:

`PR107_PROVIDER_RESULT_ADMISSION_CANDIDATE_CONFORMS_NOT_ADMITTED`
