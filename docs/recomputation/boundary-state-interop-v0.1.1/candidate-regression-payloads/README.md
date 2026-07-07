# Candidate Regression Payloads â€” Boundary-State Interop v0.1.1

These payloads are human-review candidates derived from the exterior verification report. They are intentionally separated from the shipped v0.1.1 regression suite.

## Categories

- ypass-candidates/: schema-valid paraphrases that should be treated as semantic expansion attempts but are expected to be accepted by the unmodified v0.1.1 checker.
- alse-positive-candidates/: schema-valid benign technical metadata that should be accepted but is expected to be rejected by the unmodified v0.1.1 checker.

## Review posture

These files are not normative profile changes and should not be wired into required CI until triaged. They preserve human-reviewable cases for reviewer recomputation and patch discussion.