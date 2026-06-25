# Conceptual Stack v0.1

This repository uses a layered conceptual stack. Each layer assumes the ones beneath it.

1. **Independent Establishment / Transition Localization**

   - Question: Did this property ever become valid here at all?
   - Primitive: Establishment events that can be independently localized or reconstructed.
   - Default: If no establishment event can be found, relationships do not authorize transfer.

2. **Recomputable Evidence**

   - Question: Can the establishment event be reconstructed from procedure and evidence?
   - Primitive: Evidence and processes that can be re‑run by independent parties.
   - Role: Turns social authority (“X says so”) into procedural establishment (“the procedure recomputes”).

3. **Preservation Without Inheritance**

   - Question: What happens when artifacts are preserved or referenced?
   - Rule: Preservation does not imply inheritance. Properties do not move just because objects are copied or linked.

4. **Transition Integrity**

   - Question: Given a localized establishment event, is the transition itself valid?
   - Primitive: Validity commits that record input property, context, transformation, mechanism, output property, scope, evidence, and invalidation conditions.
   - Role: Governs transitions rather than static states.

5. **Bounded Propagation**

   - Question: How do valid transitions compose across systems and over time?
   - Primitive: Compositional rules that respect scope, temporal bounds, and conservation of meaning.
   - Role: Prevents semantic inflation as properties move through complex systems.

A typical inspection sequence is:

1. Attempt to localize an establishment event for a claimed property (Layer 1).
2. If it is reconstructable, use Recomputable Evidence (Layer 2).
3. Apply Preservation Without Inheritance as the default (Layer 3).
4. If a transition exists, evaluate Transition Integrity (Layer 4).
5. If transitions compose, reason about Bounded Propagation (Layer 5).
