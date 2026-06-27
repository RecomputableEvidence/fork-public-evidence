Fork / ESAL Development Roadmap

The roadmap from here is not “add more features.” It is:

Preserve the ESAL v0.1 kernel.

Convert the release candidate into a stable release record.

Build outward through conformance, interoperability, and carefully scoped next‑semantics.

The current evidence record supports this posture:

Oracle distribution is stable at PASS: 4 / G: 3 / S: 2 / D: 1.

Permutation invariance is stable for the canonical baseline trace.

Earlier adversarial review has already identified the next real development surfaces: obligation dropping, authority narrowing/per‑hop scope, asymmetric G fingerprints, empty authority behavior, cycle/duplicate handling, validator naming, and fixture naming.

None of this is a production, compliance, legal sufficiency, or endorsement claim. It is about the reference‑oracle and its evidence.

Phase 0 — Freeze the checkpoint

Goal: Stop semantic churn around ESAL v0.1 RC6.

Actions:

Preserve esal-v0.1-rc6 as the current signed‑off release‑candidate anchor.

Do not share broadly yet.

Do not keep editing the release‑gate artifact unless a material defect appears.

Treat any additional changes as new branches / future release candidates, not silent edits to the checkpoint.

Output:ESAL v0.1 RC6 = preserved release‑record checkpoint.

This phase is essentially complete.

Phase 1 — Convert RC6 into a clean v0.1 release package

Goal: Turn the reviewed RC into a coherent package someone can pick up and understand without reading the entire review chain.

This should package:

ESAL_v0_1_RELEASE_GATE.md

CANONICALIZATION_SPEC_v0_1.md

STATE_SEMANTICS_v0_1.md

reports/latest-report.json

Permutation‑invariance result

Reviewer acknowledgment summary

Known limits / non‑claims

Reproduction commands

Recommended artifact:reports/ESAL_v0_1_RELEASE_RECORD.md

Purpose:“Here is what was reviewed, what commit was reviewed, what was executed, what passed, what was not claimed, and what remains out of scope.”

Only after this record exists should you consider a final tag such as esal-v0.1. Until then, RC6 is sufficient as the anchored candidate.

Phase 2 — Conformance Kit v0.1

Goal: Make ESAL v0.1 independently reproducible by someone else.

Deliverables (directory‑level):

reference/esal/

esal-tests/

reports/latest-report.json

tools/esal_verify.ps1

tools/Test-EsalPermutationInvariance.ps1

docs/ESAL_CONFORMANCE_KIT_v0_1.md

The conformance kit should define:

Required corpus.

Expected PASS/G/S/D distribution.

Expected fingerprints.

Expected canonical event hashes.

Expected exception classes.

Expected fingerprint availability (when None vs non‑None).

Allowed platform variance.

Forbidden dependencies (e.g., no network calls, no nondeterministic sources).

Correct claim:

ESAL v0.1 provides a reference conformance surface for independent replay comparison.

Incorrect claim:

ESAL v0.1 proves independent implementation convergence.

Convergence is not established until at least one independent implementation reproduces the outputs.

Phase 3 — Hygiene branch before new semantics

Goal: Remove avoidable reviewer friction without changing meaning.

This happens on a new branch, not by disturbing RC6.

Suggested branch:esal-v0.1-post-rc-hygiene

Low‑risk cleanup items:

Rename C-001-placeholder.jsonl to a meaningful fixture name.

Rename log7-event-reordering.jsonl if it is really an event‑ID conflict fixture.

Clarify identical‑duplicate behavior:

Canonicalization allows identical duplicates through.

Lineage validation later catches duplicate BDR IDs.

Rename or clearly document validate_events as shape‑only validation.

Document implicit cycle blocking via lineage / temporal ordering.

Consider replacing “governance‑valid replay” with “oracle‑governance‑valid replay” or “valid under ESAL v0.1 oracle rules.”

These are not conceptual advances; they reduce misread risk and make conformance work easier.

Phase 4 — Independent implementation convergence

Goal: Establish the next major evidence milestone.

This is where the project gets significantly stronger.

Path:

Freeze the conformance corpus.

Write explicit expected‑output vectors.

Ask an independent reviewer / second implementation to reproduce:

Canonical event hashes.

Reduced states.

Fingerprints.

Classifications.

Exception classes.

Record convergence or divergence.

Minimal second‑implementation options:

Clean‑room Python implementation.

Go implementation.

TypeScript implementation.

