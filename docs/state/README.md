# Fork Proof-Surface State Routing

The files in this directory occupy different temporal and governance
coordinates. They must not be read as interchangeable current-state claims.

The machine-readable route is:

- `docs/state/FORK_STATE_ROUTING_v0_2.json`
- `docs/state/FORK_STATE_ROUTING_v0_3.json`

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

## Linear replay predecessor

`longitudinal-recomputation-v0.2/LONGITUDINAL_CURRENT_PROJECTION_v0_2.json`
replays the bounded PR #90 review-preservation transition. It is a research
predecessor candidate, not an admitted projection or authority source.

Run:

```bash
python tools/check_longitudinal_recomputation_v0_2.py --json
```

## Causal reconciliation candidate

`longitudinal-recomputation-v0.3/CAUSAL_CURRENT_PROJECTION_v0_3.json`
replays the endogenous PR #81 and PR #82 branch convergence from two exact
frontier anchors. It derives causal order from Git parents and requires an
explicit decision for every state dimension at each merge. It is a research
candidate, not an admitted projection or authority source.

Run:

```bash
python tools/check_longitudinal_causal_reconciliation_v0_3.py
```

## Exterior recomputation package candidate

`longitudinal-recomputation-v0.3.1/README.md` freezes feature expansion and
provides exact-target envelopes plus machine-checkable receipt templates for
separate exterior recomputation of PR #91 and PR #92. It contains no completed
review receipt and creates no inherited review standing.

Run:

```bash
python tools/check_longitudinal_exterior_recomputation_package_v0_3_1.py
```

A passing result on any of these checkers establishes only its declared
structural and evidentiary scope. It does not establish truth, compliance,
legal sufficiency, safety, authorization, approval, certification,
endorsement, production readiness, or institutional authority.
