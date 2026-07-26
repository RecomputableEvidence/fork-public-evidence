# Fork longitudinal causal reconciliation v0.3

v0.2 could detect an unreconciled concurrent successor, but its reducer
remained ordinal and single-headed. v0.3 makes the partial order executable.

The endogenous case is the convergence of Fork's Sequence Surface and root
checksum integrity lineages:

- frontier anchor A: `5fbabbd486d4e863d23e0096600185ada92539a6`;
- frontier anchor B: `c6bb2df424193e7ef043ee3c0436bf97ba10fc6e`;
- Sequence Surface branch event: `c879242...`;
- root checksum branch event: `5150ece...`;
- PR #81 causal join: `97abe21...`;
- PR #82 closure join: `0bac4f6...`.

The inventory is the exact set reachable from the closure and not reachable
from either frontier anchor. Merge changes are bound separately against each
parent, avoiding the empty combined `diff-tree` view of a merge commit.

## Recompute

```bash
python tools/check_longitudinal_causal_reconciliation_v0_3.py
```

Inspect one coordinate:

```bash
python tools/check_longitudinal_causal_reconciliation_v0_3.py \
  --coordinate 5150ece4c29cea38cfe5e25daeb781423c680834
```

Compare concurrent branch states:

```bash
python tools/check_longitudinal_causal_reconciliation_v0_3.py \
  --compare-left c879242c4dafad68bdd8e7bcf2466e4169351969 \
  --compare-right 5150ece4c29cea38cfe5e25daeb781423c680834
```

`--write-derived` mechanically regenerates the projection, frontier coverage
receipt, reconciliation receipt, and versioned package manifest.

## Boundary

The causal join records what the declared state vector becomes. It does not
make the merge an admission event and does not inherit the later PR #83
admission anchor backward. No provider call, Pair-001 repetition, readiness
decision, retry authorization, or execution request occurs.
