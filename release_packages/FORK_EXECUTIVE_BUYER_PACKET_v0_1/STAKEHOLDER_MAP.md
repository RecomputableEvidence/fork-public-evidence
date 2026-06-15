# Stakeholder Map

## Purpose

Fork sits between institutional mechanisms.

An executive buyer conversation should identify which functions own the upstream and downstream responsibilities.

Fork should not absorb those responsibilities.

## Likely stakeholder groups

### General Counsel / Legal

Typical questions:

- What record exists if a decision is challenged?
- What was preserved?
- What changed?
- What cannot be claimed?
- What evidentiary gaps exist?

Fork boundary:

Fork preserves the record.

Fork does not make legal judgments.

### Compliance

Typical questions:

- Were required reviews, approvals, escalations, or exceptions preserved?
- Can later review distinguish PASS, FAIL, NOT_CHECKED, PARTIAL, STALE_CONTEXT, OUT_OF_SCOPE, and SOURCE_UNAVAILABLE?
- What was not captured?

Fork boundary:

Fork supports inspection.

Fork does not satisfy compliance obligations by itself.

### Audit

Typical questions:

- Can the workflow be reconstructed?
- Is the record stable?
- Does the evidence packet verify?
- Are non-claims explicit?

Fork boundary:

Fork provides a stable evidentiary object.

Fork does not perform audit.

### Risk

Typical questions:

- Where did uncertainty accumulate?
- Which dependencies are vendor-controlled?
- What gaps may affect risk posture?
- What evidence remains reviewable?

Fork boundary:

Fork makes uncertainty inspectable.

Fork does not own institutional risk acceptance.

### Security

Typical questions:

- What data is captured?
- What is only hashed or referenced?
- What access model is required?
- What happens when evidence gaps or drift are surfaced?

Fork boundary:

Fork remains read-only and out-of-band.

Fork does not become the incident-response control plane.

### Engineering / AI Infrastructure

Typical questions:

- What systems emit relevant events?
- What exports are available?
- What can be captured without runtime dependency?
- What verification mechanics exist?

Fork boundary:

Fork observes and preserves.

Fork does not route, block, or control the workflow.

### Executive sponsor

Typical questions:

- Why does this matter?
- Which workflow should be evaluated first?
- Who owns the internal response?
- What does a pilot prove?

Fork boundary:

Fork supports pilot evaluation.

Fork does not create a broader production claim.