# Repository Admission Instructions — v0.1.1

## Purpose

Admit this repair successor without rewriting either the repository predecessor baseline or v0.1.0.

## Predecessor boundaries

Repository predecessor:
- commit: `c51e28ac44104808e957c0dae73f98f262728fec`
- tree: `415f27fdf73e56a0cfa7c01098c715af118c02bb`

Semantic package predecessor:
- `FORK-HANDOFF-SEMANTIC-CORE-001-v0.1.0.zip`
- SHA-256: `baa112e3260decf707f0ed95578257c0deaa475bc43f30c9c2fc91747b674cf2`

Do not rewrite either coordinate.

## Required pre-admission checks

1. Independently verify the repository predecessor commit resolves to the declared tree.
2. Verify the v0.1.0 predecessor package SHA-256 if the predecessor ZIP is available.
3. Run all commands in `08_EXECUTION_PROTOCOL.md` with bytecode generation disabled.
4. Require 4/4 valid fixtures PASS, 15/15 adversarial fixtures FAIL, 19/19 expectations matched, 15/15 invariant fixture coverage, unit tests PASS, and closure verification PASS.
5. Require zero packaged `.pyc` / `__pycache__` files and zero undeclared package paths.
6. Verify `SHA256SUMS` according to `15_CLOSURE_VERIFICATION.py`.

## Recommended admission sequence

1. Create a successor branch from the exact repository predecessor commit.
2. Admit the complete `FORK-HANDOFF-SEMANTIC-CORE-001-v0.1.1` directory unchanged.
3. Re-run the required execution at the admission commit.
4. Record the admission commit separately from both predecessor coordinates.
5. Add a current-standing successor overlay only after admission exists; do not rewrite prior overlays.
6. Preserve v0.1.0 and its external assessment as historical predecessor evidence.
7. Do not begin `FORK-EXTERNAL-WITNESS-BINDING-001` by modifying this object; create it as a separately identified successor object.

## Required admission non-claims

Repository admission must not be described as establishing universal semantic correctness, truth, completeness, cryptographic integrity, independent witnessing, provenance authenticity, trusted chronology, authority, authorization, compliance, legal sufficiency, safety, production readiness, external reproduction of v0.1.1, or generalization.
