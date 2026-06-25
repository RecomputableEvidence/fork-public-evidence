# Transition Localization and Independent Establishment v0.1

## 1. Motivation

Transition Integrity assumes that a transition exists. It asks whether the change in validity status between two contexts is admissible under a given specification.

In practice, many purported “transitions” are not transitions at all. They are relationships with no independently localizable establishment event: no issuance, no execution, no delegation, no procedure that can be pointed to as the moment where validity was established in the new context.

This document introduces a stricter primitive:

> **Independent Establishment** — a property is not valid in a context unless its establishment in that context can be independently localized or independently reconstructed.

Transition Localization is the discipline of asking whether such an establishment event exists at all before trying to evaluate its integrity.

## 2. Core Definitions

### 2.1 Establishment Event

An **establishment event** is the act, process, or mechanism by which a property becomes valid for an artifact in a particular context and scope.

Examples:

- Issuance of a certification under a defined procedure.
- Execution of a benchmark pipeline that binds a performance claim to a model.
- Signing of a delegation that transfers a bounded authority.

An establishment event has:

- An identity (it can be referred to).
- A boundary (it begins and ends).
- A mechanism type (how it operates).
- A scope (where its conclusions apply).

### 2.2 Transition Localization

**Transition Localization** asks:

> Can independent observers identify the same establishment event as the source of a claimed property in this context?

Localization requires that:

- The establishment event is represented as an object or record, or
- The event can be reconstructed from available evidence and procedure such that independent parties arrive at the same establishment.

If no such event can be identified or reconstructed, then there is no localized transition to govern. The claimed propagation is carried entirely by relationships, not by a transition mechanism.

### 2.3 Independent Establishment

**Independent Establishment** is a localized establishment event that does not rely on hidden trust or undocumented relationships between parties.

A property \( P \) holds for artifact \( A \) in context \( C \) only if there exists an establishment event \( E \) such that:

- \( E \) is localizable (it has an identity and boundary).
- \( E \) is tied to \( A \) and \( C \) via a known mechanism type.
- \( E \) is either directly observable or reconstructable by parties who do not share implicit trust in each other.

If no such event exists, the system must treat the property as **not established** in context \( C \), regardless of how strong the relationships around \( A \) may appear.

## 3. The Localization Test

Before applying Transition Integrity to any claimed propagation of validity, we apply the **Localization Test**:

1. **Can the transition be localized?**

   - Is there an identifiable establishment event \( E \) that purports to create or re‑establish the property in the destination context?
   - Can independent observers agree on what \( E \) is?

2. **If yes: evaluate Transition Integrity over that transition.**

   - Given \( E \), evaluate whether the transformation, mechanism, evidence, and scope satisfy the rules for a valid transition.
   - This is where Transition Integrity and Validity Commits apply.

3. **If no: relationship ≠ transfer.**

   - The system may observe relationships (same organization, shared infrastructure, dependences, authorship), but these do not count as a transfer mechanism.
   - In this case, what has been discovered is not an invalid transition but the absence of a transition.

The localization test prevents governance logic from silently treating adjacency as evidence of transfer.

## 4. Classes of Establishment

Not all establishment events look the same. For inspection and tooling, it is useful to distinguish four classes of establishment claims.

### 4.1 Class A — Localizable Establishment

The establishment event is represented by a concrete, addressable object.

Examples:

- A signed certification record with a procedure ID and validity window.
- A BDR (Boundary Delta Record) backed deployment approval artifact.
- A cryptographically signed TRACE or TRUST record emitted by a governance tool.

Characteristics:

- There is an explicit record that can be fetched, hashed, and attached.
- Two observers can reliably refer to the same object when they talk about “the establishment event.”

### 4.2 Class B — Reconstructable Establishment

The establishment event is not kept as a stand‑alone object, but it can be independently reconstructed from evidence and procedure.

Examples:

- A benchmark run that can be recomputed from versioned code, datasets, and configuration.
- A static analysis pass that can be re‑invoked on the same revision.

This is where **Recomputable Evidence** naturally lives:

- The property is not justified because an authority said so.
- It is justified because a procedure can be recomputed and the result independently verified.

### 4.3 Class C — Interpretive Establishment

The establishment event depends on human judgment, deliberation, or interpretation.

Examples:

- A legal opinion issued by a counsel under a documented review process.
- A scientific argument published and peer reviewed.
- A safety board decision after a structured incident review.

Characteristics:

- The establishment can be localized (there is a decision, opinion, or report).
- Parts of the mechanism are not fully mechanizable, but they can still be documented and bounded.

### 4.4 Class D — Non‑localizable Assumption

No identifiable establishment event can be found. The property appears only through adjacency or inherited reputation.

Examples:

- “Trusted product” because it comes from a “trusted company,” with no issuance, test, or delegated authority recorded.
- “Safe model” because it belongs to a “safety‑focused team,” with no localized safety evaluation.

Characteristics:

- Inspection reveals relationships, not transitions.
- There is no object or reconstructable procedure that can be pointed to as the moment of establishment.

Under this framework:

- Classes A, B, and (with explicit caveats) C qualify as **independent establishment**.
- Class D does not. It is the category where Transition Localization should halt with a finding: *no localized transition exists*.

## 5. Relationship to Existing Concepts

Transition Localization and Independent Establishment sit beneath the other primitives in this repository.

- **Preservation Without Inheritance** remains the default rule: preserving an artifact or pointing to it does not transfer properties.
- **Independent Establishment** answers the prior question: did this property ever become valid here at all?
- **Recomputable Evidence** occupies Class B: it provides a mechanism to reconstruct establishment events without inheriting social authority.
- **Transition Integrity** applies only after localization: given an independently established transition, evaluate whether it is a valid transition for the property in question.
- **Bounded Propagation** studies how valid transitions compose across systems and over time, under explicit scope and conservation constraints.

The resulting order of operations is:

1. Ask whether an establishment event exists and can be independently localized or reconstructed.
2. If and only if it does, apply Transition Integrity to the transition.
3. If it does not, treat the claimed propagation as unsupported by a transition and governed by the default: relationships do not authorize transfer.

## 6. Consequences for Inspection

For any claimed property in a context, an inspection system can now ask:

- Is there a referenced establishment event?
- Can that event be localized (Class A), reconstructed (Class B), or at least documented as an interpretive decision (Class C)?
- If yes, proceed to evaluate transition integrity using the relevant specification.
- If no, record that **no independent establishment exists** and that any apparent validity is carried only by relationships.

This turns “absence of a transition” into an explicit object of governance, rather than a silent gap.
