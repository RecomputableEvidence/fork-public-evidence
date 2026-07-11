# Historical Authority Accretion Experiment Draft v0.1

Status: deferred draft; not admitted; no baseline execution authorized
Dependency: Authority State Invariance and Transition Model v0.1
Relationship to CSH: separate future experiment; Cross-System Claim Handoff v0.1 remains unchanged

## 1. Research question

Does explicit preservation of recorded validity state, authority state, reliance class, lineage roots, non-claims, and transition events reduce implicit authority accretion through repeated reuse?

## 2. Draft hypothesis

Across otherwise comparable multi-cycle reuse chains, Fork-instrumented chains will exhibit a lower rate of observed reliance exceeding recorded validity, permitted-use, or authority conditions than uninstrumented chains.

This is a draft hypothesis only. It is not preregistered and MUST NOT be represented as an active experiment.

## 3. Candidate chain

```text
source observation
-> system A summary
-> human review note
-> system B planning artifact
-> system C recommendation
-> later execution rationale
```

The control condition preserves ordinary references. The instrumented condition additionally preserves validity transitions, authority transitions, reliance events, lineage roots, independent validations, and non-claims.

## 4. Candidate outcomes

- Authority Drift Rate: evaluated reliance events whose observed use exceeds recorded authority scope divided by all evaluated reliance events.
- Permitted-Use Misalignment Rate.
- Validity-State Misalignment Rate.
- Non-Claim Survival Rate.
- Expired-State Reuse Rate.
- Context-Transfer Misalignment Rate.
- Revalidation-as-Authorization Misclassification Rate.
- `DVG`, `DVR`, `PCI_count`, and `PCI_ratio` as descriptive lineage indicators.

No metric is a truth, compliance, legitimacy, or risk score.

## 5. Baseline-protection requirements

Before execution, a future preregistration MUST freeze:

- scenarios and source boundaries;
- control and instrumented treatments;
- receiver identities, versions, and access paths;
- reliance-class classification rules;
- authority and validity transition rules;
- non-claim materiality rules;
- lineage-root and independent-validation rules;
- exclusions, amendments, and missing-data treatment;
- planned statistical and descriptive analyses.

Optimization is prohibited until the unoptimized baseline is complete, sealed, synthesized, and independently recomputed.

## 6. Required preservation

Every chain step must preserve raw input, raw output, claim and non-claim state, context, lineage roots, declared reliance, observed reliance, transition-event references, checker version, component compatibility results, disagreements, and hashes.

## 7. Non-claims

The future experiment will not establish truth, legal sufficiency, compliance, authority-basis validity, production readiness, general effectiveness across all domains, answerability, liability, or permission to execute.

Fork will remain out-of-band, read-only, fail-open, and detect-only. External governance or runtime systems decide whether to permit, deny, escalate, or remediate an action.

## 8. Admission status

This draft is a shaped experimental seam only. It MUST be registered as deferred in the Experimental Extension Protocol. It MUST NOT modify or delay the Cross-System Claim Handoff v0.1 baseline.
