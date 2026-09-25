Fork is a single-author (copyright Ryan Feller) research repository, created June 2026, with 631 commits, no stars or forks, and 18 open PRs against itself. It proposes that explicit "handoff-state" records reduce unsupported inheritance of claims in AI-assisted institutional workflows, and ships Python checkers, JSON schemas, synthetic fixtures, a PowerShell verifier, and a very large volume of governance prose. I read the README, the reviewer entry docs, CURRENT_STANDING, the copyright notice, the verifier script, and the tools/tests/CI listings; I did not clone or execute anything, so this is a structural and editorial review, not a correctness audit.

## What's good

The **non-claim discipline is real, not decorative.** Every surface states what it does not establish (truth, compliance, legal sufficiency, authority), and CURRENT_STANDING is candid that the central experiment (Cross-System Claim Handoff) has a blocked baseline and no corpus execution. Most research repos overclaim; this one is careful to the point of pain.

The engineering scaffolding is more than a sketch: \~60 checker scripts under `tools/`, a matching `tests/` suite, 11 GitHub Actions workflows, JSON schemas, `CHECKSUMS_SHA256.txt`, `CITATION.cff`, a changelog, and release packets with their own verification instructions. Checkers emit `--json` and use exit codes, which is the right contract for recomputation. The PowerShell verifier is clean, PS 5.1-compatible, and fails loudly on non-JSON output.

## Where it falls down

**The repository is mostly about governing itself.** CURRENT_STANDING v0.9 is an "overlay" on v0.8, which is preserved at its own PR horizon; there's a snapshot classifying 18 open PRs; there are "byte admissions," "standing," "freezes," and "intentional stops." A newcomer has to learn a private vocabulary (preservation without inheritance, observance surface, exterior observers, evidence-boundary surface) before they can find out what a Fork artifact actually looks like. The README never shows one. The single most valuable addition would be a 20-line example handoff record on the first screen, followed by the one checker that validates it.

**The root directory is a working tree, not a public surface.** Seventeen `README_*` files sit at the top level alongside `encoding_manual_review.log`, `encoding_repair_manifest.json`, `install_phase2_reconciled_to_repo.ps1`, `remote_mapping_system_v0_1_verification_result.json`, a committed `output/` directory, and both `schema/` and `schemas/`. For a project whose thesis is that reviewers should be able to see cleanly what crossed a boundary, the repo's own boundary between scratch and disclosure is blurry.

**Versioning is done with filenames instead of git.** `check_ai_governance_mapping_record_v0_1.py`, `_v0_2.py`, `_v0_2_1.py`, `_v0_2_2.py` all coexist, each with a paired test. I understand the intent (older receipts must remain recomputable against the exact checker that produced them), but it multiplies maintenance surface and makes it unclear which version a reviewer should trust today. Tags plus a `checkers/` index mapping receipt → checker commit would achieve the same with far less clutter.

**Windows-first verification.** The "one-command" path is a PowerShell script, and the docs explicitly classify running the cross-platform Python commands as "manual reconstruction" rather than "verifier execution." That is a distinction most Linux/macOS reviewers will find odd, and it puts the canonical path on the platform least used by the audience the project is courting. A `python -m fork_verify` or a `Makefile` target that the PowerShell script merely wraps would fix it.

**Licensing is "all rights reserved."** `COPYRIGHT.md` grants permission only to run the synthetic fixture and public verifier for recomputation; no modification, redistribution, or derivative implementation. That's a legitimate choice for a disclosure repo, but there is no `LICENSE` file GitHub recognizes, and the README's language about contributors and an "Exterior Observance Experiment" implies an openness the terms don't grant. State the terms in the README's first section so nobody spends an afternoon on it under a false assumption.

**The evidence is structural, not empirical.** What the checkers verify is that fixtures conform to schemas, checksums match, and required files exist. That supports "this pattern can be specified and recomputed," which the README correctly says. It does not yet touch the actual hypothesis — that these records reduce unsupported inheritance — and the one experiment designed to test it hasn't started. The README's phrase "initial evidence consistent with the hypothesis" is doing more work than the artifacts currently justify.

## Concrete suggestions, in priority order

1. Put a real example artifact and its single validating command at the top of the README; move every disclaimer after it into one linked non-claims doc rather than repeating them per section.
2. Move root `README_*`, logs, result JSONs, and `install_*.ps1` into `docs/history/` or `scratch/`; merge `schema/` into `schemas/`; stop committing `output/`.
3. Collapse versioned checkers to one current file per checker, with a receipt→commit table for historical recomputation.
4. Make the Python entry point canonical and cross-platform; keep the `.ps1` as a thin wrapper.
5. Add a `LICENSE` file matching `COPYRIGHT.md`, and say plainly in the README that this is source-available, not open source.
6. Either run the CSH baseline or reword the README to say the hypothesis is untested rather than "initially supported."
7. Rename or explain the repo name — nothing here is a GitHub fork, and "fork-public-evidence" reads as one.

The underlying idea — recording what a handoff did and did not carry, in a form later reviewers can recompute — is sound and under-served. Right now the repository's own volume and self-referential process are the main obstacle to anyone evaluating it.