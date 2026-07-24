# Fork Proof-Surface State Routing

The files in this directory occupy different temporal and governance
coordinates. They must not be read as interchangeable current-state claims.

The machine-readable route is:

- `docs/state/FORK_STATE_ROUTING_v0_2.json`

## Historical projection

`docs/state/FORK_PROOF_SURFACE_STATE_v0_1.json` is the preserved July 11
projection. It is valid at its recorded temporal closure and is not current
reliance standing.

Run its historical checker:

```bash
python tools/check_fork_proof_surface_state_v0_1.py --json --check-summary
```

Its human-readable historical summary is:

- `FORK_PROOF_SURFACE_STATE_SUMMARY_v0_1.md`

## Governed projection

`docs/state/FORK_PROOF_SURFACE_CURRENT_PROJECTION_v0_2.json` is current only
with respect to exact governed preservation coordinate
`1241c0084900f2c60f362205525464582e57b4a7`. It is not a claim that the moving
default branch is the governed current line.

Run:

```bash
python tools/check_temporal_succession_v0_1.py --json
```

## Longitudinal replay candidate

`longitudinal-recomputation-v0.2/LONGITUDINAL_CURRENT_PROJECTION_v0_2.json`
replays the bounded PR #90 review-preservation transition. It is a research
candidate, not an admitted projection or authority source.

Run:

```bash
python tools/check_longitudinal_recomputation_v0_2.py --json
```

A passing result on any of these checkers establishes only its declared
structural and evidentiary scope. It does not establish truth, compliance,
legal sufficiency, safety, authorization, approval, certification,
endorsement, production readiness, or institutional authority.
