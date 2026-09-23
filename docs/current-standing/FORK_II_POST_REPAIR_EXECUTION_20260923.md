# Fork II KERNEL-002 v0.1 — successor-only repair and post-repair execution — 2026-09-23

Ordered gate 4 is complete as bounded execution evidence. A separately named successor implementation was repaired only after FII-23–FII-26 and the 13-control population had been frozen. The predecessor was not modified.

The preserved execution reports `22/22` for the predecessor fixture baseline, `26/26` for FII-01–FII-26, `13/13` for the frozen controls, and `39/39` for the combined population. All 12 predecessor mutants remain detected, and all eight targeted successor fault reintroductions are detected at their predesignated witnesses.

The repair does not redefine CANON-v1. It separately enforces profile immutability, dependency digest syntax and exact supplied-record-byte binding, explicit fixed-time evaluation, and UNKNOWN-end uncertainty.

An initial harness-construction attempt is preserved as a negative result. The subsequent successful attempt changed only the test/receipt wrapper, not the successor implementation or frozen inputs.

This coordinate is **post-repair execution evidence, not successor release admission**. No independent-implementation, independent-human, institutional, or other stronger recomputation class is inferred from the execution itself.

The next evidence-bearing gate is a separate recomputation of the repaired package before any successor release admission.
