cd C:\N\fork-public-evidence

@'
# Vendor Risk Handoff Study Protocol v0.1

## Status

Draft study protocol for evaluating whether explicit handoff-state artifacts reduce unsupported inheritance in AI-assisted vendor-risk workflows.

This protocol is part of the Accountable Handoff Interoperability v0.1.1 public-surface hardening work.

## Research Posture

Fork's current evidence supports an engineering pattern and a motivated hypothesis, not a proven general systems theory.

This protocol does not establish that Fork improves reviewer performance. It defines how that claim could begin to be tested.

## Study Question

Do explicit handoff-state artifacts reduce unsupported inheritance events in AI-assisted vendor-risk workflows compared with ordinary workflow artifacts and logs alone?

## Hypothesis

Let `U` represent the rate of unsupported inheritance events per workflow.

Let `H` represent the presence of explicit handoff-state artifacts.

The hypothesis predicts:

```text
E[U | H = 1] < E[U | H = 0]
```

Where:

- `H = 0` means reviewers receive ordinary workflow artifacts and logs without explicit handoff-state records.
- `H = 1` means reviewers receive the same materials plus explicit Fork-style Boundary Records.

If controlled or quasi-controlled evaluation fails to show reduced unsupported inheritance, reliance ambiguity, or authority leakage in the boundary-record condition, the hypothesis is weakened or requires refinement.

## Study Design

Initial design: quasi-experimental reviewer reconstruction study.

Two review conditions are compared.

### Baseline Condition

Reviewers receive:

- an AI-assisted vendor-risk recommendation;
- an internal decision memo;
- ordinary supporting artifacts or logs;
- no explicit handoff-state record.

### Treatment Condition

Reviewers receive the same materials as the baseline condition plus explicit handoff-state artifacts identifying:

- claims made;
- evidence referenced;
- authority or policy context recorded;
- exclusions;
- unresolved issues;
- required revalidation;
- downstream reliance attempts;
- non-claims preserved.

## Primary Endpoint

Rate of unsupported inheritance events per workflow.

An unsupported inheritance event occurs when a reviewer, workflow participant, or downstream artifact treats a claim, authority basis, approval status, compliance status, validation status, or reliance basis as established even though the provided record does not explicitly support that inheritance.

### Binary Test for Unsupported Inheritance

A potential unsupported inheritance event should be counted when any of the following is true:

- a downstream actor relies on a claim with missing provenance;
- a downstream actor treats authority as granted when authority was not explicitly recorded;
- a downstream actor treats policy reference as policy approval;
- a downstream actor treats structural verification as factual correctness;
- a downstream actor treats an unresolved issue as resolved;
- a downstream actor treats evidence preservation as compliance certification;
- a downstream actor treats human review as legal or institutional sufficiency;
- a downstream actor expands claim scope beyond the recorded boundary without new authority or evidence.

## Secondary Endpoints

Secondary measures include:

- number of inferred approvals;
- number of missing authority links;
- number of unresolved issues incorrectly treated as resolved;
- number of policy references misread as policy approvals;
- reviewer disagreement rate;
- time required to reconstruct reliance basis;
- number of clarification loops required;
- reviewer confidence in what was established;
- reviewer confidence in what was not established.

## Evaluator Roles

At minimum, each workflow should be reviewed by:

- one primary reviewer simulating legal, compliance, audit, procurement, or risk review;
- one independent evaluator coding unsupported inheritance events;
- one adjudicator resolving disagreement between evaluators where needed.

Evaluator disagreement should be recorded rather than hidden.

### Inter-Rater Agreement

Where two or more evaluators code unsupported inheritance events, the study should record:

- total coded events per evaluator;
- disagreements;
- resolved event count;
- rationale for resolution.

The goal is not to force artificial certainty. The goal is to determine whether explicit handoff-state records improve reviewer convergence.

## Inclusion Criteria

A workflow may be included when:

- an AI-assisted artifact influenced a vendor-risk recommendation, triage, memo, or decision support artifact;
- the artifact crossed at least one institutional boundary;
- a downstream reviewer could plausibly infer approval, authority, compliance status, completeness, or reliance sufficiency;
- sufficient ordinary workflow materials exist to create a baseline condition.

## Exclusion Criteria

A workflow should be excluded when:

- no AI-assisted artifact was involved;
- no handoff occurred;
- the workflow did not involve institutional reliance;
- ordinary workflow materials are unavailable;
- the scenario is purely synthetic and cannot be mapped to a plausible institutional review task.

Synthetic scenarios may still be used for pilot testing, but they should be labeled as synthetic.

## Analysis Plan

The initial analysis should compare baseline and treatment conditions on:

- unsupported inheritance rate;
- reviewer disagreement rate;
- reconstruction time;
- clarification-loop count;
- authority-leakage events;
- reliance-ambiguity events.

The hypothesis is strengthened if the treatment condition produces lower unsupported inheritance, lower reliance ambiguity, and higher reviewer agreement without introducing material new confusion.

The hypothesis is weakened if the treatment condition does not improve these measures, or if Boundary Records introduce more ambiguity than ordinary artifacts and logs alone.

## Non-Claims

This protocol does not claim that Fork is effective.

This protocol does not claim statistical validity until actual evaluation data exists.

This protocol does not claim that vendor-risk workflows generalize to other institutional domains.

This protocol does not certify compliance, legal sufficiency, audit sufficiency, procurement sufficiency, production readiness, or institutional authority.

## Result Recording

Evaluation results should be recorded in:

- [`docs/evaluation/VENDOR_RISK_HANDOFF_RESULTS_v0_1.md`](VENDOR_RISK_HANDOFF_RESULTS_v0_1.md)
'@ | Set-Content -Encoding UTF8 docs\evaluation\VENDOR_RISK_HANDOFF_STUDY_PROTOCOL_v0_1.md