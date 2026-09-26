# Fork 2 — kernel v0.1

Fork 2 begins as a small executable semantic kernel, not as a rewrite of historical Fork.

Historical repository state remains preserved. This directory is a prospective successor surface anchored at `main@27a243badd1e7645cd47d8ddf1e293865aa18e8f`.

## Current operative semantic core

The first kernel implements only the four relations already frozen through the completed Fork 2 eligibility → decision → authorization sequence:

- **R3 — selection does not expand standing.** Selecting a state does not by itself expand that state's epistemic standing.
- **R5 — later rules do not rewrite historical transition results.** A later rule version does not retroactively rewrite a preserved result/disposition bound to an earlier transition.
- **R7a — failed attempts remain addressable without entering the default qualified route.**
- **R7b — unresolved attempts remain addressable without entering the default qualified route.**

The kernel deliberately does **not** enforce the five relations that remain withheld pending more evidence:

- R1 — lineage membership does not supply epistemic standing.
- R2 — selection may route only to an already qualified state; selection does not create qualification.
- R4 — a transition result is evaluated against the exact rule version bound to that transition.
- R6 — a candidate rule may not govern its own adoption.
- R8 — a failed attempt carries sufficient bindings for reconstruction without author memory.

Those withheld relations are represented in `status.json`; they are not silently promoted into code.

## Why this exists

Fork's historical implementation concentrated on preserving recomputable evidence of bounded workflow handoffs. Fork 2 keeps that history but moves the executable center one level lower: preserving and checking which semantic consequences may legitimately survive a transition.

The first build therefore favors a minimal rule:

```text
FROZEN SEMANTIC RELATION
→ EXECUTABLE CHECK

WITHHELD RELATION
→ EXPLICIT STATUS ONLY
```

## Files

- `model.py` — immutable record types used by the kernel.
- `kernel.py` — executable checks for R3, R5, R7a, and R7b.
- `status.json` — frozen/withheld relation standing.
- `../tests/test_fork2_kernel_v0_1.py` — positive and hostile tests.

## Current boundary

This is not a production runtime, policy oracle, authorization engine, universal lineage ontology, or frozen storage topology.

The implementation may change. The four frozen relations may not be violated by a valid Fork 2 successor without an explicit successor process that reopens or supersedes their standing.

## Immediate build sequence

1. Establish this minimal semantic kernel.
2. Pressure it with branching, merging, multiple rule changes, competing selections, and partial reconstruction.
3. Admit only evidence that survives independent recomputation.
4. Close withheld relations separately when their missing pressure surfaces are actually satisfied.
5. Only then choose larger implementation topology from evidence rather than from historical habit.
