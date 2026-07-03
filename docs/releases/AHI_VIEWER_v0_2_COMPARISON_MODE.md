# AHI Viewer v0.2 — Comparison Mode

## Summary

AHI Viewer v0.2 adds comparison mode for the Fork AHI proof surface.

It lets reviewers compare scenario pairs across:

- boundary movement;
- attempted inference;
- required revalidation;
- Fork-supported inspection;
- Fork non-claims;
- artifact and checker coverage.

## Canonical comparison pairs

| Pair | Purpose |
|---|---|
| Scenario 01 → Scenario 02 | Baseline unbounded handoff versus Fork-preserved handoff |
| Scenario 03 → Scenario 04 | Scope expansion versus authority leakage |
| Scenario 05 → Scenario 06 | Policy-reference laundering versus distributed handoff |
| Scenario 06 → Scenario 07 | Internal distributed authority boundary versus external authority bridge |

## Added files

- `docs/viewer/ahi-viewer-v0_2/README.md`
- `docs/viewer/ahi-viewer-v0_2/index.html`
- `docs/viewer/ahi-viewer-v0_2/app.js`
- `docs/viewer/ahi-viewer-v0_2/styles.css`
- `docs/viewer/ahi-viewer-v0_2/data/comparison_pairs.json`
- `docs/viewer/ahi-viewer-v0_2/schema/comparison_pairs.schema.json`
- `scripts/build_ahi_viewer_comparison_data_v0_2.ps1`
- `scripts/build_ahi_viewer_comparison_data_v0_2.py`
- `scripts/check_ahi_viewer_v0_2.ps1`

## Verification

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_ahi_viewer_comparison_data_v0_2.ps1 -ForceOverwrite

powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1
```

After commit:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1 -CheckDeterminism
```

## Non-authority posture

Viewer v0.2 is static, repo-local, and read-only.

It does not approve, certify, score, authorize, determine compliance, determine admissibility, establish legal sufficiency, decide acceptance, or judge correctness.

## Suggested tag

```powershell
git tag -a ahi-viewer-v0.2 -m "AHI viewer v0.2 comparison mode"

git push origin ahi-viewer-v0.2
```
