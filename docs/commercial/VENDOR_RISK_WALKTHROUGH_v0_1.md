# Vendor Risk Walkthrough v0.1

## Demonstrating Recomputable Evidence for an AI-Assisted Vendor Review

---

## Objective

This walkthrough illustrates how Fork preserves the governance context surrounding an AI-assisted vendor-risk assessment.

The example is illustrative only.

It demonstrates the preservation of evidence boundaries rather than prescribing a specific procurement or compliance process.

---

## Scenario

An organization is evaluating a prospective software vendor.

The reviewer asks an AI assistant to summarize:

- security documentation
- compliance certifications
- contractual limitations
- publicly available documentation

The AI produces a draft vendor-risk assessment.

A human analyst reviews the draft before it is shared with procurement and legal.

Fork preserves the governance context surrounding this transition.

---

## Step 1 - Workflow initiation

### Business purpose

Evaluate Vendor X for potential procurement.

### Workflow owner

Vendor Risk Management.

### Participants

- Vendor Risk Analyst
- AI Assistant
- Procurement
- Legal
- Information Security

Fork records:

- workflow identifier
- purpose
- review context
- initiating authority
- timestamp

---

## Step 2 - AI-assisted artifact generation

The analyst requests:

> Summarize the vendor's security posture and identify potential review questions.

The AI generates:

- document summary
- identified certifications
- observed security controls
- suggested follow-up questions

Fork records:

- prompt context
- AI-generated artifact
- artifact identifier
- referenced evidence
- generation timestamp

Fork does not evaluate whether the summary is correct.

---

## Step 3 - Human review

The analyst reviews the draft.

Actions include:

- correcting inaccuracies
- removing unsupported conclusions
- adding internal observations
- rejecting speculative statements

Fork records:

- reviewer identity
- review timestamp
- accepted changes
- rejected content
- reviewer comments

The resulting artifact becomes eligible for internal circulation.

---

## Step 4 - Claim boundary preservation

Fork associates the reviewed artifact with explicit claim boundaries.

### Supported

- Vendor documentation was reviewed.
- Specific certifications were observed.
- Review questions were generated.

### Not established

- Vendor is approved.
- Vendor is compliant.
- Vendor satisfies organizational policy.
- Procurement should proceed.

Fork preserves both the claims and the explicit non-claims.

---

## Step 5 - Boundary transition

The reviewed assessment is shared with Procurement and Legal.

Fork creates a Boundary Delta Record describing:

- artifact transferred
- claims preserved
- non-claims preserved
- workflow transition
- receiving role
- structural verification status

No authority transfers with the artifact.

---

## Step 6 - Downstream reliance

Procurement references the assessment during its review.

Legal independently evaluates contractual obligations.

Each organization performs its own review.

Fork records that the assessment became part of a downstream workflow without asserting that either team adopted or relied upon every statement.

---

## Step 7 - Later review

Months later, Internal Audit reviews the procurement decision.

Instead of reconstructing events from fragmented records, reviewers can inspect:

- original workflow purpose
- AI-assisted draft
- reviewer modifications
- evidence references
- preserved claim boundaries
- transition records
- downstream reliance events
- structural verification results

Without this preserved record, reviewers would typically rely on logs, document versions, and stakeholder recollection, which may not preserve original claim boundaries or review intent.

Fork supports reconstruction without replacing organizational judgment.

---

## Outcome

Fork does not determine whether the procurement decision was correct.

Fork preserves enough governance context for later reviewers to independently understand:

- what occurred
- what evidence was referenced
- what claims were established
- what claims remained outside scope
- how the artifact moved through the workflow
- whether the preserved record continues to verify

---

> Illustrative example only. This document is not a production customer record, legal opinion, compliance determination, or evidence of an actual vendor-risk decision.
