# QSA-001 v0.1.1 Successor Regression Return 001

Target successor implementation: `143fd4fc6fad105e808fae169b4454a89eb3c789`

Predecessor reference remains: `d18119105481d194298148a31715303c77a244bc`

The successor baseline passed locally. A1-A12 and focused probes A4-R, A5-R, A6-R1, A6-R2, A6-R3, and A7-R were executed against the exact bytes later preserved in the successor implementation commit; every declared expectation matched.

Focused repair observations:

- `A4-R` rejected a validly signed state-parent inconsistency at the canonical-chain relation.
- `A5-R` rejected a validly signed successor/build-mark relation inconsistency.
- `A6-R1`, `A6-R2`, and `A6-R3` independently rejected qualification intervals invalid at submission, inspection, and adoption respectively.
- `A7-R` rejected a validly signed stale-parent transition.

Standing is local successor-regression evidence only. Exterior recomputation is unopened. Bootstrap remains withheld. Production readiness and formal security are not established.
