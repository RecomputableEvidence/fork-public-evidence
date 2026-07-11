#!/usr/bin/env python3
"""Check reviewer access-path integrity fixtures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:
    raise SystemExit("Install jsonschema: python -m pip install jsonschema") from exc

SCHEMA = Path("schemas/reviewer_access_path_observation_v0_1.schema.json")
FIXTURE_ROOT = Path("docs/recomputation/boundary-state-interop-v0.1.2/fixtures")

PROHIBITED_UPGRADE_TERMS = (
    "complete-package review",
    "package failure established",
    "negative content review completed",
    "repository is structurally defective",
    "complete package satisfies",
    "artifact checker failed",
)

RESTRICTED_ACCESS = {"partial_artifact", "transformed_or_excerpted", "retrieval_failed"}
RESTRICTED_FIDELITY = {"partial", "transformed", "none", "unresolved"}
RESTRICTED_INTERPRETER = {"incompatible"}
RESTRICTED_EXECUTION = {"failed", "unavailable"}


def root_from(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists() and (candidate / "README.md").exists():
            return candidate
    raise RuntimeError("Repository root not found")


def load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def semantic_errors(item: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    restricted = (
        item["access_state"] in RESTRICTED_ACCESS
        or item["retrieval_fidelity"] in RESTRICTED_FIDELITY
        or item["interpreter_state"] in RESTRICTED_INTERPRETER
        or item["execution_state"] in RESTRICTED_EXECUTION
    )

    if restricted and item["content_assessment_permitted"]:
        errors.append("content assessment permitted under restricted access/interpreter/execution state")
    if restricted and item["content_findings"]:
        errors.append("content findings present under restricted access/interpreter/execution state")

    claims_blob = "\n".join(item["review_claims"] + item["content_findings"]).lower()
    for term in PROHIBITED_UPGRADE_TERMS:
        if term in claims_blob:
            errors.append(f"prohibited access-to-content upgrade: {term}")

    if item["access_state"] == "retrieval_failed" and item["retrieval_fidelity"] != "none":
        errors.append("retrieval_failed requires retrieval_fidelity=none")
    if item["interpreter_state"] == "incompatible" and item["execution_state"] == "successful":
        errors.append("incompatible interpreter cannot report successful execution")
    if item["execution_state"] == "successful" and not item["content_assessment_permitted"]:
        errors.append("successful compatible execution should permit a bounded assessment")
    return errors


def evaluate(root: Path) -> dict[str, Any]:
    schema = load(root / SCHEMA)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    results: list[dict[str, Any]] = []
    fixture_paths = sorted((root / FIXTURE_ROOT).rglob("*.json"))
    for path in fixture_paths:
        item = load(path)
        schema_errors = [error.message for error in validator.iter_errors(item)]
        semantics = semantic_errors(item) if not schema_errors else []
        actual_valid = not schema_errors and not semantics
        expected_valid = bool(item.get("expected_valid"))
        passed = actual_valid == expected_valid
        results.append(
            {
                "fixture": path.relative_to(root).as_posix(),
                "observation_id": item.get("observation_id"),
                "expected_valid": expected_valid,
                "actual_valid": actual_valid,
                "passed": passed,
                "schema_errors": schema_errors,
                "semantic_errors": semantics,
            }
        )

    failed = [result for result in results if not result["passed"]]
    return {
        "checker": Path(__file__).name,
        "total": len(results),
        "passed": len(results) - len(failed),
        "failed": len(failed),
        "results": results,
        "interpretation": {
            "proves": [
                "shipped access-path fixtures match expected valid or invalid classification",
                "failed, partial, or incompatible access is not silently upgraded into content review",
            ],
            "does_not_prove": [
                "artifact truth",
                "compliance",
                "legal sufficiency",
                "safety",
                "authorization",
                "approval",
                "production readiness",
                "institutional authority",
            ],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    result = evaluate(root_from(args.root))
    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for item in result["results"]:
            print(
                f"[{'PASS' if item['passed'] else 'FAIL'}] "
                f"{item['observation_id']}: expected={item['expected_valid']} "
                f"actual={item['actual_valid']}"
            )
        print(
            "REVIEWER_ACCESS_PATH_INTEGRITY_PASS"
            if result["failed"] == 0
            else "REVIEWER_ACCESS_PATH_INTEGRITY_FAIL"
        )
    return 1 if result["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
