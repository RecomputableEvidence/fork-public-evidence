# Scenario 06 Transition Graph

## Distributed handoff chain

| Boundary | From | To | What crossed | What did not cross | Boundary effect |
|---|---|---|---|---|---|
| S06-B01 | System A Intake Analyzer | System B Risk Summarizer | Source-backed triage context | Approval authority, compliance determination, correctness certification | Preserved with narrowing |
| S06-B02 | System B Risk Summarizer | System C Approval Router | Narrowed routing summary | Approval authority, policy satisfaction, execution eligibility | Expansion attempt recorded |

## Interpretation

The graph is structurally inspectable because each transition records what crossed, what was narrowed, and what was withheld.

The failure appears at **S06-B02**. System C treats System B's narrowed routing summary as if it carried approval authority. That authority was not present in the upstream records and was explicitly withheld by the claim boundary contract.

## Fork boundary

Fork records the transition graph and unsupported inference. Fork does not approve, certify, score, authorize, determine compliance, or judge correctness.