Strongest external value:

Two independent ESAL v0.1 implementations produce the same canonical event hashes, states, fingerprints, and classifications over the same corpus.

That is a meaningful, category‑forming claim. It’s worth treating as a distinct milestone.

Phase 5 — ESAL v0.2 design decisions

Goal: Decide which unresolved semantics become governed behavior in a v0.2.These are semantic design changes, not cosmetic tweaks. Each one changes what the oracle means.

Major v0.2 candidates:

Obligation dropping

v0.1 accumulates obligations by union.

It does not require child BDRs to restate inherited obligations.

v0.2 could introduce OBLIGATION_DROPPED, but that is a material semantic change.

Per‑hop authority narrowing

v0.1 authority is cumulative trace‑level authority.

It does not enforce child‑local authority isolation.

v0.2 could add active authority scope, but that requires an extended state model and clearer execution semantics.

Multi‑parent BDR merge

v0.1 is effectively single‑parent lineage.

v0.2 could define DAG merge semantics.

You’d need to settle authority/obligation merge algebra first.

Constraint / obligation discharge

v0.1 only accumulates.

Future versions need explicit termination / discharge events.

Boundary conflict classification

v0.1 silently selects the first resolvable boundary pair.

v0.2 could classify conflicting boundary candidates as structural errors instead.

Key principle:v0.2 should not be “more tests.” It should be a semantic design release with clearly stated differences from v0.1.

Phase 6 — BDR / ESAL / TIS integration

Goal: Connect the objects without collapsing their boundaries.

Stack sketch:

TIS — transition validity semantics.

BDR — boundary‑crossing record / inspectability surface.

ESAL — event‑state replay and fingerprint oracle.

SMR — system mapping / external integration record.

Core integration question:When a BDR is emitted, how does ESAL consume it as an event without inheriting external authority or policy guarantees from the BDR?

Deliverable:docs/BDR_ESAL_HANDOFF_CONTRACT_v0_1.md

This should define:

Which BDR fields become ESAL event fields.

What ESAL preserves verbatim.

What ESAL explicitly does not validate.

How non‑claims are preserved across the handoff.

How release‑gate evidence references BDRs without overstating what ESAL proves.

This matters because Fork’s category is not “one more checker.” It is coordination of claim boundaries across artifacts.

Phase 7 — Pilot-facing evidence story

Goal: Translate the technical layer into buyer‑understandable evidence without overclaiming.

Not a sales deck yet; more like:

docs/FORK_EVIDENCE_BOUNDARY_WALKTHROUGH_v0_1.md

Use one concrete workflow (for example, AI‑assisted vendor risk summary):

AI produces a summary.

Human reviews and annotates.

Claim boundary is recorded.

A BDR records a boundary transition.

ESAL replays events and fingerprints state.

A release gate states what verified and what was not claimed.

Buyer‑facing line:

Fork does not tell you the decision was right. It preserves what was claimed, what was not claimed, what evidence was referenced, and whether the recorded trace still verifies under the stated oracle rules.

That is the product bridge.

Practical 30 / 60 / 90 Roadmap

Next 30 days

Freeze RC6 (done).

Create ESAL_v0_1_RELEASE_RECORD.md.

Build ESAL_CONFORMANCE_KIT_v0_1.md.

Clean fixture names and validator naming on a hygiene branch.

Decide whether to tag final esal-v0.1 or hold RC6 until one independent reproducer exists.

30–60 days

Create independent implementation target.

Add expected‑output test vectors.

Formalize BDR_ESAL_HANDOFF_CONTRACT_v0_1.md.

Document current v0.1 limits as explicit v0.2 candidate semantics.

60–90 days

Attempt independent convergence.

Draft ESAL v0.2 design memo.

Decide obligation dropping / authority narrowing / multi‑parent merge semantics.

Build one end‑to‑end Fork evidence walkthrough for a real AI‑assisted workflow.

What we should not do next

Do not broadly share RC6 without a specific reason or context.

Do not keep creating RC tags for wording churn.

Do not add log10 or log11 until obligation and multi‑parent semantics are decided.

Do not claim independent convergence yet.

Do not turn ESAL into a policy‑enforcement engine.

Do not let PASS become a compliance or authorization signal.

The roadmap in one sentence

First, make ESAL v0.1 reproducible; second, make it independently convergent; third, connect it cleanly to BDR/TIS; fourth, only then translate it into buyer‑facing Fork evidence workflows.