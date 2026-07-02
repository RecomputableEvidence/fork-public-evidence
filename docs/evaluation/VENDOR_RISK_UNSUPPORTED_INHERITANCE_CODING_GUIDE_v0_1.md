# Vendor Risk Unsupported Inheritance Coding Guide v0.1

## Status

Draft coding guide for the vendor-risk handoff evaluation.

This guide supports the Accountable Handoff Interoperability evaluation path after `ahi-v0.1.2`.

Fork's current evidence supports an engineering pattern and a motivated hypothesis, not a proven general systems theory.

## Purpose

This guide defines how to identify and code unsupported inheritance events during vendor-risk handoff evaluation.

It is intended to make evaluation results inspectable, repeatable, and challengeable by later reviewers.

## Core Evaluation Question

Do explicit handoff-state artifacts reduce unsupported inheritance events in AI-assisted vendor-risk workflows compared with ordinary workflow artifacts and logs alone?

## Variables

Let `U` represent the rate of unsupported inheritance events per workflow.

Let `H` represent the presence of explicit handoff-state artifacts.

The hypothesis predicts:

```text
E[U | H = 1] < E[U | H = 0]
```

Where:

- `H = 0` means baseline review using ordinary artifacts and logs only.
- `H = 1` means treatment review using the same artifacts plus Fork-style Boundary Records.

## Definition: Unsupported Inheritance Event

An unsupported inheritance event occurs when a reviewer, participant, or downstream artifact treats a claim, authority basis, approval status, compliance status, validation status, or reliance basis as established even though the provided record does not explicitly support that inheritance.

## Binary Coding Test

Code an event as `UNSUPPORTED_INHERITANCE` when any of the following are true:

- A downstream actor relies on a claim with missing provenance.
- A downstream actor treats authority as granted when authority was not explicitly recorded.
- A downstream actor treats a policy reference as policy approval.
- A downstream actor treats structural verification as factual correctness.
- A downstream actor treats an unresolved issue as resolved.
- A downstream actor treats evidence preservation as compliance certification.
- A downstream actor treats human review as legal, compliance, procurement, or institutional sufficiency.
- A downstream actor expands claim scope beyond the recorded boundary without new authority or evidence.
- A downstream actor treats a bounded example workflow as a validated or recommended general pattern.
- A downstream actor treats a Fork record as approval, certification, authorization, or production readiness.

## Do Not Code as Unsupported Inheritance

Do not code an event as unsupported inheritance merely because:

- A reviewer asks a question about authority, compliance, approval, or sufficiency.
- A record references a policy while clearly preserving the policy-reference non-claim.
- A reviewer identifies an unresolved issue without treating it as resolved.
- A downstream actor narrows reliance scope.
- A downstream actor requests additional evidence or revalidation.
- A reviewer correctly distinguishes structural verification from factual correctness.
- A reviewer correctly states that Fork does not decide whether reliance is justified.

## Event Categories

Use one primary category per event.

| Category                          | Meaning                                                                     |
|-----------------------------------|-----------------------------------------------------------------------------|
| `CLAIM_SCOPE_EXPANSION`          | A claim is treated as broader than recorded                                 |
| `AUTHORITY_LEAKAGE`             | Authority is inferred or transferred without explicit basis                |
| `POLICY_APPROVAL_CONFUSION`     | Policy reference is treated as policy approval or applicability             |
| `COMPLIANCE_CERTIFICATION_CONFUSION` | Evidence preservation or verification is treated as compliance certification |
| `LEGAL_SUFFICIENCY_CONFUSION`   | Human review or record integrity is treated as legal sufficiency           |
| `FACTUAL_CORRECTNESS_CONFUSION` | Structural verification is treated as truth or correctness                  |
| `RESOLUTION_CONFUSION`          | An unresolved issue is treated as resolved                                  |
| `PRODUCTION_READINESS_CONFUSION`| A bounded record is treated as production approval or readiness             |
| `RELIANCE_BASIS_AMBIGUITY`      | Reviewer cannot determine what was relied upon or why                       |
| `OTHER_UNSUPPORTED_INHERITANCE` | Unsupported inheritance not captured above                                  |

## Required Coding Fields

Each counted event should record:

| Field               | Required | Description                                             |
|---------------------|----------|---------------------------------------------------------|
| `event_id`          | Yes      | Stable event identifier                                 |
| `condition`         | Yes      | `BASELINE` or `TREATMENT`                               |
| `workflow_id`       | Yes      | Workflow or scenario identifier                         |
| `category`          | Yes      | Event category from this guide                          |
| `actor_or_artifact` | Yes      | Who or what made the inference                          |
| `inferred_claim`    | Yes      | What was inferred                                       |
| `record_support`    | Yes      | What the record actually supported                      |
| `why_unsupported`   | Yes      | Why the inference exceeded the record                   |
| `evidence_refs`     | Yes      | Relevant artifacts, lines, packets, or notes            |
| `coder_id`          | Yes      | Person or role coding the event                         |
| `adjudication_status` | Yes    | `UNREVIEWED`, `AGREED`, `DISPUTED`, or `RESOLVED`       |
| `adjudication_note` | No       | Resolution rationale if disputed                        |

## Canonical Positive Example

**Scenario**

A baseline reviewer receives an AI-assisted vendor-risk memo and ordinary workflow notes. The memo says a vendor was reviewed by a human analyst. The reviewer writes: "The vendor appears approved for low-risk onboarding."

**Coding**

Code as `UNSUPPORTED_INHERITANCE`.

Category: `AUTHORITY_LEAKAGE`.

**Reason**

The record indicates human review occurred, but it does not establish approval authority, approval status, legal sufficiency, compliance determination, or onboarding authorization.

## Canonical Negative Example

**Scenario**

A treatment reviewer receives the same memo plus a Fork Boundary Record. The reviewer writes: "The record shows a human review occurred, but approval authority and compliance status are not established."

**Coding**

Do not code as unsupported inheritance.

**Reason**

The reviewer preserved the boundary between observed review, authority, approval, and compliance.

## Ambiguous Example

**Scenario**

A reviewer writes: "The packet verifies, so the decision appears supportable."

**Coding**

Potentially code as `UNSUPPORTED_INHERITANCE`.

Category: `FACTUAL_CORRECTNESS_CONFUSION`.

**Adjudication Question**

Did the reviewer mean structural verification only, or did the reviewer treat structural verification as factual or institutional sufficiency?

If unclear, record as disputed and adjudicate.

## Inter-Rater Guidance

When two coders disagree:

- Preserve both initial codes.
- Identify the disputed inference.
- Identify what the record explicitly supported.
- Decide whether the downstream statement exceeded the record.
- Record the adjudication rationale.

Do not hide evaluator disagreement. Disagreement is itself evidence about whether the boundary record improved reviewer convergence.

## Non-Claims

This guide does not claim that Fork reduces unsupported inheritance.

This guide does not establish statistical validity.

This guide does not certify legal, compliance, procurement, audit, operational, production, or institutional sufficiency.

This guide defines a bounded coding method for initial evaluation only.