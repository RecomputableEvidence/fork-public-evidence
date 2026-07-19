# CSH-AMEND-003 — provenance-bound execution governance v0.1.2

Status: proposed; not admitted; not executable.

This instrumentation/security amendment is the natural successor to CSH-AMEND-002. It preserves the complete v0.1 scientific freeze and both original Pair-001 attempts while replacing two live, byte-sealed workflow copies with hardened successors. The original workflow bytes remain available outside `.github/workflows` and retain their SHA-256, Git-blob, source-commit, and amendment lineage.

## Unchanged scientific commitments

The hypothesis, corpus, prompt packets, handoff artifacts, receiver bindings, parameters, fixed run order, classifier, stopping rule, optimization embargo, and 108-unit baseline remain unchanged. CSH-AMEND-003 does not reinterpret either original attempt and does not convert a failed or incomplete provider interaction into a successful run.

## Execution boundary

The amendment creates no receiver authority. Structural readiness is deliberately distinct from executable readiness. Receiver calls remain prohibited until:

1. preservation PR #61 is admitted;
2. claim-admission PR #62 is admitted;
3. the stacked CSH v0.1.2 amendment PR is admitted;
4. the instrumentation release anchor is published against the admitted commit and its required checks succeed; and
5. the operator validates provider identity, credential scope, quota, and receipt destination without exposing credential material.

The checker returns `STRUCTURALLY_READY_EXECUTION_BLOCKED` while any prerequisite is false. `--require-executable` fails closed.

## First authorized operation after admission

CSH-AMEND-002 requires two new, lineage-linked repetitions for affected Pair-001. The exact request bytes must match the preserved originals. New run identifiers and new receipt directories are mandatory. The originals remain immutable, unreplaced, and unsuperseded. Only after those bounded repetitions are preserved may the operator continue through the fixed baseline order without changing the preregistered design.

## Non-claims

This amendment does not establish the hypothesis, receiver correctness, safety, compliance, legal sufficiency, certification, endorsement, production readiness, or institutional authority. It records operational integrity and creates a reviewable path to execution; it does not grant that execution.
