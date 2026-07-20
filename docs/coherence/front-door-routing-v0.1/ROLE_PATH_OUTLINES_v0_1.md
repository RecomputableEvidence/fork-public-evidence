# Visitor Role-Path Outlines v0.1

Status: `DRAFT_COHERENCE_OUTLINE`

These outlines route visitors to existing Fork surfaces. They do not create new authority, contribution admission, review standing, experiment permission, or publication effect.

## Shared opening boundary

Every route begins with the same distinction:

> Fork preserves bounded evidence context for later inspection. Structural verification does not become truth, approval, authorization, compliance, legal sufficiency, safety, production readiness, or inherited authority.

Every visitor should be able to locate:

- the exact commit or head being inspected;
- the smallest artifact supporting the relevant claim;
- the applicable verifier or declared absence of one;
- explicit non-claims;
- unresolved, failed, blocked, or not-checked conditions.

---

## 1. Reviewer path

### Visitor goal

Inspect Fork's current public proof surface and produce a bounded review tied to an exact checkout.

### First click

- `docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md`

### Supporting route

1. Read `docs/CURRENT_PROOF_SURFACE_v0_1.md`.
2. Read `docs/REVIEWER_START_HERE_v0_1.md`.
3. Record the exact commit, operating system, shell, Python version, Git version, and PowerShell availability.
4. Run:

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1 -Json
   ```

5. Inspect the selected example fixture:
   `docs/review/boundary-pressure/fixtures/valid/BPR_RR_VALID_001_receipt_preserved_as_structural_v0_1.json`.
6. Read `docs/review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md` before interpreting results.
7. Record failures, access limitations, overread risks, and unresolved questions without silently repairing them.

### Concrete next action

File an exact-head review observation that states:

- what was executed or inspected;
- what result was observed;
- what was not checked;
- what the result does not establish;
- any discrepancy or ambiguity.

### Stop conditions

Stop and classify rather than infer when:

- the checkout is not the declared head;
- a required source or artifact cannot be accessed;
- a command cannot run in the available environment;
- the result differs from the declared expectation;
- the review question requires authority outside Fork's evidence boundary.

---

## 2. Contributor path

### Visitor goal

Propose a bounded correction, adversarial fixture, documentation improvement, or checker change without widening claims or silently changing standing.

### First click

- `docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md`, especially the optional adversarial interaction section.

### Supporting route

1. Reproduce the current behavior from an exact base before editing.
2. Identify the smallest affected artifact or checker.
3. State whether the proposed work is:
   - editorial or routing;
   - schema or contract;
   - implementation;
   - canonical fixture or registry;
   - experiment or receipt;
   - historical correction;
   - admission or publication.
4. Declare files in scope and files explicitly excluded.
5. Preserve the original failure, negative evidence, or disputed state when the proposal corrects it.
6. Add a negative or adversarial test when changing checker behavior.
7. Run the applicable verifier and record the exact head.
8. Open the pull request as a draft.

### Required draft-PR fields

- change classification;
- claim;
- scope and exclusions;
- exact base and candidate head;
- validation performed;
- failures and residuals;
- non-claims;
- admission or publication effect;
- provider-call, readiness, and experiment-execution effects where applicable.

### Concrete next action

Open one draft pull request containing one bounded change class and one reviewable claim. Do not combine front-door editing, checker semantics, historical correction, and admission into one undifferentiated change.

### Stop conditions

Stop and separate the work when:

- an editorial change becomes normative;
- a checker repair would erase the failing specimen;
- a new fixture changes a preregistered experiment;
- a change would imply execution or retry authority;
- the exact base cannot be established;
- the proposal requires an admission act not present in the branch.

---

## 3. Governance or buyer-reader path

### Visitor goal

Determine whether Fork's evidence-boundary approach is relevant to a governance, legal, risk, audit, compliance, security, or procurement problem without treating the repository as a certification or deployment approval.

### First click

- `docs/commercial/BUYER_QUICK_START_GC_CISO_RISK_v0_1.md`

### Supporting route

1. Read the root README's plain-language explanation and non-claims.
2. Read the buyer quick start.
3. Inspect `docs/CURRENT_PROOF_SURFACE_v0_1.md` to distinguish machine-checked, protocol-only, observation, and future-work surfaces.
4. Run or commission the public verifier rather than relying only on narrative materials.
5. Read `docs/architecture/FORK_MATURITY_AND_TERMINOLOGY_BOUNDARY_v0_1.md`.
6. Identify one bounded workflow where evidence context is presently lost or overread.
7. Complete any pilot-discovery worksheet only as discovery evidence, not approval.

### Concrete next action

Write a bounded applicability question in this form:

> In workflow X, can Fork preserve evidence fields Y and Z so reviewer role A can later inspect condition B, while explicitly not claiming C?

### Stop conditions

Stop before treating Fork as:

- a runtime enforcement or approval layer;
- a compliance or legal-admissibility oracle;
- a replacement for GRC, SIEM, audit, policy, or institutional controls;
- proof that a client workflow is suitable for deployment;
- procurement, risk-acceptance, or production authorization.

---

## 4. Researcher path

### Visitor goal

Evaluate Fork's hypotheses, architecture, failure modes, experiments, and non-equivalences at the correct maturity level.

### First click

- `docs/research/ACCOUNTABLE_HANDOFF_INTEROPERABILITY_POSITION_PAPER_v0_1.md`

### Supporting route

1. Read `docs/CURRENT_PROOF_SURFACE_v0_1.md` and note the claims ladder.
2. Read the position paper as a motivated hypothesis, not a proven general theory.
3. Inspect:
   - `docs/modular-surface/FORK_MODULAR_SURFACE_v0_1.md`;
   - `docs/modular-surface/FORK_SURFACE_INTERACTION_CONTRACT_v0_1.md`;
   - `docs/modular-surface/FORK_MODULAR_SURFACE_CROSSWALK_v0_1.md`.
4. Distinguish protocol surfaces from completed experiments and exterior observations.
5. Inspect adversarial and negative-evidence records under:
   - `docs/review/boundary-pressure/`;
   - `docs/reconstruction/adversarial/`;
   - `docs/exterior-observations/`.
6. Locate the machine-readable state relevant to the experiment before citing narrative status.
7. Propose a falsifying or discriminating test rather than an endorsement statement.

### Concrete next action

Submit a research question that identifies:

- the hypothesis or boundary under pressure;
- the observable event;
- the expected preserved, narrowed, expanded, unresolved, or mixed outcome;
- the evidence required;
- the stopping rule;
- the explicit non-claims.

### Stop conditions

Stop and preserve non-equivalence when:

- two systems use similar vocabulary with different semantics;
- evidence continuity is being treated as authority continuity;
- a model self-report is being treated as verified internal mechanism;
- an unresolved observation is being resolved through assumption;
- an experiment's prerequisites or exact-head bindings are incomplete.

---

## Path-design acceptance rule

Each final role page must end with one action that a visitor can perform without navigating an undifferentiated documentation directory. The action must preserve exact-head, evidence-scope, non-claim, and authority boundaries.