# Fork Boundary Mapping Evidence Public Handoff v0.1

## Status

`PUBLIC_HANDOFF_RECORDED`

## Purpose

This handoff provides a public-facing path for inspecting the Fork Boundary Mapping Evidence surface.

It is intended for readers who want to understand the evidence without first accepting Fork's category claim.

The handoff directs readers to the records, checker, tests, and execution receipt that show how Fork distinguishes preserved evidence from non-inherited authority.

## Public posture

Fork does not ask the reader to trust inherited meaning.

Fork asks the reader to inspect whether evidence, authority, scope, and non-claims remain distinguishable after a boundary crossing.

The current evidence surface is built around a simple premise:

A claim is based upon evidence.

Therefore this handoff points first to evidence objects, then to recomputation.

## What to inspect first

Start with the index:

`docs/FORK_BOUNDARY_MAPPING_EVIDENCE_INDEX_v0_1.md`

Then inspect the evidence packet:

`docs/FORK_BOUNDARY_MAPPING_EVIDENCE_PACKET_v0_1.md`

The packet explains the object model and the included mapping records.

## What the evidence records show

The current examples show three common boundary patterns:

| Pattern | Native evidence | Downstream assumption | Fork result |
|---|---|---|---|
| Benchmark result to deployment safety | Benchmark execution evidence | Performance treated as deployment safety | Safety inheritance not established |
| Vendor report to compliance status | Vendor review evidence | Report treated as compliance status | Compliance inheritance not established |
| Agent tool permission to action authority | Tool access evidence | Permission treated as action authority | Action authority inheritance not established |

These examples do not claim that the downstream assumption is always wrong.

They record that the downstream authority is not established merely by preserving the upstream evidence.

## How to recompute the structural result

From the repository root:

~~~text
python .\tools\check_boundary_mapping_evidence.py
~~~

Expected result:

`STRUCTURAL_PASS`

The checker validates that the records preserve:

- source claims,
- evidence references,
- boundary crossings,
- downstream assumptions,
- attempted inherited authority,
- non-claims,
- unresolved questions,
- bounded result tokens,
- required non-inheritance results.

Run the tests:

~~~text
python -m unittest discover -s tests -p "test_boundary_mapping_evidence_v0_1.py"
~~~

Expected result:

`OK`

## Execution receipt

The local execution result is preserved in:

`reports/FORK_BOUNDARY_MAPPING_EVIDENCE_CHECKER_EXECUTION_RECEIPT_v0_1.json`

A readable report is preserved in:

`reports/FORK_BOUNDARY_MAPPING_EVIDENCE_CHECKER_EXECUTION_REPORT_v0_1.md`

The receipt records local structural checker execution and test execution.

It does not bind the GitHub CI log itself.

## What a reader may conclude

A reader may inspect that Fork has an executable evidence surface for recording and checking the distinction between:

- evidence preservation, and
- authority inheritance.

The current evidence surface supports the bounded determination:

`STRUCTURAL_PASS`

for the included v0.1 boundary mapping examples.

## What a reader should not conclude

A reader should not conclude that Fork has established:

- legal sufficiency,
- regulatory compliance,
- audit acceptance,
- deployment safety,
- model truth,
- benchmark validity,
- vendor trustworthiness,
- agent authorization,
- runtime enforcement,
- institutional approval,
- external endorsement,
- business fitness,
- claim inheritance,
- independent external validation.

## External use

An external reviewer, evaluator, or domain expert may use this handoff to:

1. inspect the evidence records,
2. run the checker,
3. run the tests,
4. compare their observed results to the receipt,
5. bring a domain-native object for future boundary mapping.

No endorsement is implied by inspection.

No adoption is implied by recomputation.

No external authority transfers into Fork merely because the evidence was reviewed.

## Boundary

This handoff is an evidence-navigation artifact only.

It does not create new claims beyond the existence, location, and intended inspection path of the current boundary mapping evidence surface.
