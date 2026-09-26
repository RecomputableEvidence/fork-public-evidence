# Fork 2 — kernel v0.1

Fork 2 begins as a small executable semantic kernel, not as a rewrite of historical Fork.

Historical repository state remains preserved. This directory is a prospective successor surface anchored at `main@27a243badd1e7645cd47d8ddf1e293865aa18e8f`.

## Current operative semantic core

The first kernel implements only the four relations already frozen through the completed Fork 2 eligibility → decision → authorization sequence:

- **R3 — selection does not expand standing.** Selecting a state does not by itself expand that state's epistemic standing.
- **R5 — later rules do not rewrite historical transition results.** A later-rule projection carries an explicit later-rule context and may not rewrite a preserved result/disposition bound to the historical transition's earlier rule.
- **R7a — failed attempts remain addressable without entering the default qualified route.**
- **R7b — unresolved attempts remain addressable without entering the default qualified route.**

R7a/R7b are conjunctive in the executable kernel: FAILED/UNRESOLVED attempts must remain addressable **and** must remain outside the default qualified route.

R5 does not evaluate rule correctness, compare evaluation semantics, or establish rule chronology. `later_rule_id` is projection provenance used to keep the later-rule dimension explicit; exact rule-bound evaluation remains R4 and remains withheld.

The kernel deliberately does **not** enforce the five relations that remain withheld pending more evidence:

- R1 — lineage membership does not supply epistemic standing.
- R2 — selection may route only to an already qualified state; selection does not create qualification.
- R4 — a transition result is evaluated against the exact rule version bound to that transition.
- R6 — a candidate rule may not govern its own adoption.
- R8 — a failed attempt carries sufficient bindings for reconstruction without author memory.

Those withheld relations are represented in `status.json`; they are not silently promoted into code.

## Standing provenance

`status.json` no longer asks a reviewer to accept relation standing as an unbound assertion. `provenance.json` binds every R1–R8 standing entry to the exact predecessor package identities, decision-return hash, authorization record identity, and operative/withheld source registers that produced the current standing.

The canonical standing records needed to traverse eligibility → decision → authorization are copied under `fork2/provenance/` with their original SHA-256 identities bound in `provenance.json`. The predecessor package ZIP bytes themselves are **not** embedded in this PR. Therefore:

```text
EMBEDDED STANDING RECORDS
!=
EMBEDDED FULL SOURCE PACKAGES
```

The provenance surface establishes standing-origin identity and traversal. Full predecessor package recomputation still requires the separately preserved bound source packages.

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

- `__init__.py` — package marker.
- `model.py` — immutable record types used by the kernel.
- `kernel.py` — executable checks for R3, R5, R7a, and R7b.
- `status.json` — frozen/withheld relation standing and exact enforcement map.
- `provenance.json` — machine-readable predecessor/decision/authorization origin binding.
- `provenance/` — exact standing-record copies used by that origin binding.
- `../tests/test_fork2_kernel_v0_1.py` — positive, hostile, aggregation, standing-map, and provenance tests.

## Current boundary

This is not a production runtime, policy oracle, authorization engine, universal lineage ontology, or frozen storage topology.

The implementation may change. The four frozen relations may not be violated by a valid Fork 2 successor without an explicit successor process that reopens or supersedes their standing.

## Immediate build sequence

1. Establish this minimal semantic kernel.
2. Pressure it with branching, merging, multiple rule changes, competing selections, and partial reconstruction.
3. Admit only evidence that survives independent recomputation.
4. Close withheld relations separately when their missing pressure surfaces are actually satisfied.
5. Only then choose larger implementation topology from evidence rather than from historical habit.
