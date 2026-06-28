# Fork Boundary Mapping Evidence Index v0.1

## Status

`BOUNDARY_MAPPING_EVIDENCE_INDEX_RECORDED`

## Purpose

This index provides a navigation layer for the Fork Boundary Mapping Evidence surface.

It identifies the evidence objects, schema, checker, tests, execution receipt, and public handoff materials that together show how Fork records the distinction between preserved evidence and non-inherited authority.

The purpose is not to argue for Fork by assertion.

The purpose is to let the evidence surface be inspected and recomputed.

## Evidence premise

A claim is based upon evidence.

Fork therefore presents bounded evidence records first:

- what source claim existed,
- what evidence was preserved,
- what boundary was crossed,
- what downstream assumption appeared,
- what authority was attempted to be inherited,
- what Fork preserves,
- what Fork does not inherit,
- what remains unresolved.

## Evidence chain

The current boundary mapping evidence chain is:

1. Boundary mapping evidence records are defined.
2. Example records are provided across three governance boundary patterns.
3. A structural checker validates the records.
4. Tests exercise positive and negative checker behavior.
5. A local execution receipt preserves the observed checker and test result.

In short:

`boundary mapping evidence -> structural checker -> executed pass -> preserved receipt`

## Primary packet

| Path | Role |
|---|---|
| `docs/FORK_BOUNDARY_MAPPING_EVIDENCE_PACKET_v0_1.md` | Explains the boundary mapping evidence packet and its bounded purpose |
| `reports/FORK_BOUNDARY_MAPPING_EVIDENCE_STATUS_v0_1.md` | Records packet status, included mappings, result tokens, limitations, and non-claims |

## Schema

| Path | Role |
|---|---|
| `schemas/fork_boundary_mapping_evidence_v0_1.schema.json` | Defines the structured shape of Fork boundary mapping evidence records |

## Evidence records

| Path | Boundary pattern |
|---|---|
| `examples/fork_boundary_mapping_evidence/benchmark_to_deployment_safety_v0_1.json` | Benchmark result consumed as deployment safety |
| `examples/fork_boundary_mapping_evidence/vendor_report_to_compliance_status_v0_1.json` | Vendor report consumed as compliance status |
| `examples/fork_boundary_mapping_evidence/agent_tool_permission_to_action_authority_v0_1.json` | Agent tool permission consumed as action authority |

## Checker surface

| Path | Role |
|---|---|
| `tools/check_boundary_mapping_evidence.py` | Validates boundary mapping evidence records |
| `tests/test_boundary_mapping_evidence_v0_1.py` | Tests positive and negative checker behavior |
| `reports/FORK_BOUNDARY_MAPPING_EVIDENCE_CHECKER_STATUS_v0_1.md` | Records checker status, scope, failure conditions, and non-claims |

## Execution receipt

| Path | Role |
|---|---|
| `reports/FORK_BOUNDARY_MAPPING_EVIDENCE_CHECKER_EXECUTION_RECEIPT_v0_1.json` | Preserves local checker and test execution result as structured receipt |
| `reports/FORK_BOUNDARY_MAPPING_EVIDENCE_CHECKER_EXECUTION_REPORT_v0_1.md` | Human-readable execution report corresponding to the JSON receipt |

## Recompute commands

From the repository root, run:

~~~text
python .\tools\check_boundary_mapping_evidence.py
~~~

Expected checker result for the current v0.1 examples:

`STRUCTURAL_PASS`

Run the unit tests:

~~~text
python -m unittest discover -s tests -p "test_boundary_mapping_evidence_v0_1.py"
~~~

Expected test result:

`OK`

Validate the execution receipt JSON:

~~~text
python -m json.tool .\reports\FORK_BOUNDARY_MAPPING_EVIDENCE_CHECKER_EXECUTION_RECEIPT_v0_1.json
~~~

## Current record count

The current v0.1 boundary mapping evidence set contains three records:

- `agent_tool_permission_to_action_authority_v0_1`
- `benchmark_to_deployment_safety_v0_1`
- `vendor_report_to_compliance_status_v0_1`

## Result tokens used

The current evidence records use bounded result tokens including:

- `BOUNDARY_MAPPING_RECORDED`
- `EVIDENCE_PRESERVED`
- `AUTHORITY_INHERITANCE_NOT_ESTABLISHED`
- `SCOPE_EXPANSION_RECORDED`
- `NON_CLAIM_PRESERVED`
- `UNRESOLVED_AUTHORITY_ASSUMPTION_RECORDED`

These are evidence-recording tokens. They are not legal, compliance, safety, approval, runtime, business, or truth determinations.

## What this evidence surface supports

This evidence surface supports the bounded observation that Fork can produce structurally checkable records distinguishing preserved evidence from non-inherited authority across exemplar governance boundary patterns.

## Non-claims

This index does not establish:

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

## Boundary

This index is a navigation artifact.

It does not alter the underlying evidence records, checker behavior, schema, tests, execution receipt, or result determinations.
