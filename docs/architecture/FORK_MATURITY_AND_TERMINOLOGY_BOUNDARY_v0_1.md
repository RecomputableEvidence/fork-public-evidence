# Fork Maturity and Terminology Boundary v0.1

## Purpose

This document defines Fork's current maturity posture and constrains high-risk terminology so reviewers, buyers, and integrators do not confuse evidence-boundary preservation with authority, approval, compliance, correctness, continuation validity, or production governance.

Its goal is to make the existing modular surfaces safer to read and reuse, not to broaden Fork's responsibilities or expand its claim surface.

## Current Maturity Statement

Fork is research-grade and pilot-discovery ready for bounded AI-assisted evidence-boundary workflows. It is not a general production governance platform, compliance engine, runtime control plane, approval system, or authority layer.

This sentence is the canonical maturity line and should be reused consistently in:

- README and top-level docs.
- Commercial and buyer-facing materials.
- Outreach and design-partner conversations.

## Approved Category Language

These phrases are considered safe shorthand when describing Fork's role:

- "bounded evidence-boundary infrastructure for AI-assisted workflows"
- "recomputable evidence and reliance-context preservation"
- "non-authoritative evidentiary layer around AI-assisted workflow handoffs"
- "out-of-band record of what was requested, produced, reviewed, relied upon, excluded, and explicitly not claimed"

When these phrases are used, they should be understood as:

- Fork preserves structure and scope of evidence and reliance.
- Fork supports structural verification of declared record structure and boundary consistency; it does not establish policy correctness, legal admissibility, or decision quality.

## Risky or Prohibited Language

The following terms are considered high-risk and should be avoided when describing Fork, because they can be misread as claims of correctness, compliance, or authority:

- "compliance engine"
- "proof of correctness"
- "governance system of record"
- "decision authority"
- "approval layer"
- "runtime control plane"
- "execution controller"
- "legal admissibility oracle"
- "production governance platform"

If these capabilities exist in a deployment, they belong to adjacent systems such as PAAK, ExecutionProof, AnchorStack, or institutional governance, not to Fork.

## Evidence vs Authority

Fork's core invariant is the separation between evidence and authority.

### Evidence: Fork's domain

Fork may preserve:

- What was requested, produced, reviewed, modified, excluded, and relied upon.
- Claim scope, explicit non-claims, unresolved items, and reliance transitions.
- Structural verification that the preserved record matches its declared boundary.

### Authority: adjacent domain

Adjacent systems and institutions determine:

- Who is allowed to permit, deny, escalate, or bind a decision.
- Under which policy, role, risk tier, and institutional mandate.

### Fork's position

Evidence may inform authority; it must not inherit authority.

A preserved, structurally verified record does not prove that a decision was correct, compliant, or permissible.

The fact that evidence exists does not grant or renew permission for continuation.

Rule: Treat Fork outputs as inputs to governance, not as governance decisions.

## Authority vs Authority Exercised vs Continuation Validity

Several reviewers have emphasized related but distinct concepts. Fork uses the following separation:

| Concept | Fork position |
|---|---|
| Authority | Adjacent systems and institutions decide who is allowed to act in general. Fork does not decide or certify this. |
| Authority exercised | Fork may record who relied on an artifact, when, under what stated role, policy, scope, and purpose. Fork does not judge whether that exercise was appropriate. |
| Continuation validity | Adjacent execution and governance systems decide whether an action should continue under live conditions. This is explicitly outside Fork's decision surface. |

In practice:

- Fork captures authority exercised as part of a reliance record.
- Fork records who accepted, modified, or relied upon an AI-assisted artifact only as declared reliance context, not as approval certification.
- Fork does not determine whether that authority was sufficient.
- Fork does not determine whether continuation was justified.
- Execution governance and continuation-validity logic belong to systems such as PAAK, ExecutionProof, AnchorStack, or institutional control frameworks.

## BDR / SMR / RGV Semantic Concordance

This section clarifies the intended meaning of key Fork artifacts so integrators do not project their own semantics onto them.

