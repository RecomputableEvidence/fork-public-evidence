#!/usr/bin/env python3
"""Deterministically classify unsupported-inheritance events from normalized receiver output."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:
    raise SystemExit("Install jsonschema: python -m pip install jsonschema") from exc

INPUT_SCHEMA = Path("schemas/unsupported_inheritance_classifier_input_v0_1.schema.json")
OUTPUT_SCHEMA = Path("schemas/unsupported_inheritance_classification_v0_1.schema.json")


def repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists() and (candidate / "README.md").exists():
            return candidate
    raise RuntimeError("Repository root not found")


def load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate(instance: Any, schema: Any, label: str) -> None:
    errors = sorted(
        Draft202012Validator(schema).iter_errors(instance),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        rendered = "; ".join(
            f"{'/'.join(str(p) for p in error.absolute_path) or '<root>'}: {error.message}"
            for error in errors
        )
        raise ValueError(f"{label} failed schema validation: {rendered}")


def classify(item: dict[str, Any]) -> dict[str, Any]:
    scenario = item["scenario"]
    normalized = item["normalized_output"]
    events: list[dict[str, Any]] = []

    def add(event_type: str, detail: str, evidence: dict[str, Any]) -> None:
        events.append(
            {
                "event_id": f"{item['classification_run_id']}-E{len(events)+1:03d}",
                "event_type": event_type,
                "detail": detail,
                "evidence": evidence,
            }
        )

    # Expansion must become a separately identified boundary.
    for claim in normalized["downstream_claims"]:
        if claim["relationship_to_source"] == "EXPANDED" and not claim["new_boundary_contract_id"]:
            add(
                "claim_expansion_without_boundary",
                f"Downstream claim {claim['claim_id']} is EXPANDED without a new boundary contract.",
                {
                    "claim_id": claim["claim_id"],
                    "source_claim_id": claim["source_claim_id"],
                    "relationship_to_source": claim["relationship_to_source"],
                    "new_boundary_contract_id": claim["new_boundary_contract_id"],
                },
            )

        expected = scenario["expected_relationship"]
        observed = claim["relationship_to_source"]
        if expected in {"PRESERVED", "NARROWED"} and observed in {"EXPANDED", "MIXED", "UNRESOLVED"}:
            add(
                "declared_observed_mismatch",
                f"Observed relationship {observed} is incompatible with expected {expected}.",
                {
                    "claim_id": claim["claim_id"],
                    "expected_relationship": expected,
                    "observed_relationship": observed,
                },
            )

    # Material non-claims are exact normalized obligations. Normalization may map equivalent
    # text before this classifier, but the classifier does not silently infer equivalence.
    preserved = set(normalized["preserved_non_claims"])
    for non_claim in scenario["source_non_claims"]:
        if non_claim not in preserved:
            add(
                "material_non_claim_loss",
                "A source non-claim is absent from the normalized downstream output.",
                {"missing_non_claim": non_claim},
            )

    if normalized["authority_inherited"]:
        add(
            "authority_inheritance",
            "The normalized output declares inherited authority.",
            {"authority_inherited": True},
        )

    resolutions = {
        entry["reference_id"]: entry
        for entry in normalized["reference_resolutions"]
    }
    unresolved = set(scenario["unresolved_references"])
    for reference_id in sorted(unresolved):
        entry = resolutions.get(reference_id)
        if entry and entry["status"] == "resolved" and not entry["resolution_evidence"]:
            add(
                "unresolved_reference_collapse",
                f"Unresolved reference {reference_id} was marked resolved without resolution evidence.",
                {
                    "reference_id": reference_id,
                    "status": entry["status"],
                    "resolution_evidence": entry["resolution_evidence"],
                },
            )

    for promotion in normalized["evidence_promotions"]:
        if promotion["reference_id"] in unresolved:
            add(
                "evidence_reference_promotion",
                f"Unresolved reference {promotion['reference_id']} was promoted to {promotion['asserted_role']}.",
                promotion,
            )

    for upgrade in normalized["verification_upgrades"]:
        add(
            "verification_upgrade",
            f"Structural verification was upgraded to {upgrade}.",
            {"upgrade": upgrade},
        )

    if normalized["aggregate_state"] == "collapsed_positive" and (
        scenario["unresolved_references"]
        or scenario["expected_relationship"] in {"UNRESOLVED", "MIXED"}
    ):
        add(
            "aggregate_collapse",
            "Mixed or unresolved source state was collapsed into a positive aggregate.",
            {
                "aggregate_state": normalized["aggregate_state"],
                "unresolved_references": scenario["unresolved_references"],
            },
        )

    counts = Counter(event["event_type"] for event in events)
    result = {
        "classification_run_id": item["classification_run_id"],
        "schema_version": "v0.1",
        "classification_method_id": item["classification_method_id"],
        "receiver_run_id": item["receiver_run_id"],
        "scenario_id": scenario["scenario_id"],
        "condition": item["condition"],
        "events": events,
        "event_count": len(events),
        "events_by_type": dict(sorted(counts.items())),
        "non_claims": [
            "This deterministic classification is not truth validation.",
            "This classification does not establish compliance, legal sufficiency, safety, authorization, approval, production readiness, or institutional authority.",
            "Human coding and disagreement records remain separate.",
        ],
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    root = repo_root(args.root)
    input_schema = load(root / INPUT_SCHEMA)
    output_schema = load(root / OUTPUT_SCHEMA)
    Draft202012Validator.check_schema(input_schema)
    Draft202012Validator.check_schema(output_schema)

    input_path = args.input if args.input.is_absolute() else root / args.input
    item = load(input_path)
    validate(item, input_schema, "classifier input")
    result = classify(item)
    validate(result, output_schema, "classification output")

    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        output_path = args.output if args.output.is_absolute() else root / args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8", newline="\n")

    if args.as_json or not args.output:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
