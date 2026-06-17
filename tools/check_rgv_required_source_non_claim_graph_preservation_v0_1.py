#!/usr/bin/env python3
"""
RGV Required Source Non-Claim Graph Preservation v0.1 checker.

This checker enforces downstream preservation of required source non-claims
when an RGV PASS result is consumed by CCE-like graph-composition nodes.

It does not verify source truth, factual basis, wholeness, completeness,
admissibility, lawfulness, legal sufficiency, compliance, safety, correctness,
institutional authority, runtime authorization, or source completeness.

This checker performs structural alias detection over known machine-readable
metadata fields. It does not perform NLP or adjudicate arbitrary human prose.
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
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

NEW_CLAIM_SEMANTIC_FIELDS = EXPANSION_SEMANTIC_FIELDS | {
    "declared_claims",
    "claims",
    "claim_id",
    "claim_type",
    "supported_claims",
    "semantic_assertions",
}

PROHIBITED_SEMANTIC_VALUES = {
    "SOURCE_TRUTH",
    "SOURCE_TRUTH_ASSERTED",
    "SOURCE_TRUTH_CONFIRMED",
    "SOURCE_TRUTH_VERIFICATION",
    "SOURCE_DATA_IS_VERIFIED_TRUTH",
    "VERIFIED_TRUTH",
    "VALIDATED_FACT",
    "CONFIRMED_TRUTH",
    "FACTUAL_BASIS_CONFIRMED",
    "FACTUAL_CONFIRMATION",
    "FACTUALLY_CHECKED",
    "FACTUALLY_SUPPORTED",
    "EVIDENCE_CONFIRMED",
    "WHOLE_STORY",
    "WHOLENESS_ASSERTED",
    "COMPREHENSIVE",
    "COMPLETE_PICTURE",
    "COMPLETE_EVIDENCE",
    "COMPLETENESS_ASSERTION",
    "ADMISSIBLE",
    "ADMISSIBILITY_INFERRED",
    "ADMISSIBILITY_INFERENCE",
    "LEGALLY_USABLE",
    "COURT_APPROPRIATE",
    "LAWFUL",
    "LAWFULNESS_IMPLIED",
    "LAWFULNESS_DETERMINATION",
    "LEGALLY_COMPLIANT",
    "REGULATORY_CONFORMING",
    "FULLY_COMPLIANT_BY_FORK_PASS",
    "APPROVED_BY_FORK",
}

STRUCTURAL_METADATA_ROOT_FIELDS = {
    "METADATA",
    "EXTENSIONS",
    "CUSTOM_DOWNSTREAM_EXTENSIONS",
    "CONSUMPTION_CONTEXT",
    "INTERPRETATION",
    "LEGAL_ASSESSMENT",
    "FACTUAL_STATUS",
    "CLEARANCE_LEVEL",
    "ASSUMED_STATUS",
    "DOWNSTREAM_METADATA",
    "MACHINE_METADATA",
}

PROHIBITED_ALIAS_FRAGMENTS = {
    "SOURCE_TRUTH",
    "VERIFIED_TRUTH",
    "FACTUAL",
    "FACTUALLY",
    "FACT_CHECKED",
    "ADMISSIBLE",
    "ADMISSIBILITY",
    "LAWFUL",
    "LAWFULNESS",
    "LEGAL_CLEARANCE",
    "LEGAL_COMPLIANCE",
    "COMPLIANT_BY_FORK",
    "FULLY_COMPLIANT",
    "COMPLETE_EVIDENCE",
    "WHOLE_STORY",
    "APPROVED_BY_FORK",
    "CONFIRMED_BY_FORK",
    "VALIDATED_BY_FORK",
}

FREE_TEXT_FIELDS_NOT_SCANNED = {
    "summary",
    "notes",
    "description",
    "comment",
    "comments",
    "rationale",
    "human_readable_summary",
}

NON_CLAIM_FIELDS = {
    "preserved_non_claims",
    "required_source_non_claims",
    "result_non_claims",
    "non_claims",
    "required_source_non_claim_bundle",
}

FAIL_FALSE_VALUES = {
    "SOURCE_FALSE",
    "FALSE",
    "FACTUALLY_FALSE",
    "UNLAWFUL",
    "ILLEGAL",
    "INADMISSIBLE",
    "FACTUALLY_UNSUPPORTED",
    "UNSUPPORTED_FACTS",
    "SOURCE_INVALID",
    "CONTENT_FALSE",
}

FORK_PASS_REFERENCE_TOKENS = {
    "RGV_PASS",
    "FORK_RGV_PASS",
    "STRUCTURAL_PASS",
    "FORK_PASS",
    "RGV_VERIFICATION_RESULT",
}


def err(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}


def is_non_empty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def normalize_token(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value)
    normalized = normalized.strip().upper()
    normalized = re.sub(r"[^A-Z0-9]+", "_", normalized).strip("_")
    return normalized


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
            return normalize_token(value)

    state = node.get("verification_state")
    if isinstance(state, dict):
        value = state.get("status")
        if is_non_empty(value):
            return normalize_token(value)

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


def iter_reference_strings(value: Any):
    if isinstance(value, str) and value.strip():
        yield value.strip()
    elif isinstance(value, list):
        for item in value:
            yield from iter_reference_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_reference_strings(item)


def truthy_structural_value(value: Any) -> bool:
    if value is True:
        return True
    if value in (False, None):
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return bool(value)


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


def contains_any_fragment(token: str, fragments: set[str]) -> bool:
    return any(fragment in token for fragment in fragments)


def scan_structured_metadata(value: Any, path: list[str]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                continue

            key_token = normalize_token(key)
            child_path = path + [key]

            if contains_any_fragment(key_token, PROHIBITED_ALIAS_FRAGMENTS) and truthy_structural_value(child):
                errors.append(
                    err(
                        "STRUCTURAL_METADATA_CONTRADICTION",
                        f"Structured metadata path {'.'.join(child_path)} carries a prohibited Fork/RGV inference alias",
                    )
                )

            if isinstance(child, str):
                child_token = normalize_token(child)
                if contains_any_fragment(child_token, PROHIBITED_ALIAS_FRAGMENTS):
                    errors.append(
                        err(
                            "STRUCTURAL_METADATA_CONTRADICTION",
                            f"Structured metadata path {'.'.join(child_path)} carries prohibited semantic value {child_token}",
                        )
                    )

            errors.extend(scan_structured_metadata(child, child_path))

    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(scan_structured_metadata(child, path + [str(index)]))

    elif isinstance(value, str):
        token = normalize_token(value)
        if contains_any_fragment(token, PROHIBITED_ALIAS_FRAGMENTS):
            errors.append(
                err(
                    "STRUCTURAL_METADATA_CONTRADICTION",
                    f"Structured metadata path {'.'.join(path)} carries prohibited semantic value {token}",
                )
            )

    return errors


def find_structured_metadata_aliases(node: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    for key, value in node.items():
        if not isinstance(key, str):
            continue

        key_token = normalize_token(key)

        if key in FREE_TEXT_FIELDS_NOT_SCANNED:
            continue

        if key in NON_CLAIM_FIELDS:
            continue

        if key_token in STRUCTURAL_METADATA_ROOT_FIELDS:
            errors.extend(scan_structured_metadata(value, [key]))
            continue

        if contains_any_fragment(key_token, PROHIBITED_ALIAS_FRAGMENTS) and truthy_structural_value(value):
            errors.append(
                err(
                    "STRUCTURAL_METADATA_CONTRADICTION",
                    f"Structured field {key} carries a prohibited Fork/RGV inference alias",
                )
            )

    return errors


def get_new_claim_node(node: dict[str, Any], nodes_by_id: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    new_claim_node_id = node.get("new_claim_node_id")
    if not is_non_empty(new_claim_node_id):
        return None

    claim = nodes_by_id.get(new_claim_node_id)
    return claim if isinstance(claim, dict) else None


def has_claim_boundary(value: dict[str, Any]) -> bool:
    for field in ("non_claims", "required_source_non_claims", "required_source_non_claim_bundle", "claim_boundary"):
        if value.get(field):
            return True
    return False


def has_valid_new_claim_node(node: dict[str, Any], nodes_by_id: dict[str, dict[str, Any]]) -> bool:
    claim = get_new_claim_node(node, nodes_by_id)
    if not isinstance(claim, dict):
        return False

    authority = claim.get("authority_basis") or claim.get("authority_refs") or claim.get("authority")
    evidence = claim.get("evidence_basis") or claim.get("evidence_refs") or claim.get("evidence")

    authority_present = bool(authority) if not isinstance(authority, str) else bool(authority.strip())
    evidence_present = bool(evidence) if not isinstance(evidence, str) else bool(evidence.strip())

    return authority_present and evidence_present and has_claim_boundary(claim)


def source_reference_tokens(source: dict[str, Any]) -> set[str]:
    tokens = set(FORK_PASS_REFERENCE_TOKENS)
    ident = node_id(source)
    if ident:
        tokens.add(normalize_token(ident))
    return tokens


def references_only_fork_pass(value: Any, source: dict[str, Any]) -> bool:
    refs = [normalize_token(item) for item in iter_reference_strings(value)]
    if not refs:
        return False

    source_refs = source_reference_tokens(source)
    return all(ref in source_refs for ref in refs)


def references_fork_pass(value: Any, source: dict[str, Any]) -> bool:
    refs = {normalize_token(item) for item in iter_reference_strings(value)}
    return bool(refs & source_reference_tokens(source))


def check_new_claim_shadowing(
    source: dict[str, Any],
    target: dict[str, Any],
    nodes_by_id: dict[str, dict[str, Any]],
    prohibited_expansion: list[str],
) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    if not prohibited_expansion:
        return errors

    claim = get_new_claim_node(target, nodes_by_id)
    if not isinstance(claim, dict):
        return errors

    authority = claim.get("authority_basis") or claim.get("authority_refs") or claim.get("authority")
    evidence = claim.get("evidence_basis") or claim.get("evidence_refs") or claim.get("evidence")

    if references_fork_pass(authority, source):
        errors.append(
            err(
                "FORK_PASS_USED_AS_EXPANSION_AUTHORITY",
                f"New claim node {node_id(claim)} uses RGV PASS {node_id(source)} as authority for prohibited expansion",
            )
        )

    if references_only_fork_pass(evidence, source):
        errors.append(
            err(
                "FORK_PASS_SOLE_EVIDENCE_FOR_PROHIBITED_EXPANSION",
                f"New claim node {node_id(claim)} uses RGV PASS {node_id(source)} as the sole evidence basis for prohibited expansion",
            )
        )

    return errors


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
    errors.extend(find_structured_metadata_aliases(target))

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

    claim = get_new_claim_node(target, nodes_by_id)
    if isinstance(claim, dict):
        expansion_tokens |= semantic_tokens_for_fields(claim, NEW_CLAIM_SEMANTIC_FIELDS)
        errors.extend(find_structured_metadata_aliases(claim))

    prohibited_expansion = sorted(expansion_tokens & PROHIBITED_SEMANTIC_VALUES)

    if prohibited_expansion and not has_valid_new_claim_node(target, nodes_by_id):
        for token in prohibited_expansion:
            errors.append(
                err(
                    "UNAUTHORIZED_INFERENCE_EXPANSION",
                    f"Downstream node {node_id(target)} expands RGV PASS {node_id(source)} into {token} without a new claim node carrying its own authority, evidence, and non-claim boundary",
                )
            )

    if prohibited_expansion and has_valid_new_claim_node(target, nodes_by_id):
        errors.extend(
            check_new_claim_shadowing(
                source=source,
                target=target,
                nodes_by_id=nodes_by_id,
                prohibited_expansion=prohibited_expansion,
            )
        )

    return errors


def check_indeterminate_not_treated_as_pass(source: dict[str, Any], target: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    if result_status(source) != "INDETERMINATE":
        return errors

    tokens = semantic_tokens_for_fields(
        target,
        HARD_SEMANTIC_FIELDS | EXPANSION_SEMANTIC_FIELDS | {"result_mapping", "source_result_mapping"},
    )

    if tokens & PASS_ALIASES:
        errors.append(
            err(
                "INDETERMINATE_TREATED_AS_PASS",
                f"Downstream node {node_id(target)} treats INDETERMINATE source {node_id(source)} as PASS",
            )
        )

    prohibited = sorted(tokens & PROHIBITED_SEMANTIC_VALUES)
    for token in prohibited:
        errors.append(
            err(
                "INDETERMINATE_USED_AS_PROHIBITED_SUPPORT",
                f"Downstream node {node_id(target)} uses INDETERMINATE source {node_id(source)} as prohibited support for {token}",
            )
        )

    return errors


def check_fail_not_treated_as_source_falsity(source: dict[str, Any], target: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    if result_status(source) != "FAIL":
        return errors

    tokens = semantic_tokens_for_fields(
        target,
        HARD_SEMANTIC_FIELDS | EXPANSION_SEMANTIC_FIELDS | {"failure_meaning", "source_result_interpretation", "result_mapping"},
    )

    false_tokens = sorted(tokens & FAIL_FALSE_VALUES)
    for token in false_tokens:
        errors.append(
            err(
                "FAIL_TREATED_AS_LEGAL_OR_FACTUAL_DETERMINATION",
                f"Downstream node {node_id(target)} treats FAIL source {node_id(source)} as {token}; FAIL is a structural semantics posture, not a source-content determination",
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

        if is_rgv_result(source) and status == "FAIL":
            errors.extend(check_fail_not_treated_as_source_falsity(source, target))

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
            "This checker performs structural alias checks over known machine-readable metadata fields but does not perform NLP.",
            "This checker does not mutate or reinterpret the v0.4 evidentiary-weight profile contract."
        ],
    }

    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))