#!/usr/bin/env python3
"""Validate Public Review Round 006 structured observations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:
    raise SystemExit("Install jsonschema: python -m pip install jsonschema") from exc

SCHEMA = Path("schemas/public_review_round_006_observation_v0_1.schema.json")
OBS_ROOT = Path("docs/review/public-rounds/round-006/observations")


def repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists() and (candidate / "README.md").exists():
            return candidate
    raise RuntimeError("Repository root not found")


def load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def evaluate(root: Path) -> dict[str, Any]:
    schema = load(root / SCHEMA)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    results = []
    ids = set()

    for path in sorted((root / OBS_ROOT).glob("*.json")):
        item = load(path)
        errors = [error.message for error in validator.iter_errors(item)]
        if item.get("observation_id") in ids:
            errors.append("duplicate observation_id")
        ids.add(item.get("observation_id"))

        source_path = item.get("source_summary_path")
        if source_path and not (root / source_path).exists():
            errors.append(f"missing source summary: {source_path}")

        blob = "\n".join(item.get("preserved_interpretation", []) + item.get("recommendations", [])).lower()
        for prohibited in ("fork is certified", "fork is compliant", "production ready", "authority transferred"):
            if prohibited in blob:
                errors.append(f"prohibited authority or sufficiency upgrade: {prohibited}")

        results.append(
            {
                "path": path.relative_to(root).as_posix(),
                "observation_id": item.get("observation_id"),
                "passed": not errors,
                "errors": errors,
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
                "Round 006 observations satisfy the bounded observation schema",
                "source-summary paths are present",
                "authority and endorsement remain explicitly untransferred",
            ],
            "does_not_prove": [
                "reviewer endorsement",
                "external citation relevance",
                "repository implementation correctness",
                "the CSH hypothesis",
                "production readiness",
            ],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    result = evaluate(repo_root(args.root))
    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for item in result["results"]:
            print(f"[{'PASS' if item['passed'] else 'FAIL'}] {item['observation_id']}")
        print("ROUND006_OBSERVATIONS_PASS" if result["failed"] == 0 else "ROUND006_OBSERVATIONS_FAIL")
    return 1 if result["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
