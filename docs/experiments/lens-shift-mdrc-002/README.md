# LS-MDRC-002 — Measurement-System, Branch-Governance, and Construct-Separation Calibration

**Research object:** `LS-MDRC-002`  
**Status:** `CONSTRUCTED_AND_STRUCTURALLY_CLOSED`  
**Bound repository commit:** `2dab684fc904f43ca0d35d1c1bbc500e92156ec4`  
**Repository URL:** `https://github.com/RecomputableEvidence/fork-public-evidence/`  
**Construction timestamp:** `2026-09-21T18:00:00Z` (nominal)  
**Specification source:** Prompt document LS-MDRC-002 §1–§24, provided by requester  

---

## What this object is

LS-MDRC-002 is an external implementation, examination, and recomputation path for the **LS-MDRM** (Lens Shift Measurement and Diagnostic Rubric Model) candidate. It tests whether a frozen measurement instrument can discriminate recursive Lens Shift behavior under bounded conditions.

This object does **not** validate, prove, certify, endorse, or establish the scientific correctness of the Lens Shift framework. It tests whether the proposed instrument can fail visibly.

---

## Directory layout

```
docs/experiments/lens-shift-mdrc-002/
    README.md                             ← this file
    SPECIFICATION/                        ← normative source binding records
    schemas/                              ← machine-readable JSON Schemas
    fixtures/
        development/                      ← open development fixtures
        calibration/                      ← calibration fixtures (open)
        holdout/                          ← sealed holdout manifest
        negative-controls/                ← non-Lens-Shift and degraded fixtures
        sentinels/                        ← edge-case sentinel fixtures
    runs/                                 ← trajectory execution records
    receipts/
        construction/                     ← construction receipt
        testing/                          ← test receipt
        recomputation/                    ← recomputation receipt
    reports/                              ← final bounded dispositions
    SHA256SUMS                            ← package hash manifest
```

---

## Location selection rationale

The repository uses `docs/experiments/<experiment-name>/` for experimental objects. The existing CSH experiment is at `docs/experiments/cross-system-claim-handoff-v0.1/`. LS-MDRC-002 is created at `docs/experiments/lens-shift-mdrc-002/` following the same convention. This path does not conflict with any existing experiment and does not modify any existing Fork research object.

---

## Non-claims

- This object does not establish that Lens Shift is beneficial, optimal, scalable, or scientifically validated.
- This object does not constitute independent scientific validation of any LS-MDRM result.
- Recomputation by a second context does not constitute independent validation; it is mechanical re-traversal.
- Repository adjacency to the CSH experiment does not create derivation, equivalence, endorsement, or standing inheritance.
- Construction does not confer scientific authority.

---

## Source separation

The CSH experiment artifacts under `docs/experiments/cross-system-claim-handoff-v0.1/` are **not modified** by this object. LS-MDRC-002 references them as a naturalistic calibration fixture only.
