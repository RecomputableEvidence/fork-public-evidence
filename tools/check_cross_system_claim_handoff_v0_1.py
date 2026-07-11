#!/usr/bin/env python3
"""Validate the CSH v0.1 preregistered scaffold and, optionally, baseline completeness."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:
    raise SystemExit("Install jsonschema: python -m pip install jsonschema") from exc

BASE = Path("docs/experiments/cross-system-claim-handoff-v0.1")
MANIFEST = BASE / "EXPERIMENT_MANIFEST_v0_1.json"
FREEZE = BASE / "CORPUS_FREEZE_v0_1.json"
REGISTRY = BASE / "SYSTEM_REGISTRY_v0_1.json"
PREREG = BASE / "PREREGISTRATION_v0_1.md"
ANCHOR = BASE / "EXPERIMENT_RELEASE_ANCHOR_v0_1.json"
CORPUS = BASE / "corpus"
RUNS = BASE / "runs"
RESULTS = BASE / "results"

SCHEMAS = {
    "manifest": Path("schemas/cross_system_claim_handoff_manifest_v0_1.schema.json"),
    "scenario": Path("schemas/cross_system_claim_handoff_scenario_v0_1.schema.json"),
    "freeze": Path("schemas/cross_system_claim_handoff_corpus_freeze_v0_1.schema.json"),
    "registry": Path("schemas/cross_system_claim_handoff_system_registry_v0_1.schema.json"),
    "run": Path("schemas/cross_system_claim_handoff_run_v0_1.schema.json"),
    "result": Path("schemas/cross_system_claim_handoff_result_v0_1.schema.json"),
}

HYPOTHESIS = "E[U | H = 1] < E[U | H = 0]"
EXPECTED_SCENARIOS = {
    "SIM_A_BOUNDARY_PRESERVED",
    "SIM_B_BOUNDARY_NARROWED",
    "SIM_C_NON_CLAIM_DROPPED",
    "SIM_D_EXPANSION_WITHOUT_AUTHORITY",
    "SIM_F_POINTER_UNRESOLVED",
    "SIM_H_CASCADING_INHERITANCE",
}


def repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists() and (candidate / "README.md").exists():
            return candidate
    raise RuntimeError("Repository root not found")


def load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def schema_errors(instance: Any, schema: Any) -> list[str]:
    return [
        f"{'/'.join(str(p) for p in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(instance),
            key=lambda error: list(error.absolute_path),
        )
    ]


def evaluate(root: Path, require_complete_baseline: bool = False) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def record(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": passed, "detail": detail})

    schemas = {}
    for name, path in SCHEMAS.items():
        try:
            schema = load(root / path)
            Draft202012Validator.check_schema(schema)
            schemas[name] = schema
            record(f"schema_{name}_valid", True, path.as_posix())
        except Exception as exc:
            record(f"schema_{name}_valid", False, str(exc))

    required_files = [
        BASE / "README.md",
        PREREG,
        BASE / "METHOD_v0_1.md",
        MANIFEST,
        FREEZE,
        REGISTRY,
        BASE / "AMENDMENT_REGISTER_v0_1.json",
        ANCHOR,
    ]
    missing = [path.as_posix() for path in required_files if not (root / path).exists()]
    record("required_experiment_artifacts", not missing, "present" if not missing else "; ".join(missing))

    if missing or len(schemas) != len(SCHEMAS):
        return finish(checks, require_complete_baseline)

    manifest = load(root / MANIFEST)
    errors = schema_errors(manifest, schemas["manifest"])
    record("manifest_schema", not errors, "valid" if not errors else "; ".join(errors))

    prereg_text = (root / PREREG).read_text(encoding="utf-8")
    readme_text = (root / BASE / "README.md").read_text(encoding="utf-8")
    record("hypothesis_preregistration_sync", HYPOTHESIS in prereg_text, HYPOTHESIS)
    record("hypothesis_readme_sync", HYPOTHESIS in readme_text, HYPOTHESIS)
    record(
        "manifest_hypothesis_sync",
        manifest.get("hypothesis", {}).get("expression") == HYPOTHESIS,
        manifest.get("hypothesis", {}).get("expression", "<missing>"),
    )

    scenario_paths = sorted((root / CORPUS).glob("SIM_*.json"))
    scenario_ids = set()
    scenario_failures = []
    for path in scenario_paths:
        scenario = load(path)
        errors = schema_errors(scenario, schemas["scenario"])
        if errors:
            scenario_failures.append(f"{path.name}: {'; '.join(errors)}")
        scenario_ids.add(scenario.get("scenario_id"))
    record(
        "scenario_schema_and_set",
        not scenario_failures and scenario_ids == EXPECTED_SCENARIOS,
        "six preregistered scenario descriptors"
        if not scenario_failures and scenario_ids == EXPECTED_SCENARIOS
        else "; ".join(scenario_failures + [f"observed={sorted(scenario_ids)}"]),
    )
    record(
        "manifest_scenario_sync",
        set(manifest.get("scenario_ids", [])) == EXPECTED_SCENARIOS,
        "manifest scenario IDs match preregistration",
    )

    freeze = load(root / FREEZE)
    errors = schema_errors(freeze, schemas["freeze"])
    record("freeze_schema", not errors, "valid" if not errors else "; ".join(errors))
    if freeze.get("freeze_status") == "draft_unfrozen":
        record(
            "unfrozen_baseline_blocked",
            freeze.get("baseline_execution_permitted") is False
            and bool(freeze.get("blocking_unresolved_items")),
            "draft freeze blocks receiver execution",
        )
    else:
        bound_paths = [entry["path"] for group in ("scenario_artifacts","prompt_artifacts","handoff_artifacts","schema_artifacts","checker_artifacts") for entry in freeze.get(group, [])]
        digest_errors = []
        for group in ("scenario_artifacts","prompt_artifacts","handoff_artifacts","schema_artifacts","checker_artifacts"):
            for entry in freeze.get(group, []):
                path = root / entry["path"]
                if not path.exists() or sha256(path) != entry["sha256"]:
                    digest_errors.append(entry["path"])
        record("frozen_artifact_digests", not digest_errors and bool(bound_paths), "verified" if not digest_errors else "; ".join(digest_errors))

    registry = load(root / REGISTRY)
    errors = schema_errors(registry, schemas["registry"])
    record("system_registry_schema", not errors, "valid" if not errors else "; ".join(errors))
    if registry.get("registry_status") == "frozen":
        registry_blob = json.dumps(registry)
        record("frozen_registry_has_no_unassigned_values", "UNASSIGNED" not in registry_blob, "all receiver fields assigned")

    run_paths = sorted((root / RUNS).rglob("*.json")) if (root / RUNS).exists() else []
    result_paths = sorted((root / RESULTS).rglob("*.json")) if (root / RESULTS).exists() else []
    run_errors = []
    run_keys = set()
    terminal = 0
    for path in run_paths:
        item = load(path)
        errors = schema_errors(item, schemas["run"])
        if errors:
            run_errors.append(f"{path.relative_to(root)}: {'; '.join(errors)}")
        key = (
            item.get("scenario_id"),
            item.get("condition"),
            item.get("receiver_class_id"),
            item.get("replicate_id"),
        )
        if key in run_keys:
            run_errors.append(f"duplicate experimental unit: {key}")
        run_keys.add(key)
        if item.get("terminal_disposition") != "not_started":
            terminal += 1
    record("run_records_schema_and_unique_units", not run_errors, "valid" if not run_errors else "; ".join(run_errors))

    result_errors = []
    for path in result_paths:
        item = load(path)
        errors = schema_errors(item, schemas["result"])
        if errors:
            result_errors.append(f"{path.relative_to(root)}: {'; '.join(errors)}")
    record("result_records_schema", not result_errors, "valid" if not result_errors else "; ".join(result_errors))

    if manifest.get("baseline_run_status") == "not_started":
        record("not_started_has_no_terminal_runs", terminal == 0, f"terminal runs={terminal}")

    if require_complete_baseline:
        record("complete_baseline_unit_count", len(run_keys) == 108 and terminal == 108, f"unique units={len(run_keys)}, terminal={terminal}")
        record("complete_baseline_manifest_status", manifest.get("baseline_run_status") == "complete", str(manifest.get("baseline_run_status")))
        record("complete_baseline_frozen", freeze.get("freeze_status") == "frozen", str(freeze.get("freeze_status")))

    return finish(checks, require_complete_baseline)


def finish(checks: list[dict[str, Any]], require_complete_baseline: bool) -> dict[str, Any]:
    failed = [check for check in checks if not check["passed"]]
    return {
        "checker": Path(__file__).name,
        "mode": "complete_baseline" if require_complete_baseline else "scaffold_and_available_records",
        "total": len(checks),
        "passed": len(checks) - len(failed),
        "failed": len(failed),
        "checks": checks,
        "interpretation": {
            "proves": [
                "the preregistered CSH scaffold and available records satisfy bounded structural checks",
                "the hypothesis is synchronized across preregistration, manifest, and experiment README",
                "the unfrozen scaffold blocks baseline execution",
            ],
            "does_not_prove": [
                "that the baseline has run unless complete-baseline mode passes",
                "that Fork reduces unsupported inheritance",
                "truth",
                "compliance",
                "legal sufficiency",
                "production readiness",
                "institutional authority",
            ],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--require-complete-baseline", action="store_true")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    result = evaluate(repo_root(args.root), args.require_complete_baseline)
    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for check in result["checks"]:
            print(f"[{'PASS' if check['passed'] else 'FAIL'}] {check['name']}: {check['detail']}")
        print("CSH_CHECK_PASS" if result["failed"] == 0 else "CSH_CHECK_FAIL")
    return 1 if result["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
