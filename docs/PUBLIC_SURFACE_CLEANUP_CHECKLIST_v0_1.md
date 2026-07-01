# Public Surface Cleanup Checklist v0.1

## Purpose

This checklist tracks the cleanup work needed before treating the public surface as ready for cold legal, compliance, procurement, and audit reviewers.

Fork's current evidence supports an engineering pattern and a motivated hypothesis, not a proven general systems theory.

## Required Before Cold Legal / Compliance Review

### 1. Character Encoding

- [ ] Search for mojibake artifacts.
- [ ] Repair `Ã`, `Â`, `â€™`, `â€œ`, `â€`, `â€“`, `â€”`, and corrupted arrow artifacts.
- [ ] Confirm files are UTF-8 without BOM where practical.
- [ ] Confirm no unintended semantic changes were introduced.

### 2. Root README Compression

- [ ] Reduce `README.md` to a short public entry surface.
- [ ] Keep primary reviewer path only.
- [ ] Move detailed routing to `docs/REVIEWER_ROUTING_GUIDE_v0_1.md`.
- [ ] Preserve explicit non-claims.
- [ ] Preserve verification quickstart.
- [ ] Keep buyer / pricing content bounded and clearly marked as indicative.

### 3. Routing Discipline

- [ ] Root README points to one primary path.
- [ ] Technical validation, non-claim, research, and pilot paths live in the routing guide.
- [ ] No contradictory or duplicative routing blocks remain.

### 4. Link Integrity

- [ ] Run grep for outdated `rrelease_packages`.
- [ ] Confirm all `release_packages/` links are spelled correctly.
- [ ] Confirm new research, evaluation, and reviewer-note links resolve.

### 5. Commit Discipline

- [ ] Keep encoding / README cleanup separate from research-package commits.
- [ ] Do not mix unrelated experimental changes unless intentionally scoped.
- [ ] Review `git diff --stat` before staging.
- [ ] Avoid `git add .` unless the full working tree has been reviewed.

## Non-Claims

This checklist does not certify that the public surface is legally sufficient, compliance-ready, production-ready, or complete.

It records cleanup criteria for reviewer-facing legibility and boundary discipline.
