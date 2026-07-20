# CI Failure and Correction Record v0.1

## Scope

This record preserves the first exact-head integration failure observed for draft PR #85 and the bounded correction applied afterward.

## Failed exact head

- head: `09230a11de58c048fbc4099336acf3cf5d80749a`
- workflow: `Fork Proof-Surface Integration`
- run: `29762670955`
- conclusion: `failure`

The following jobs failed at their first proof-surface state step:

- Python proof surface — Ubuntu;
- Python proof surface — Windows;
- PowerShell 5.1 proof-surface entry point.

The CSH execution-instrumentation jobs succeeded. `Fork Evidence CI` run `29762671174` and `Root Checksum Manifest v0.1` run `29762671072` also succeeded at the failed head.

## Cause

The front-door rewrite removed the exact canonical research-hypothesis expression required by `tools/check_fork_proof_surface_state_v0_1.py`:

```text
E[U | H = 1] < E[U | H = 0]
```

The checker requires the root README to remain synchronized with `docs/state/FORK_PROOF_SURFACE_STATE_v0_1.json`. The omission was a coherence regression: the underlying canonical state was unchanged, but the new front door no longer surfaced the expression.

## Correction

Commit `582189d873e16d4a527ffc8fae20dddfa87180b4` restores a compact `Research status` section containing the exact canonical expression and bounded interpretation.

The correction does not change:

- the canonical proof-surface state;
- the hypothesis itself;
- checker or schema semantics;
- evidentiary standing;
- authority boundaries;
- Pair-001 standing or execution controls;
- provider-call authority;
- PR #84.

## Standing

The failed run remains preserved as negative evidence. The correction must be validated at the new exact head; success at a later head does not rewrite the earlier failure into a pass.

This record is not admission, publication, merge authorization, readiness promotion, provider authority, or Pair-001 execution authority.
