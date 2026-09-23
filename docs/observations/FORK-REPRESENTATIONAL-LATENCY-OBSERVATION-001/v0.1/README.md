# RLO-001 — representational latency observation v0.1

This is a descriptive, coordinate-bound, non-scored specimen. Main at `4e80ee7f33ac890c4101d741cf3da93522d2fd33` contains PR #164's CSH-S001 freezes and blocked hosted gates, while the designated standing route still names v0.7 and describes the successor as being prepared. The pre-repair routing checker passes 11/11 checks.

Read `OBSERVATION.json` for exact coordinates, distinctions, and source bindings. `sources/` preserves the exact bytes examined before repair. `SHA256SUMS` binds this observation package, excluding itself. Git commit ordering records preservation before the later repair commit; capture time is not a trusted timestamp.

## Bounded finding

The designated interpreted state fell behind admitted evidence, but the repository retained sufficient state to reconstruct this divergence and repair present orientation without mutating predecessor artifacts.

PR #161 is already represented by v0.7's delta despite its PR #160 base coordinate. PR #163 is partially mentioned in routing but missing from the register delta. PR #164's explicit freezes overtake the preparation wording. PR #165 is open branch context only, not an admitted transition. Frozen measurement and execution-record semantics do not mean the receiver registry, run order, or complete experiment is frozen.

A reviewer could reasonably mistake the designated representation for the latest admitted state. Actual reviewer reliance, harm, causal attribution to AI acceleration, and earliest detection time are not established.

## Recompute

With a full repository clone, verify `SHA256SUMS` using Python/hashlib or `sha256sum -c SHA256SUMS` from this directory. Each source has a commit, Git blob ID, SHA-256, and preserved copy. Compare `git show <commit>:<path>` with that copy. PR #165 source bytes are included even if its branch later disappears; its commit is not asserted to be a main ancestor. `ROUTING_CHECK_BEFORE_REPAIR.json` records the original checker output; the original checker and routes are preserved alongside it.

## Boundaries

```text
PRESERVATION != SYNCHRONIZATION
PRESERVED != CURRENTLY INTERPRETED
CURRENTLY INTERPRETED != CURRENTLY REPRESENTATIVE
```

No score, severity threshold, semantic weight, or universal latency metric is introduced. No predecessor standing register, experiment, or closed research object is changed. A successor may restore orientation after this specimen has been committed. The specimen alone does not prove the original broad thesis.
