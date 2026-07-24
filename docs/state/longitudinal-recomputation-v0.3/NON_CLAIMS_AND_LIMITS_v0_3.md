# Causal reconciliation v0.3 — non-claims and limits

This candidate advances Fork from single-headed ordinal replay to
frontier-bounded causal replay. It proves only that, within the declared
frontier:

- Git commits are completely inventoried relative to the exact anchors;
- events bind exact trees, parents, timestamps, subjects, and per-parent path
  deltas;
- event order is derived from parent edges rather than registry order;
- every merge has an explicit decision for every declared state dimension;
- committed projections and receipts reproduce from the declared inputs.

It does not prove:

- semantic event completeness outside the frontier;
- that a declared event classification or reconciliation choice is correct;
- truth, causality beyond Git ancestry, safety, compliance, or legal
  sufficiency;
- review inheritance, admission, publication, authority, approval,
  endorsement, readiness, retry permission, or execution permission.

The PR #81 and PR #82 merges are treated as causal joins. Their later PR #83
admission anchor is outside this frontier and is not silently inherited
backward into either merge.

The checker performs no provider call and no Pair-001 repetition.