| Term | Fork-safe meaning | Not meant as |
|---|---|---|
| Evidence Boundary | Declared claim, non-claim, evidence, and verifier scope for a record or bundle. | Truth, correctness, compliance sufficiency, or approval. |
| Structural Verification | Verification of record shape and declared boundary consistency, such as hashes, manifests, and graph relations. | Factual or policy correctness; legal or risk verdict. |
| Reliance Record | What was relied upon, by whom, when, under what stated boundary and authority-exercised context. | Judgment that reliance was justified or authorized. |
| Boundary Delta Record (BDR) | Mechanical representation of what changed across a transition and which claims may or may not legitimately transfer under declared rules. | Legal, policy, or risk verdict on the consequences of that change. |
| System Mapping Receipt (SMR) | How another system maps or references Fork's claims, non-claims, and surfaces without inheriting Fork's authority or lending its own. | Endorsement, approval, or guarantee of compatibility. |
| Relational Graph Verifier (RGV) | Stateless relational graph verification of CBC/CCE bundles and their structural relations. | Policy oracle, truth oracle, risk engine, or correctness proof. |
| Continuation Validity | Adjacent question about whether operation should continue under current conditions. | A Fork decision or responsibility. |

These meanings should be preserved in all external and internal references.

When in doubt, prefer narrow, structural interpretations over semantic or policy-laden ones.

## Adjacent System Boundaries

Fork is designed to sit alongside, not replace, other governance and assurance systems.

### Runtime attestation systems

Examples include Verdict and Sigstore-anchored seals.

These systems may attest that an artifact or output existed in a given form at a given time with a given hash.

Fork may consume these attestations as part of its evidence boundary, but it does not inherit their claims.

### Execution governance and continuation-validity systems

Examples include PAAK, ExecutionProof, AnchorStack, and institutional execution controls.

These systems may decide whether an action is permitted, admissible, or supported under current conditions before or during execution.

They may emit governed-state exports, evidence records, ProofRecords, or validity statuses.

Fork may preserve these as inputs to the evidentiary record.

Fork does not perform these checks and does not adopt their authority.

### Institutional governance, legal, compliance, and audit functions

These functions interpret Fork's records and adjacent system outputs in light of policy, law, ethics, and risk appetite.

They remain responsible for judgments about correctness, compliance, admissibility, liability, and institutional decision authority.

### Fork's narrower contribution

Fork preserves enough bounded, recomputable context that later reviewers can see what was relied upon, what was excluded, and what claims remain supportable without treating Fork as the decision-maker.

Fork determines whether its evidence-boundary record structurally verifies; it communicates that state to adjacent systems that determine execution, admissibility, and continuation.

## Usage Guidance

When adding new docs, demo scripts, examples, or outreach materials:

- Reuse the Current Maturity Statement verbatim.
- Use Approved Category Language.
- Avoid Risky or Prohibited Language.
- When describing interactions with PAAK, ExecutionProof, AnchorStack, Verdict, Sigstore, or similar systems, explicitly state:
  - What Fork preserves.
  - What the adjacent system decides.
  - That Fork's outputs are inputs to those decisions, not substitutes.
- When designing schemas or fixtures:
  - Keep evidence vs authority explicit.
  - Keep authority vs authority exercised explicit.
  - Keep continuation validity outside Fork's decision surface unless a future version explicitly changes that boundary.
  - Use the BDR / SMR / RGV meanings from the concordance to avoid semantic drift.

Strongest rule: Treat Fork outputs as structured, recomputable inputs to governance and assurance processes, never as governance or assurance decisions themselves.

## Status Boundary

This document describes the project's status and terminology at v0.1 of the maturity and terminology boundary.

It does not:

- Expand Fork's claim surface.
- Introduce new proof surfaces or responsibilities.
- Change the semantics of existing contracts or schemas without explicit versioning.

Any future broadening of Fork's responsibilities, including movement toward production governance, would require:

- An explicit maturity statement update.
- New versioned doctrine and schema changes.
- Re-evaluation of how Fork is positioned alongside adjacent systems.

Until such a change is deliberate and explicit, this document should be considered normative for how Fork is described externally and internally.
