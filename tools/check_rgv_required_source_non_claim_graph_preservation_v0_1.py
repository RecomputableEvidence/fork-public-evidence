#!/usr/bin/env python3
"""
RGV Required Source Non-Claim Graph Preservation v0.1 checker.

This checker enforces downstream preservation of required source non-claims
when an RGV PASS result is consumed by CCE-like graph-composition nodes.

It does not verify source truth, factual basis, wholeness, completeness,
admissibility, lawfulness, legal sufficiency, compliance, safety, correctness,
institutional authority, runtime authorization, or source completeness.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

try:
    from check_rgv_result_required_source_non_claim_binding_v0_1 import REQUIRED_NON_CLAIM_IDS
except Exception:
    REQUIRED_NON_CLAIM_IDS = {
        "SOURCE_TRUTH_NOT_CLAIMED",
        "FACTUAL_BASIS_NOT_CONFIRMED",
        "WHOLENESS_NOT_ASSERTED",
        "COMPLETENESS_NOT_STATED",
        "ADMISSIBILITY_NOT_INFERRED",
        "LAWFULNESS_NOT_IMPLIED",
    }


CONSUMPTION_EDGE_TYPES = {
    "CLAIM_CONSUMPTION",
    "CLAIM_CONSUMPTION_EVENT",
    "CCE_CONSUMES",
    "RGV_PASS_CONSUMPTION",
}

PASS_ALIASES = {
    "PASS",
    "RGV_PASS",
    "STRUCTURAL_PASS",
}

FORBIDDEN_ASSERTION_FIELDS = {
    "source_truth_assertions": "SOURCE_TRUTH_ASSERTED",
    "factual_basis_confirmations": "FACTUAL_BASIS_CONFIRMED",
    "wholeness_assertions": "WHOLENESS_ASSERTED",
    "completeness_statements": "COMPLETENESS_STATED",
    "admissibility_inferences": "ADMISSIBILITY_INFERRED",
    "lawfulness_implications": "LAWFULNESS_IMPLIED",
}

HARD_SEMANTIC_FIELDS = {
    "reliance",
    "reliance_mode",
    "consumption_semantics",
    "treated_as",
    "treats_source_result_as",
    "asserted_meaning",
}

EXPANSION_SEMANTIC_FIELDS = {
    "inferred_claims",
    "derived_claims",
    "expanded_claims",
    "new_claim_categories",
}

PROHIBITED_SEMANTIC_VALUES = {
    "SOURCE_TRUTH",
    "SOURCE_TRUTH_ASSERTED",
    "SOURCE_TRUTH_CONFIRMED",
    "SOURCE_TRUTH_VERIFICATION",
    "VERIFIED_TRUTH",
    "FACTUAL_BASIS_CONFIRMED",
    "FACTUAL_CONFIRMATION",
    "FACTUALLY_CHECKED",
    "WHOLE_STORY",
    "WHOLENESS_ASSERTED",
    "COMPLETE_EVIDENCE",
    "COMPLETENESS_ASSERTION",
    "ADMISSIBLE",
    "ADMISSIBILITY_INFERRED",
    "ADMISSIBILITY_INFERENCE",
    "LAWFUL",
    "LAWFULNESS_IMPLIED",
    "LAWFULNESS_DETERMINATION",
}


def err(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}


def is_non_empty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def normalize_token(value: str) -> str:
    return value.strip().upper().replace("-", "_").replace(" ", "_")


def node_id(node: dict[str, Any]) -> str | None:
    for key in ("node_id", "id", "record_id"):
        value = node.get(key)
        if is_non_empty(value):
            return value
    return None


def result_status(node: dict[str, Any]) -> str | None:
    for key in ("result", "verification_result", "status"):
        value = node.get(key)
        if is_non_empty(value):
            return value.strip().upper()

    state = node.get("verification_state")
    if isinstance(state, dict):
        value = state.get("status")
        if is_non_empty(value):
            return value.strip().upper()

    return None


def is_rgv_result(node: dict[str, Any]) -> bool:
    return node.get("record_type") == "RGV_VERIFICATION_RESULT" or result_status(node) in {
        "PASS",
        "FAIL",
        "INDETERMINATE",
        "ERROR",
    }


def edge_source(edge: dict[str, Any]) -> str | None:
    for key in ("source_node_id", "source", "from", "from_node_id"):
        value = edge.get(key)
        if is_non_empty(value):
            return value
    return None


def edge_target(edge: dict[str, Any]) -> str | None:
    for key in ("target_node_id", "target", "to", "to_node_id"):
        value = edge.get(key)
        if is_non_empty(value):
            return value
    return None


def edge_type(edge: dict[str, Any]) -> str:
    value = edge.get("edge_type") or edge.get("type") or ""
    return normalize_token(value) if isinstance(value, str) else ""


def iter_values(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from iter_values(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_values(item)


def extract_non_claim_ids(record: dict[str, Any]) -> list[str]:
    ids: list[str] = []

    for field in (
        "preserved_non_claims",
        "required_source_non_claims",
        "result_non_claims",
        "non_claims",
    ):
        value = record.get(field)
        if isinstance(value, list):
            for item in value:
                if isinstance(item, str) and is_non_empty(item):
                    ids.append(item.strip())
                elif isinstance(item, dict):
                    non_claim_id = item.get("non_claim_id") or item.get("id")
                    if is_non_empty(non_claim_id):
                        ids.append(non_claim_id.strip())

    bundle = record.get("required_source_non_claim_bundle")
    if isinstance(bundle, dict):
        bundle_items = bundle.get("required_non_claims")
        if isinstance(bundle_items, list):
            for item in bundle_items:
                if isinstance(item, dict):
                    non_claim_id = item.get("non_claim_id") or item.get("id")
                    if is_non_empty(non_claim_id):
                        ids.append(non_claim_id.strip())

    return ids


def find_forbidden_assertion_fields(node: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    for field, code in FORBIDDEN_ASSERTION_FIELDS.items():
        if node.get(field):
            errors.append(
                err(
                    code,
                    f"{field} is prohibited on a downstream consumption node because RGV PASS cannot be consumed as that assertion category",
                )
            )

    return errors


def semantic_tokens_for_fields(node: dict[str, Any], fields: set[str]) -> set[str]:
    tokens: set[str] = set()

    for field in fields:
        if field not in node:
            continue
        for value in iter_values(node[field]):
            tokens.add(normalize_token(value))

    return tokens


def has_valid_new_claim_node(node: dict[str, Any], nodes_by_id: dict[str, dict[str, Any]]) -> bool:
    new_claim_node_id = node.get("new_claim_node_id")
    if not is_non_empty(new_claim_node_id):
        return False

    claim = nodes_by_id.get(new_claim_node_id)
    if not isinstance(claim, dict):
        return False

    authority = claim.get("authority_basis") or claim.get("authority_refs") or claim.get("authority")
    evidence = claim.get("evidence_basis") or claim.get("evidence_refs") or claim.get("evidence")

    authority_present = bool(authority) if not isinstance(authority, str) else bool(authority.strip())
    evidence_present = bool(evidence) if not isinstance(evidence, str) else bool(evidence.strip())

    return authority_present and evidence_present


def check_pass_consumption_preserves_non_claims(
    source: dict[str, Any],
    target: dict[str, Any],
    edge: dict[str, Any],
    nodes_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    target_ids = set(extract_non_claim_ids(target))
    missing = sorted(REQUIRED_NON_CLAIM_IDS - target_ids)
    for non_claim_id in missing:
        errors.append(
            err(
                "DROPPED_REQUIRED_SOURCE_NON_CLAIM",
                f"Downstream node {node_id(target)} consumes RGV PASS {node_id(source)} but does not preserve {non_claim_id}",
            )
        )

    errors.extend(find_forbidden_assertion_fields(target))

    hard_tokens = semantic_tokens_for_fields(target, HARD_SEMANTIC_FIELDS)
    prohibited_hard = sorted(hard_tokens & PROHIBITED_SEMANTIC_VALUES)
    for token in prohibited_hard:
        errors.append(
            err(
                "PROHIBITED_INHERITANCE",
                f"Downstream node {node_id(target)} consumes RGV PASS {node_id(source)} with prohibited semantic reliance {token}",
            )
        )

    expansion_tokens = semantic_tokens_for_fields(target, EXPANSION_SEMANTIC_FIELDS)
    prohibited_expansion = sorted(expansion_tokens & PROHIBITED_SEMANTIC_VALUES)

    if prohibited_expansion and not has_valid_new_claim_node(target, nodes_by_id):
        for token in prohibited_expansion:
            errors.append(
                err(
                    "UNAUTHORIZED_INFERENCE_EXPANSION",
                    f"Downstream node {node_id(target)} expands RGV PASS {node_id(source)} into {token} without a new claim node carrying its own authority and evidence basis",
                )
            )

    return errors


def check_indeterminate_not_treated_as_pass(source: dict[str, Any], target: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    if result_status(source) != "INDETERMINATE":
        return errors

    tokens = semantic_tokens_for_fields(
        target,
        HARD_SEMANTIC_FIELDS | {"result_mapping", "source_result_mapping"},
    )

    if tokens & PASS_ALIASES:
        errors.append(
            err(
                "INDETERMINATE_TREATED_AS_PASS",
                f"Downstream node {node_id(target)} treats INDETERMINATE source {node_id(source)} as PASS",
            )
        )

    return errors


def check_graph(graph: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    nodes = graph.get("nodes")
    edges = graph.get("edges")

    if not isinstance(nodes, list):
        errors.append(err("MISSING_NODES", "graph.nodes must be a list"))
        return errors

    if not isinstance(edges, list):
        errors.append(err("MISSING_EDGES", "graph.edges must be a list"))
        return errors

    nodes_by_id: dict[str, dict[str, Any]] = {}

    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(err("INVALID_NODE", f"nodes[{index}] must be an object"))
            continue

        ident = node_id(node)
        if ident is None:
            errors.append(err("MISSING_NODE_ID", f"nodes[{index}] is missing node_id"))
            continue

        if ident in nodes_by_id:
            errors.append(err("DUPLICATE_NODE_ID", f"Duplicate node_id {ident}"))
            continue

        nodes_by_id[ident] = node

    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            errors.append(err("INVALID_EDGE", f"edges[{index}] must be an object"))
            continue

        source_id = edge_source(edge)
        target_id = edge_target(edge)

        if source_id not in nodes_by_id:
            errors.append(err("MISSING_EDGE_SOURCE", f"edges[{index}] references missing source node {source_id}"))
            continue

        if target_id not in nodes_by_id:
            errors.append(err("MISSING_EDGE_TARGET", f"edges[{index}] references missing target node {target_id}"))
            continue

        source = nodes_by_id[source_id]
        target = nodes_by_id[target_id]
        kind = edge_type(edge)

        if kind not in CONSUMPTION_EDGE_TYPES and target.get("record_type") != "CLAIM_CONSUMPTION_EVENT":
            continue

        status = result_status(source)

        if is_rgv_result(source) and status == "PASS":
            errors.extend(
                check_pass_consumption_preserves_non_claims(
                    source=source,
                    target=target,
                    edge=edge,
                    nodes_by_id=nodes_by_id,
                )
            )

        if is_rgv_result(source) and status == "INDETERMINATE":
            errors.extend(check_indeterminate_not_treated_as_pass(source, target))

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            json.dumps(
                {
                    "result": "ERROR",
                    "errors": [
                        err(
                            "USAGE",
                            "Usage: check_rgv_required_source_non_claim_graph_preservation_v0_1.py <graph.json>",
                        )
                    ],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 2

    path = Path(argv[1])

    try:
        graph = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        print(
            json.dumps(
                {
                    "result": "FAIL",
                    "checked_graph": str(path),
                    "errors": [err("JSON_PARSE_ERROR", str(exc))],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    if not isinstance(graph, dict):
        print(
            json.dumps(
                {
                    "result": "FAIL",
                    "checked_graph": str(path),
                    "errors": [err("GRAPH_NOT_OBJECT", "Graph must be a JSON object")],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    errors = check_graph(graph)
    result = "PASS" if not errors else "FAIL"

    output = {
        "checker": "check_rgv_required_source_non_claim_graph_preservation_v0_1",
        "checked_graph": str(path),
        "result": result,
        "errors": errors,
        "required_non_claim_ids": sorted(REQUIRED_NON_CLAIM_IDS),
        "checker_non_claims": [
            "This checker does not verify SOURCE_TRUTH.",
            "This checker does not determine factual basis, wholeness, completeness, admissibility, or lawfulness.",
            "This checker enforces downstream preservation of required source non-claim boundaries when consuming RGV PASS results.",
            "This checker does not mutate or reinterpret the v0.4 evidentiary-weight profile contract."
        ],
    }

    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))