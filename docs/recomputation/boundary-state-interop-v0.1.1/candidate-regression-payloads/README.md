# Candidate Regression Payloads — Boundary-State Interop v0.1.1

These payloads are human-review candidates derived from the exterior verification report. They are intentionally separated from the shipped v0.1.1 regression suite.

## Categories

- `bypass-candidates/`: schema-valid paraphrases that the current checker accepts, but which may carry reliance/no-further-review semantics to a human reader.
- `false-positive-candidates/`: schema-valid benign technical metadata sentences that the current checker rejects because trigger words appear in unrelated technical senses.

## Status

These files are triage candidates, not normative conformance fixtures.

They should not be wired into required CI until the project decides whether the intended checker posture is strict phrase-list linting, context-scoped linting, or explicitly best-effort semantic linting.