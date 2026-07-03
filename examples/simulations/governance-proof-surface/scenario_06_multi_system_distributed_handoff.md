# Scenario 06 — Multi-System Distributed Handoff

## Purpose

This scenario turns the Scenario 06 scaffold into an artifact-backed structural simulation of a distributed AI-assisted handoff across independently accountable systems.

The scenario models a three-system chain:

1. **System A — Intake Analyzer** creates a bounded, source-backed triage summary.
2. **System B — Risk Summarizer** narrows that summary into a routing recommendation.
3. **System C — Approval Router** incorrectly treats the routed summary as if approval authority crossed the boundary.

The failure mode is not that any individual system is necessarily defective inside its own boundary. The failure is that the downstream system treats a narrowed artifact as carrying a new authority-bearing claim that no prior record established.

## Structural claim

Fork records the transition state between independently accountable systems:

- what crossed,
- what was narrowed,
- what did not cross,
- what remained unresolved,
- what required separate authority or evidence,
- and where downstream reliance exceeded the preserved record.

## Artifact family

Scenario 06 is backed by:

- `scenario_06_boundary_delta_record.json`
- `scenario_06_claim_boundary_contract.json`
- `scenario_06_claim_consumption_event.json`
- `scenario_06_system_mapping_receipt.json`
- `scenario_06_distributed_authority_failure_event.json`
- `scenario_06_transition_graph.md`
- `scenario_06_non_claims_panel.md`

## Expected result

The dedicated Scenario 06 checker should report that the multi-system handoff is structurally inspectable and that the distributed authority inheritance attempt is recorded as unsupported.

## Non-authority boundary

Fork does not approve the case, certify the downstream decision, authorize the routed action, score the risk, determine compliance, or judge correctness. Fork preserves a bounded handoff record showing which claims crossed, which claims did not cross, and which downstream inference required separate evidence or authority.
