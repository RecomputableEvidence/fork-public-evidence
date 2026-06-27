ESAL Independent Reproduction Gap Report v0.1

Document ID: ESAL_INDEPENDENT_REPRODUCTION_GAP_REPORT_v0_1
Status: Draft v0.1
Intended path: reports/ESAL_INDEPENDENT_REPRODUCTION_GAP_REPORT_v0_1.md
Applies to: ESAL v0.1 independent reproduction readiness.
Primary spec: spec/BDR-ESAL-v0.1.md
Boundary posture: Preservation without inheritance.

---

1. Purpose

This report records the current gap between ESAL’s branch-visible conformance evidence and full independent reproduction.

It is not a failure report.

It is a boundary-preserving readiness report.

---

2. Current strength

ESAL now has a normative specification path:

- spec/BDR-ESAL-v0.1.md

This materially improves the ability of an independent evaluator to implement replay behavior without reading the reference implementation.

The current branch also contains ESAL-oriented docs, test vectors, expected outputs, tools, and reports.

This supports the next step: packaging those assets for independent reproduction.

---

3. Remaining gap

Independent reproduction is not yet established.

The main gap is not conceptual.

The main gap is evidentiary:

A second implementation has not yet reproduced the expected ESAL states, fingerprints, and failure classes from the public specification and vector corpus.

---

4. Gap register

Gap token | Status | Meaning | Closure condition
----------|--------|---------|------------------
INDEPENDENCE_UNESTABLISHED | Open | No second implementation reproduction is preserved | Independent implementation produces matching results
VECTOR_BUNDLE_UNNORMALIZED | Open | Existing vectors are useful but not yet packaged as a clean reproduction corpus | Dedicated reproduction vector bundle exists
FINGERPRINT_EXPECTATIONS_INCOMPLETE | Open | Expected fingerprints may not be bound for every successful vector | Fingerprint records added for all successful vectors
FAILURE_CLASS_BINDING_INCOMPLETE | Open | Failure vectors may not all preserve required error class expectations | Failure records added for all failing vectors
COMMAND_BINDING_INCOMPLETE | Open | Expected outputs may not all preserve command and commit metadata | Each expected output records command and commit
IMPLEMENTATION_PROVENANCE_ABSENT | Open | No external implementation provenance is preserved | Independent reproduction report records executor, tool, environment, and commit

---

5. Recommended closure sequence

Step 1 — Normalize reproduction vectors

Create a dedicated reproduction vector bundle:

- esal-tests/reproduction/

The bundle should include positive, adversarial, malformed, expected, and fingerprint artifacts.

Step 2 — Bind expected fingerprints

For every successful replay vector, preserve:

- canonical state
- SHA-256 fingerprint
- command
- commit
- implementation version
- limitations

Step 3 — Bind expected failure classes

For every failing vector, preserve:

- expected result
- expected error code
- expected failure phase
- command
- commit
- limitations

Step 4 — Publish independent implementation instructions

Create a minimal instruction file explaining how a second implementer should reproduce the results from the spec.

Step 5 — Preserve external reproduction report

When an independent evaluator runs the corpus, preserve a report containing:

- implementation name
- implementation repository or archive reference
- executor identity or role
- execution timestamp
- command
- environment
- commit
- vector results
- matched / mismatched fingerprints
- limitations
- non-claims

---

6. What closure would establish

Closing these gaps would establish:

- ESAL v0.1 replay behavior was independently reproduced under declared conditions.

It would not establish:

- Legal sufficiency.
- Compliance.
- Safety.
- Truth.
- Approval.
- Runtime authorization.
- Institutional endorsement.
- External authority.
- Host-system conformance.

---

7. Current determination

Current status:

- INDEPENDENT_REPRODUCTION_NOT_YET_ESTABLISHED

Recommended next status target:

- REPRODUCTION_PACKET_READY

Final target after external run:

- INDEPENDENT_REPRODUCTION_ESTABLISHED_WITH_LIMITATIONS

---

8. Summary

Fork has now moved from a spec-stub exposure to a spec-backed replay model.

The next credibility threshold is independent reproduction.

This report exists to keep that threshold explicit, bounded, and reviewable.
