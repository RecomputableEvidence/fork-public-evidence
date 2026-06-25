# BDR Localization Posture v0.1

## 1. Purpose

Boundary Delta Record (BDR) v0.1 is a mechanical boundary inspection artifact. It does not infer meaning, rank severity, adjudicate policy, or accept authored outcomes as authoritative.

This document clarifies how BDR relates to **Transition Localization and Independent Establishment**:

- BDR operates **after** a minimal localization check.
- If there is no independently localizable establishment event for a claimed property at a boundary, BDR should be able to emit a specific, inspectable limitation.
- The absence of a localized establishment event is **not** an implicit governance decision about truth, safety, legality, or compliance. It is simply the statement: *no transition to evaluate* under BDR v0.1.

## 2. Localization and BDR

BDR does not perform full Transition Localization. It does not search for establishment events, reconstruct procedures, or classify epistemic status.

Instead, BDR assumes that:

- If a boundary record declares that a property has become valid or remains valid in a new context, it may include a reference to an establishment event (for example, an issuance, approval, or recomputable procedure).
- If such an establishment reference is present, BDR can report that the record is compatible with localization.
- If no establishment reference is present, BDR can report that it has **no localized establishment to evaluate**.

In both cases, BDR remains strictly structural and non‑interpretive.

## 3. New Non‑Claim Limitation

BDR v0.1 introduces a standard non‑claim that downstream systems can inspect:

- `no_localized_establishment_for_transferred_property`

This limitation means:

- The record claims that a property is valid at or across a boundary.
- The record does **not** reference any establishment event or recomputable procedure that would localize or reconstruct how that property became valid in this context.
- BDR therefore does **not** evaluate a transition for that property. It only records that there is **no transition to evaluate**.

It does **not** mean:

- The content is false.
- The content is unsafe, illegal, or noncompliant.
- The content is blocked, rejected, or malicious.

Those are governance questions for other components.

## 4. Receipt Fields for Localization

To make localization posture visible, BDR receipts can include the following optional fields:

- `localization_status` (string)
  - `LOCALIZABLE_OR_RECONSTRUCTABLE_ESTABLISHMENT`
  - `NO_LOCALIZABLE_ESTABLISHMENT`

- `localization_findings` (array of strings)
  - Example codes:
    - `NO_ESTABLISHMENT_EVENT_REF`
    - `NON_LOCALIZABLE_ASSUMPTION_DETECTED`

### 4.1 Behavior

BDR remains non‑inferential:

- BDR does **not** infer whether an establishment event *should* exist for a property.
- BDR does **not** infer the type or class of an establishment event from natural language.

Instead:

- If the record includes an explicit `establishment_ref` (or equivalent field), BDR may set:
  - `localization_status: "LOCALIZABLE_OR_RECONSTRUCTABLE_ESTABLISHMENT"`
- If the record does **not** include such a reference, BDR may set:
  - `localization_status: "NO_LOCALIZABLE_ESTABLISHMENT"`
  - and add `NO_ESTABLISHMENT_EVENT_REF` to `localization_findings`.
  - and add `no_localized_establishment_for_transferred_property` to `limitations` or equivalent diagnostics.

BDR does not validate the correctness of the establishment event; it only reports whether one has been declared.

## 5. Interaction with INSPECTABLE / NOT_INSPECTABLE

The localization posture is orthogonal to the core BDR outcome:

- `INSPECTABLE` / `NOT_INSPECTABLE` remain structural outcomes under BDR v0.1 rules.
- `localization_status` and `localization_findings` qualify **what BDR saw** about establishment references; they do not add risk semantics.

Possible patterns:

- A record may be `INSPECTABLE` with `LOCALIZABLE_OR_RECONSTRUCTABLE_ESTABLISHMENT`.
- A record may be `NOT_INSPECTABLE` with `LOCALIZABLE_OR_RECONSTRUCTABLE_ESTABLISHMENT` (for example, due to other structural mismatches).
- A record may be `INSPECTABLE` with `NO_LOCALIZABLE_ESTABLISHMENT` if BDR is configured to treat localization as advisory only.
- A record may be `NOT_INSPECTABLE` with `NO_LOCALIZABLE_ESTABLISHMENT` if a stricter profile requires that boundary claims about certain properties must reference a localized establishment event.

BDR does not decide which combination is acceptable in a deployment. That is a policy decision for downstream governance systems.

## 6. Non‑Goals

This posture explicitly does **not**:

- Add requirement inference (e.g., guessing that a safety claim should have an establishment event).
- Introduce severity or risk scoring.
- Treat `NO_LOCALIZABLE_ESTABLISHMENT` as a safety or compliance verdict.

BDR remains a mechanical inspector of declared structure. Localization posture is merely another visible dimension of that structure.

## 7. Summary

- BDR v0.1 operates after a minimal localization check.
- If a boundary record references an establishment event, BDR can record that localization is possible.
- If not, BDR can record `no_localized_establishment_for_transferred_property` and `NO_LOCALIZABLE_ESTABLISHMENT` as inspectable limitations.
- This keeps BDR non‑interpretive while making “no transition to evaluate” an explicit, machine‑readable outcome.
