# Fork Sequence Surface v0.1

## Purpose

The Fork Sequence Surface makes ordered progression independently inspectable. It records what was observed, which gate or classification followed, what authority was or was not present, which stopping rule applied, and which successor states were declared without turning that record into a workflow engine.

The sequence itself is the inspection subject. A reviewer should be able to distinguish historical evidence, control publication, excluded diagnostics, external authorization, readiness, execution, and interpretation without reconstructing their order from unrelated files or trusting a mutable status field.

## Architectural position

The Sequence Surface is introduced as a candidate cross-surface inspectability projection. It does not modify the six admitted modular surfaces and is not represented as an admitted seventh surface before separate review and anchoring.

It is distinct from the Transition Surface. The Transition Surface inspects semantic and evidentiary deltas across a boundary. The Sequence Surface orders references to observations and controls across surfaces. It does not reinterpret those referenced artifacts or decide the consequence of a delta.

It is also distinct from orchestration. The Sequence Surface may expose a declared successor and its unmet requirements. It may not schedule the successor, satisfy the requirement, create authority, make a provider call, promote readiness, or execute Pair-001.

## Three-layer model

### Append-only ledger

The ledger records ordered events. Each event includes:

- an ordinal and stable identifier;
- a declared transition;
- prior and resulting sequence states;
- the recorded authority requirement and effect;
- bounded observed-call deltas;
- byte-bound evidence references;
- a hash-chain link;
- explicit non-claims.

Later events may explain, classify, or supersede an operational path. They may not rewrite or delete an earlier event.

### Transition contract

The transition contract declares permitted state changes, exact effects, authorization requirements, stopping branches, and forbidden promotions. The ledger is checked against the contract; it is not accepted merely because it contains plausible state names.

The contract predeclares the current DeepSeek branches:

- one byte-identical uppercase diagnostic only after separate explicit authorization and the fixed 24-hour gap;
- freshness validation and a separate readiness anchor after success;
- a terminal stop on an identical failure;
- classification before any different-outcome continuation;
- a separately authorized lowercase diagnostic only after the identical uppercase failure;
- `CSH-AMEND-004` and a new receiver/version stratum after lowercase success.

None of those branches automatically completes or executes Pair-001.

### Deterministic projection

The checker derives current state, counters, blockers, declared successors, and execution effect from the ledger plus the referenced control artifacts. It then compares the derived object with the committed projection.

The committed projection is a receipt of recomputation, not an authority source. Editing it cannot change the checker's result because the checker recomputes it independently.

## Pair-001 reference instance

The reference ledger orders:

1. the two preserved original Pair-001 attempts;
2. the instrumentation repair and successor-control proposal;
3. publication of the instrumentation release anchor;
4. three excluded provider-validation diagnostics;
5. the fail-closed validation disposition;
6. the unresolved receiver-drift classification;
7. reconciliation of the mutable publication projection.

The projection therefore exposes both historical provider activity and the present block:

- eight provider calls are observed in the referenced history;
- two are preserved original Pair-001 attempts;
- six are excluded provider-validation calls;
- zero are Pair-001 repetitions;
- the DeepSeek cause remains `UNRESOLVED`;
- the provider request remains blocked;
- retry authorization is absent;
- readiness and execution effects remain `NONE`.

## Adversarial coverage

The fixture set requires rejection of:

- a skipped gate;
- reordered events;
- forged authorization;
- a silent provider retry hidden inside a non-call event;
- false Pair-001 completion or execution eligibility.

The checker also rejects duplicate JSON keys, non-finite values, broken event hashes, path escape, symlink substitution, missing evidence, digest divergence, undeclared transitions, and projection tampering.

The hash chain does not defeat coordinated re-sealing by itself. The separate successor anchor is required to bind the admitted ledger, checker, schema, projection, exact merge commit, and successful workflow runs from outside the candidate change.

## Verification

From the repository root:

```powershell
python ./tools/check_fork_sequence_surface_v0_1.py --json
python -m pytest ./tests/test_fork_sequence_surface_v0_1.py
```

A passing result establishes only that the declared sequence is structurally ordered, byte-bound to its referenced repository artifacts, consistent with the transition contract, and deterministically projected under the checker.

## Successor anchor boundary

This candidate PR cannot contain its own admission anchor. A valid anchor requires facts unavailable until after merge: the exact merge commit, the admitted tree, and the completed workflow runs at the reviewed head.

The anchor must therefore be append-only and published in a separate successor change. It must have no provider-call, Pair-001 execution, or readiness effect.

## Non-claims

- Sequence conformance is not truth or correctness.
- An allowed successor is not an authorization to take it.
- Elapsed time is not authorization.
- Publication and review are not provider-execution authority.
- A diagnostic is not an experiment repetition.
- Projection is not approval, compliance, safety, legal sufficiency, production readiness, or institutional authority.
- The Sequence Surface does not own or automate downstream consequences.
