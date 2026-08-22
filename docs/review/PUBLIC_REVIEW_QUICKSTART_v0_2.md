# Fork Public Review Quickstart v0.2

Status: `CANDIDATE_REVIEW_ROUTE`

## Goal

Give a cold reviewer one short path to inspect a bounded proof and one short path to inspect the versioned public-disclosure successor without traversing Fork's full historical corpus.

## 1. Record your exact subject

From a clean clone, record:

- commit hash;
- branch/ref;
- operating system;
- shell;
- Python version;
- Git version.

If reviewing the current successor candidate, the branch context is:

`adoption/five-band-instantiation-v0.1.1-candidate`

Do not describe a moving branch name as an immutable review coordinate; record the exact commit you actually inspect.

## 2. Read the root orientation

Read:

- `README.md`
- `docs/REVIEWER_START_HERE_v0_2.md`

Reviewer question:

> Can I tell what Fork is, what it preserves, what it explicitly does not do, and which route fits my purpose?

## 3. Recompute one bounded proof

From repository root:

```bash
python tools/run_proof_001_review_does_not_silently_travel_v0_1.py --json
```

Interpret only the bounded Proof 001 result. Do not generalize a pass into truth, compliance, safety, production readiness, or authority.

## 4. Inspect the disclosure successor

Read:

`technical-disclosure/v0.1.2/README_VERIFY_PUBLIC_DISCLOSURE_v0_1_2.md`

Then run:

Linux/macOS:

```bash
cd technical-disclosure/v0.1.2
python3 verify_public_disclosure_v0_1_2.py
```

Windows PowerShell:

```powershell
Set-Location .\technical-disclosure\v0.1.2
python .\verify_public_disclosure_v0_1_2.py
```

Record the exact output and exit status.

The v0.1.2 repository successor first runs the inherited exact v0.1.1 verifier and then checks successor-specific repair/lineage conditions. It does not claim that a detached v0.1.2 ZIP release already exists.

## 5. Follow the route that matches your question

- Adoption / integration → `docs/adoption/README.md`
- Research / standing → `docs/research/fork-research-program-v0.1/README.md`
- Failures / correction lineage → `docs/preservation/failure-mode-archive-v0.1/README.md`
- Architecture → `docs/modular-surface/FORK_MODULAR_SURFACE_v0_1.md`
- Exact route metadata → `docs/state/FORK_STATE_ROUTING_v0_5_CANDIDATE.json`

## 6. Record confusion as evidence

If a link is stale, a command is platform-incompatible, a standing is unclear, or two routes appear to conflict, record that condition exactly. Do not silently repair the path in your report.

## 7. Boundary statement

A successful checker execution establishes only the declared structural or semantic condition within that checker's bound scope.

It does not establish truth, legal sufficiency, compliance, safety, authorization, approval, endorsement, production readiness, procurement approval, or institutional authority.
