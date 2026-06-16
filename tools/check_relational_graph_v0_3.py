#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


VERIFIER_VERSION = "RGV_v0_3"

REQUIRED_GRAPH_NON_CLAIMS = {
    "RGV_NON_CLAIM_SOURCE_TRUTH",
    "RGV_NON_CLAIM_LEGAL_OR_COMPLIANCE_SUFFICIENCY",
    "RGV_NON_CLAIM_RUNTIME_ENFORCEMENT",
    "RGV_NON_CLAIM_EXTERNAL_POINTER_VALIDATION",
    "RGV_NON_CLAIM_COMPLETE_HISTORY",
}

REQUIRED_CCE_NON_CLAIMS = {
    "CCE_NON_CLAIM_SOURCE_TRUTH",
    "CCE_NON_CLAIM_LEGAL_OR_REGULATORY_SUFFICIENCY",
    "CCE_NON_CLAIM_RUNTIME_ENFORCEMENT",
    "CCE_NON_CLAIM_SOURCE_COMPLETENESS",
    "CCE_NON_CLAIM_EXPANDED_CLAIM_NODE",
}

ABSOLUTE_ASSURANCE_TERMS = [
    "unfalsifiable",
    "guaranteed",
    "guarantee",
    "fully compliant",
    "complete coverage",
    "safe for production",
    "ready for deployment",
    "no risk",
    "source truth fully confirmed",
    "absolute truth",
    "deployment approved",
    "compliance certification",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def repo_root_from_tool() -> Path:
    return Path(__file__).resolve().parents[1]


def validator(schema: dict[str, Any]) -> Draft202012Validator:
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def schema_errors(schema: dict[str, Any], instance: dict[str, Any], prefix: str) -> list[str]:
    errors = []
    for err in sorted(validator(schema).iter_errors(instance), key=lambda e: list(e.path)):
        path = ".".join(str(part) for part in err.path) or "<root>"
        errors.append(f"{prefix}: schema error at {path}: {err.message}")
    return errors


def duplicate_values(values: list[str]) -> list[str]:
    counts = Counter(v for v in values if v)
    return sorted(value for value, count in counts.items() if count > 1)


def is_external_pointer(value: str | None) -> bool:
    return isinstance(value, str) and (value.startswith("https://") or value.startswith("uri:"))


def non_claim_ids(record: dict[str, Any], key: str = "non_claims") -> set[str]:
    return {
        item.get("non_claim_id")
        for item in record.get(key, [])
        if isinstance(item, dict) and item.get("non_claim_id")
    }


def has_unknown(instance: dict[str, Any], claim_id: str | None = None, unknown_id: str | None = None) -> bool:
    for unknown in instance.get("unresolved_unknowns", []):
        if not isinstance(unknown, dict):
            continue
        if unknown_id and unknown.get("unknown_id") == unknown_id:
            return True
        if claim_id and unknown.get("related_claim_id") == claim_id:
            return True
    return False


def detect_cycles(edges: list[dict[str, str]]) -> list[str]:
    graph: dict[str, list[str]] = defaultdict(list)
    for edge in edges:
        graph[edge["from_claim_id"]].append(edge["to_claim_id"])

    cycles: list[str] = []
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []

    def dfs(node: str) -> None:
        if node in visiting:
            try:
                start = stack.index(node)
                cycle = stack[start:] + [node]
            except ValueError:
                cycle = [node, node]
            cycles.append(" -> ".join(cycle))
            return
        if node in visited:
            return
        visiting.add(node)
        stack.append(node)
        for nxt in graph.get(node, []):
            dfs(nxt)
        stack.pop()
        visiting.remove(node)
        visited.add(node)

    for node in list(graph):
        dfs(node)
    return sorted(set(cycles))


def build_result(bundle: dict[str, Any], errors: list[str], warnings: list[str], graph_edges: list[dict[str, str]], external_pointers: list[dict[str, str]], unresolved_pointers: list[dict[str, str]], local_cbc_ids: list[str], local_cce_ids: list[str]) -> dict[str, Any]:
    if errors:
        overall_state = "FAIL"
        graph_closure_state = "INVALID"
    elif unresolved_pointers:
        overall_state = "INDETERMINATE"
        graph_closure_state = "OPEN_UNRESOLVED_POINTERS"
    elif external_pointers:
        overall_state = "PASS"
        graph_closure_state = "OPEN_EXTERNAL_POINTERS"
    else:
        overall_state = "PASS"
        graph_closure_state = "CLOSED_LOCAL"

    return {
        "record_type": "RELATIONAL_GRAPH_VERIFICATION_RESULT",
        "verifier_version": VERIFIER_VERSION,
        "bundle_id": bundle.get("graph_id"),
        "overall_state": overall_state,
        "graph_closure_state": graph_closure_state,
        "checked_counts": {
            "cbc_records": len(bundle.get("cbc_records", [])),
            "cce_records": len(bundle.get("cce_records", [])),
            "graph_edges": len(graph_edges),
            "external_pointers": len(external_pointers),
            "unresolved_pointers": len(unresolved_pointers),
        },
        "local_cbc_ids": local_cbc_ids,
        "local_cce_ids": local_cce_ids,
        "graph_edges": graph_edges,
        "external_pointers": external_pointers,
        "unresolved_pointers": unresolved_pointers,
        "errors": errors,
        "warnings": warnings,
        "result_non_claims": [
            {"non_claim_id": "RGV_RESULT_NON_CLAIM_SOURCE_TRUTH", "statement": "This result does not assert that any source claim is true."},
            {"non_claim_id": "RGV_RESULT_NON_CLAIM_LEGAL_OR_COMPLIANCE_SUFFICIENCY", "statement": "This result does not assert legal, regulatory, contractual, or compliance sufficiency."},
            {"non_claim_id": "RGV_RESULT_NON_CLAIM_RUNTIME_ENFORCEMENT", "statement": "This result does not enforce, approve, block, or authorize runtime behavior."},
            {"non_claim_id": "RGV_RESULT_NON_CLAIM_EXTERNAL_POINTER_VALIDATION", "statement": "External pointers are not locally validated unless the referenced artifact is present in the supplied bundle and validated there."},
            {"non_claim_id": "RGV_RESULT_NON_CLAIM_COMPLETE_HISTORY", "statement": "This result does not assert that the bundle contains complete historical lineage."},
        ],
    }


def validate_bundle(bundle: dict[str, Any], repo_root: Path | None = None) -> dict[str, Any]:
    if repo_root is None:
        repo_root = repo_root_from_tool()

    schema_dir = repo_root / "schemas"
    bundle_schema = load_json(schema_dir / "relational_graph_bundle_v0_3.schema.json")
    cbc_schema = load_json(schema_dir / "claim_boundary_contract_v0_2_2.schema.json")
    cce_schema = load_json(schema_dir / "claim_consumption_events_v0_2_2.schema.json")

    errors: list[str] = []
    warnings: list[str] = []
    graph_edges: list[dict[str, str]] = []
    external_pointers: list[dict[str, str]] = []
    unresolved_pointers: list[dict[str, str]] = []

    errors.extend(schema_errors(bundle_schema, bundle, "bundle"))

    cbc_wrappers = bundle.get("cbc_records", [])
    cce_wrappers = bundle.get("cce_records", [])

    artifact_to_cbc: dict[str, dict[str, Any]] = {}
    cbc_by_claim_id: dict[str, dict[str, Any]] = {}
    local_cbc_ids: list[str] = []

    for duplicate in duplicate_values([w.get("artifact_id") for w in cbc_wrappers if isinstance(w, dict)]):
        errors.append(f"duplicate CBC artifact_id: {duplicate}")

    for index, wrapper in enumerate(cbc_wrappers):
        if not isinstance(wrapper, dict):
            errors.append(f"cbc_records[{index}] is not an object")
            continue
        artifact_id = wrapper.get("artifact_id", f"cbc_records[{index}]")
        record = wrapper.get("record", {})
        errors.extend(schema_errors(cbc_schema, record, f"CBC {artifact_id}"))
        claim_id = record.get("claim_id")
        if claim_id:
            if claim_id in cbc_by_claim_id:
                errors.append(f"duplicate CBC claim_id: {claim_id}")
            cbc_by_claim_id[claim_id] = record
            local_cbc_ids.append(claim_id)
        artifact_to_cbc[artifact_id] = record

    for duplicate in duplicate_values([w.get("artifact_id") for w in cce_wrappers if isinstance(w, dict)]):
        errors.append(f"duplicate CCE artifact_id: {duplicate}")

    cce_event_ids: list[str] = []

    for index, wrapper in enumerate(cce_wrappers):
        if not isinstance(wrapper, dict):
            errors.append(f"cce_records[{index}] is not an object")
            continue
        artifact_id = wrapper.get("artifact_id", f"cce_records[{index}]")
        cce = wrapper.get("record", {})
        errors.extend(schema_errors(cce_schema, cce, f"CCE {artifact_id}"))

        event_id = cce.get("event_id")
        if event_id:
            cce_event_ids.append(event_id)

        consumed_claims = cce.get("consumed_claims", [])
        consumed_ids = [claim.get("claim_id") for claim in consumed_claims if isinstance(claim, dict)]
        for duplicate in duplicate_values(consumed_ids):
            errors.append(f"CCE {artifact_id}: duplicate consumed claim_id: {duplicate}")

        consumed_set = set(consumed_ids)
        relied = set(cce.get("relied_claim_ids", []))
        rejected = set(cce.get("rejected_claim_ids", []))
        if relied - consumed_set:
            errors.append(f"CCE {artifact_id}: relied_claim_ids not consumed: {sorted(relied - consumed_set)}")
        if rejected - consumed_set:
            errors.append(f"CCE {artifact_id}: rejected_claim_ids not consumed: {sorted(rejected - consumed_set)}")
        if relied & rejected:
            errors.append(f"CCE {artifact_id}: claim_ids cannot be both relied and rejected: {sorted(relied & rejected)}")

        consumed_by_id = {claim.get("claim_id"): claim for claim in consumed_claims if isinstance(claim, dict) and claim.get("claim_id")}
        required_preserved: set[str] = set()
        local_sources_for_edge: set[str] = set()

        for claim_id in relied:
            claim = consumed_by_id.get(claim_id)
            if not claim:
                continue
            required_preserved.update(claim.get("source_non_claim_ids", []))
            source_artifact_id = claim.get("source_artifact_id")
            source_cbc = None

            if source_artifact_id:
                if is_external_pointer(source_artifact_id):
                    external_pointers.append(
                        {
                            "event_id": str(event_id),
                            "pointer_type": "CONSUMED_SOURCE_CBC",
                            "reference": source_artifact_id,
                            "state": "EXTERNAL_POINTER",
                        }
                    )
                    warnings.append(
                        f"CCE {artifact_id}: consumed source is external and was not locally validated: {source_artifact_id}"
                    )
                else:
                    source_cbc = artifact_to_cbc.get(source_artifact_id)
                    if source_cbc is None:
                        errors.append(
                            f"CCE {artifact_id}: consumed source CBC not found locally for claim {claim_id}"
                        )
            else:
                source_cbc = cbc_by_claim_id.get(claim_id)
                if source_cbc is None:
                    errors.append(
                        f"CCE {artifact_id}: consumed source CBC not found locally for claim {claim_id}"
                    )

            if source_cbc is not None:
                source_claim_id = source_cbc.get("claim_id")
                if source_claim_id != claim_id:
                    errors.append(
                        f"CCE {artifact_id}: consumed source artifact claim_id mismatch for {claim_id}"
                    )

                local_sources_for_edge.add(source_claim_id or claim_id)

                cce_ids = set(claim.get("source_non_claim_ids", []))
                source_ids = non_claim_ids(source_cbc)
                if cce_ids != source_ids:
                    errors.append(
                        f"CCE {artifact_id}: source_non_claim_ids do not match local CBC for {claim_id}"
                    )

            if claim.get("verification_state") != "PASS" and not has_unknown(cce, claim_id=claim_id):
                errors.append(f"CCE {artifact_id}: non-PASS relied claim requires unresolved_unknown: {claim_id}")

            for limitation in claim.get("source_assurance", {}).get("assurance_limitations", []):
                lower = str(limitation).lower()
                for term in ABSOLUTE_ASSURANCE_TERMS:
                    if term in lower:
                        errors.append(f"CCE {artifact_id}: assurance_limitations contains absolute assurance language: {term}")

        missing_preserved = required_preserved - set(cce.get("preserved_non_claim_ids", []))
        if missing_preserved:
            errors.append(f"CCE {artifact_id}: non_claims from relied claims not preserved: {sorted(missing_preserved)}")

        cce_non_claim_ids = [item.get("non_claim_id") for item in cce.get("cce_non_claims", []) if isinstance(item, dict)]
        for duplicate in duplicate_values(cce_non_claim_ids):
            errors.append(f"CCE {artifact_id}: duplicate cce_non_claim_id: {duplicate}")
        missing_cce_non_claims = REQUIRED_CCE_NON_CLAIMS - set(cce_non_claim_ids)
        if missing_cce_non_claims:
            errors.append(f"CCE {artifact_id}: required CCE non_claims missing: {sorted(missing_cce_non_claims)}")

        effect = cce.get("boundary_effect")
        detail = cce.get("boundary_effect_detail", {})
        downstream = cce.get("downstream_output", {})
        resolution = detail.get("new_claim_reference_resolution")
        new_claim_reference = detail.get("new_claim_reference")
        new_cbc_id = detail.get("new_claim_boundary_contract_id")
        new_claim_ids = set(downstream.get("new_claim_ids", []))
        expansion_fields = ["expansion_reason", "new_claim_reference", "new_claim_boundary_contract_id", "authorizing_party", "additional_evidence_refs"]

        if effect == "EXPANDED":
            for field in expansion_fields:
                value = detail.get(field)
                if value is None or value == "" or value == []:
                    errors.append(f"CCE {artifact_id}: EXPANDED boundary_effect requires {field}")
            if resolution == "NOT_APPLICABLE":
                errors.append(f"CCE {artifact_id}: EXPANDED boundary_effect cannot use NOT_APPLICABLE resolution")
            if new_cbc_id and new_cbc_id not in new_claim_ids:
                errors.append(f"CCE {artifact_id}: downstream_output.new_claim_ids must include boundary_effect_detail.new_claim_boundary_contract_id")
            if resolution == "LOCAL_RESOLVED":
                if new_cbc_id not in cbc_by_claim_id:
                    errors.append(f"CCE {artifact_id}: LOCAL_RESOLVED target CBC not found locally: {new_cbc_id}")
                else:
                    for source_id in sorted(local_sources_for_edge):
                        graph_edges.append({"event_id": str(event_id), "edge_type": "EXPANDED", "from_claim_id": source_id, "to_claim_id": new_cbc_id})
            elif resolution == "EXTERNAL_POINTER":
                if not is_external_pointer(new_claim_reference):
                    errors.append(f"CCE {artifact_id}: EXTERNAL_POINTER requires https:// or uri: reference")
                else:
                    external_pointers.append({"event_id": str(event_id), "pointer_type": "NEW_CLAIM_BOUNDARY", "reference": str(new_claim_reference), "target_claim_id": str(new_cbc_id), "state": "EXTERNAL_POINTER"})
                    warnings.append(f"CCE {artifact_id}: external new-claim boundary pointer was recorded but not locally validated")
            elif resolution == "NOT_RESOLVED":
                unresolved_pointers.append({"event_id": str(event_id), "pointer_type": "NEW_CLAIM_BOUNDARY", "target_claim_id": str(new_cbc_id), "state": "NOT_RESOLVED"})
                if not has_unknown(cce, claim_id=new_cbc_id, unknown_id="unknown_new_claim_boundary_unresolved"):
                    errors.append(f"CCE {artifact_id}: NOT_RESOLVED pointer requires unresolved_unknown marker")
            elif resolution not in {"LOCAL_RESOLVED", "EXTERNAL_POINTER", "NOT_RESOLVED"}:
                errors.append(f"CCE {artifact_id}: invalid expansion pointer resolution: {resolution}")
            if "expanded_claim" in cce or "expanded_claim_body" in cce:
                errors.append(f"CCE {artifact_id}: CCE must not contain expanded claim body")
            if "expanded_claim" in detail or "expanded_claim_body" in detail:
                errors.append(f"CCE {artifact_id}: CCE boundary_effect_detail must not contain expanded claim body")
        elif effect == "PRESERVED":
            if resolution != "NOT_APPLICABLE":
                errors.append(f"CCE {artifact_id}: PRESERVED boundary_effect requires NOT_APPLICABLE resolution")
            if new_claim_ids:
                errors.append(f"CCE {artifact_id}: PRESERVED boundary_effect cannot create downstream new_claim_ids")
            present = [field for field in ["narrowing_reason"] + expansion_fields if detail.get(field)]
            if present:
                errors.append(f"CCE {artifact_id}: PRESERVED boundary_effect cannot contain boundary-change fields: {present}")
        elif effect == "NARROWED":
            if resolution != "NOT_APPLICABLE":
                errors.append(f"CCE {artifact_id}: NARROWED boundary_effect requires NOT_APPLICABLE resolution")
            if new_claim_ids:
                errors.append(f"CCE {artifact_id}: NARROWED boundary_effect cannot create downstream new_claim_ids")
            if not detail.get("narrowing_reason"):
                errors.append(f"CCE {artifact_id}: NARROWED boundary_effect requires narrowing_reason")
            present = [field for field in expansion_fields if detail.get(field)]
            if present:
                errors.append(f"CCE {artifact_id}: NARROWED boundary_effect cannot contain expansion fields: {present}")
        else:
            errors.append(f"CCE {artifact_id}: unknown boundary_effect: {effect}")

    for duplicate in duplicate_values(cce_event_ids):
        errors.append(f"duplicate CCE event_id: {duplicate}")

    bundle_non_claim_ids = [item.get("non_claim_id") for item in bundle.get("bundle_non_claims", []) if isinstance(item, dict)]
    for duplicate in duplicate_values(bundle_non_claim_ids):
        errors.append(f"duplicate bundle non_claim_id: {duplicate}")
    missing_graph_non_claims = REQUIRED_GRAPH_NON_CLAIMS - set(bundle_non_claim_ids)
    if missing_graph_non_claims:
        errors.append(f"required graph bundle non_claims missing: {sorted(missing_graph_non_claims)}")

    for cycle in detect_cycles(graph_edges):
        errors.append(f"cycle detected in local CBC expansion graph: {cycle}")

    return build_result(bundle, errors, warnings, graph_edges, external_pointers, unresolved_pointers, sorted(set(local_cbc_ids)), sorted(set(cce_event_ids)))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify a Fork relational graph bundle v0.3.")
    parser.add_argument("bundle", help="Path to relational_graph_bundle_v0_3 JSON file")
    parser.add_argument("--repo-root", default=None, help="Repository root. Defaults to parent of this tool.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve() if args.repo_root else repo_root_from_tool()
    result = validate_bundle(load_json(Path(args.bundle)), repo_root=repo_root)
    print(json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False))
    return 0 if result["overall_state"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
