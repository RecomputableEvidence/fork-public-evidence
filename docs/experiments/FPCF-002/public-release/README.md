# FPCF-002 — Public prospective forecast evidence archive (candidate)

Published as an **additive public preservation branch**. This record does not amend or admit historical forecast selections. The original 25-forecast FPCF-001 catalogue, prior MKT-01 prospective candidate (#199), FPCF-002 participant A/B/C original return records, their reasoning and sources, negative and verification receipts, and the temporal discrepancy/correction are preserved in a byte-bound archive.

## Standing and limits

- **FPCF-001:** original 25 candidate forecasts, no wholesale admission. MKT-01 original anchor lives in [PR #199](https://github.com/RecomputableEvidence/fork-public-evidence/pull/199), with its distinct server-time witness.
- **FPCF-002:** A (neutral), B (method-equipped), C (method-equipped previously exposed); 6 forecasts each; **not admitted** to forecasting-skill or causal-method-efficacy conclusions.
- Local predecision→final checks do not prove independently witnessed temporal ordering. Submission times, local clocks, GitHub publication time, and event outcomes must not be conflated.
- The temporal discrepancy assertion in 001 was superseded by an **additive correction 002** identifying ChatGPT app timestamps as completion times, not assignment times. Both remain preserved.
- This branch's GitHub publication timestamp establishes a public availability upper bound for its archived bytes; it does not retroactively timestamp the internal candidate-selection stages.
- Independent source verification and adjudication must operate on the original frozen forecasts; resolution documents must be separate successor artifacts and may report YES / NO / UNRESOLVED / INVALID according to the individual contract.

## Complete source archive

To avoid GitHub connector binary-upload limitations, this release stores the exact archive as **10 ordered base64 text parts** in `parts/archive.b64.part01.txt` through `part10.txt`. Concatenate their base64 contents in numerical order, strip whitespace, decode to a ZIP, and verify:

- SHA-256 **`b4956497d4c146c2825b593064a64d2c3a362e51ba5048617f4d8f1d8e09a486`**
- Bytes: **578,960**
- Includes **14 untouched predecessor/return/verification artifacts** plus the enclosing disclosure and `OBJECT_MANIFEST.json` of each original SHA-256 and byte length.

Example offline reconstruction (Python 3):

```python
from pathlib import Path
import base64, hashlib
parts = sorted(Path('parts').glob('archive.b64.part*.txt'))
assert len(parts) == 10
encoded = ''.join(''.join(p.read_text().split()) for p in parts)
raw = base64.b64decode(encoded, validate=True)
assert hashlib.sha256(raw).hexdigest() == 'b4956497d4c146c2825b593064a64d2c3a362e51ba5048617f4d8f1d8e09a486'
Path('FPCF_002_COMPLETE_PRESERVATION_SOURCE.zip').write_bytes(raw)
```

## Policy for future reveals

Never silently edit a prediction's original bytes. Publish later observations as separately timestamped, additive result packets linked by subject SHA-256 and commit. Preserve incomplete/out-of-scope result and unfavorable findings. Recompute forecasts and evidence properties separately; a correct event prediction is not evidence of a correct reasoning history or method effect.
