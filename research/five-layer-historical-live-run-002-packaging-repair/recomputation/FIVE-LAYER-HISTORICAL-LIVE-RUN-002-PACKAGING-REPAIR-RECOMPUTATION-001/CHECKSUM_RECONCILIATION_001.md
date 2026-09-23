# CHECKSUM-RECONCILIATION-001

**Object:** `FIVE-LAYER-HISTORICAL-LIVE-RUN-002-PACKAGING-REPAIR-RECOMPUTATION-001`

During repository-side freeze construction, `RECOMPUTATION_RECEIPT.json` was serialized with compact inline arrays for two fields rather than the indentation layout used by the local draft from which the initial `SHA256SUMS.txt` entry had been calculated.

The semantic and field content of the receipt was not changed by that repository serialization, but the exact repository bytes differ from the local draft bytes. The repository-resident receipt is therefore authoritative for the freeze coordinate.

Observed repository receipt identity:

- bytes: `5598`
- Git blob: `e7db0e953c3c4d8b03116e89db8c4c3e9265a841`
- SHA-256: `9e76b19f85cf307b3a1d172c46bbbcd74528d404c137afd5fe8cf8890b8bef48`

The initial checksum entry `a202856f...` belonged to the 5,830-byte local draft and is not valid for the repository-resident receipt.

Treatment:

- preserve the initial freeze commit in Git ancestry;
- change no recomputation finding, subject binding, disposition, or semantic standing;
- add this reconciliation record;
- replace `SHA256SUMS.txt` with hashes of the final repository-resident freeze files.

**Semantic-rerun effect:** `NONE`  
**Subject-artifact effect:** `NONE`  
**Freeze disposition effect:** `NONE`
