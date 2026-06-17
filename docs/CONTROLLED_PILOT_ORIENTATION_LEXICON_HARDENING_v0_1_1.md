# Controlled Pilot Orientation Lexicon Hardening v0.1.1

## Purpose

This patch tightens stakeholder-facing terminology in the controlled-pilot orientation layer.

It does not change Fork's controlled-pilot architecture. It reduces the risk that legal, compliance, audit, clinical, utilization-management, security, or operational stakeholders import non-Fork meanings into Fork structural-readiness artifacts.

## Hardening changes

### 1. Replace "zero authorization valence"

The phrase "zero authorization valence" is replaced with plainer institutional language.

Preferred wording:

```text
The presence of this template or reference confers zero authorization by its mere existence. It has no legal, operational, clinical, compliance, or live-ingestion authorization effect by itself.
```

### 2. Define structural readiness

Stakeholder-facing materials now define structural readiness.

Structural readiness refers only to Fork's schema, hash, receipt, template, package-index, and checker validation. It does not mean workflow readiness, clinical readiness, operational readiness, compliance readiness, production readiness, or live-ingestion authorization.

### 3. Replace "support institutional review"

The phrase "Fork outputs may support institutional review" is replaced with:

```text
Fork outputs may serve as structural evidence during institutional review, but do not constitute or replace institutional approval.
```

### 4. Rename ambiguous APPROVED statuses

Bare `approval_status: "APPROVED"` fields are removed from dry-run and orientation artifacts.

Replacement fields:

```text
dry_run_review_status: "DRY_RUN_REVIEWED"
orientation_acknowledgment_status: "ORIENTATION_ACKNOWLEDGED"
```

## Boundary

This patch does not authorize live ingestion, certify production readiness, certify source truth, certify completeness, certify legal admissibility, certify lawfulness, certify regulatory compliance, certify HIPAA compliance, certify medical correctness, certify clinical appropriateness, certify utilization-management sufficiency, or replace institutional approval.

It only hardens the stakeholder-facing lexicon around Fork structural-readiness artifacts.
