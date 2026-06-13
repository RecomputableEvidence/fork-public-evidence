# Reading Guide: From Reconstructive Fidelity to Recomputable Evidence

## Purpose

This reading guide connects Fork's reconstructive-fidelity doctrine to its executable evidence posture.

Read this after the README and before the white paper, v0.7 release notes, or verification scripts. Its purpose is to explain how the abstract governance problem becomes a bounded, test-backed evidence mechanism without expanding Fork's claims beyond what the artifacts establish.

## Suggested Reading Order

1. **README** — what Fork establishes and does not establish.
2. **This reading guide** — how reconstructive fidelity maps to recomputable evidence.
3. **White Paper: _Reconstructive Fidelity in the Age of AI_** — the broader governance and evidentiary doctrine.
4. **v0.7 Release Notes** — the narrow recomputability receipt-binding milestone.
5. **Local Verification Script** — run `technical-disclosure/verify_public_disclosure.py` to inspect the public disclosure verification surface.
6. **Schemas, examples, tests, and tools** — review the executable evidence constraints in `schemas/`, `examples/`, `tests/`, and `tools/`.

## From Reconstructive Fidelity to Recomputable Evidence

AI governance cannot depend only on an institution's present memory of what happened.

Models change. Prompts change. Policies change. Personnel change. Vendors, interfaces, workflows, and authority structures all shift over time. When an AI-assisted decision is later questioned, the central issue is not simply whether the institution can explain itself. The issue is whether a later reviewer can reconstruct the relevant evidence without relying on the institution's current interpretation.

That is the purpose of reconstructive fidelity.

Reconstructive fidelity asks whether a past workflow event can be recovered with enough structure to distinguish: content — what was said or produced; attribution — what actor, account, system, or source is associated with it; mechanical status — what passed, failed, or was not checked; inference boundaries — what the record is not allowed to prove; resolution authority — who is permitted to resolve ambiguity; and resolution history — how unresolved questions, overrides, or corrections changed over time. It does not claim that the underlying decision was correct. It asks whether the evidentiary conditions around that decision were preserved clearly enough for later review.

Fork translates that doctrine into an executable evidence posture.

Instead of treating verification as a single broad PASS/FAIL claim, Fork separates what was observed, what was preserved, what was checked, what failed, what was not checked, and what the record is not allowed to prove.

This matters because preserved evidence can be overread.

A record may be intact without being true.  
A workflow may be reconstructable without being trustworthy.  
A hash may verify without proving strong recomputation.  
A preserved determination may remain internally consistent without retaining present-state validity.  
A PASS result may indicate a bounded check, not total validation.

Fork's recomputability enforcement prevents one specific escalation path: NON_RECOMPUTABLE evidence cannot satisfy gates requiring STRONG_RECOMPUTATION. The v0.7 receipt-binding release does not add new recomputability classes or broaden that enforcement. It binds the existing recomputability enforcement into auditable PASS/FAIL receipt evidence: each receipt records the artifact recomputability class, gate required class, gate result, reason code, and claim boundary behind the decision.

The broader claim is intentionally limited.

Fork does not establish source truth, decision correctness, legal sufficiency, policy compliance, or institutional authority. This is a conceptual summary of the boundary; the README contains the itemized non-claims list, including source truth/completeness, signer identity/non-repudiation, legal admissibility, compliance or ethical correctness, third-party verifier independence, live deployment, and production readiness. Fork preserves bounded evidence so later interpreters can assess reconstructive fidelity without letting one preserved property inherit claims it did not independently establish.

In that sense, Fork is not an AI governance dashboard. It is evidence infrastructure for AI-assisted workflows: a silent, read-only evidentiary layer between occurrence and later interpretation.