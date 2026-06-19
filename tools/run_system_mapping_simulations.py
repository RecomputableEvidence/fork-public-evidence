#!/usr/bin/env python3
"""Run synthetic SYSTEM_MAPPING_RECORD simulations.

The harness records structural simulation outcomes only. It does not approve,
certify, authorize, or evaluate truth, compliance, safety, or readiness.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
RECEIPT_CHECKER = REPO_ROOT / "tools" / "check_system_mapping_receipt.py"
DEFAULT_MANIFEST = REPO_ROOT / "examples" / "system_mapping_simulations" / "manifest_v0_1.json"

SIMULATION_RECORDED = "SIMULATION_MAPPING_RECORDED"
SIMULATION_EXPANSION_GAP = "SIMULATION_EXPANSION_GAP_RECORDED"
SIMULATION_NON_CLAIM_DROP = "SIMULATION_NON_CLAIM_DROP_RECORDED"
SIMULATION_UNRESOLVED_POINTER_GAP = "SIMULATION_UNRESOLVED_POINTER_GAP_RECORDED"
SIMULATION_EXPECTATION_MISMATCH = "SIMULATION_EXPECTATION_MISMATCH_RECORDED"
SIMULATION_INPUT_GAP = "SIMULATION_INPUT_GAP_RECORDED"

CHECKER_TO_SIMULATION = {
    "STRUCTURAL_MAPPING_RECORDED": SIMULATION_RECORDED,
    "STRUCTURAL_MAPPING_PROVISIONAL_RECORDED": SIMULATION_RECORDED,
    "EXPANSION_AUTHORITY_GAP_RECORDED": SIMULATION_EXPANSION_GAP,
    "NON_CLAIM_DROP_RECORDED": SIMULATION_NON_CLAIM_DROP,
    "UNRESOLVED_POINTER_MAPPING_GAP_RECORDED": SIMULATION_UNRESOLVED_POINTER_GAP,
    "MAPPING_INCOMPLETE_RECORDED": SIMULATION_INPUT_GAP,
}

DO_NOT_MAP_TO = [
    "APPROVAL",
    "AUTHORIZATION",
    "COMPLIANCE",
    "CONTROL_EFFECTIVENESS",
    "DEPLOYMENT_READINESS",
    "LEGAL_SUFFICIENCY",
    "RISK_ACCEPTANCE",
    "SAFETY",
    "TRUTH",
    "WAIVER_APPROVAL",
]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def run_receipt_checker(receipt: dict[str, Any]) -> dict[str, Any]:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as handle:
        json.dump(receipt, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
        temp_path = Path(handle.name)

    try:
        result = subprocess.run(
            [sys.executable, str(RECEIPT_CHECKER), str(temp_path)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
    finally:
        temp_path.unlink(missing_ok=True)

    if not result.stdout:
        return {
            "result_kind": SIMULATION_INPUT_GAP,
            "checker_output": {},
            "errors": [
                {
                    "code": "RECEIPT_CHECKER_NO_OUTPUT",
                    "message": result.stderr,
                }
            ],
        }

    checker_output = json.loads(result.stdout)
    checker_kind = checker_output["result"]["result_kind"]
    simulation_kind = CHECKER_TO_SIMULATION.get(checker_kind, SIMULATION_INPUT_GAP)

    return {
        "result_kind": simulation_kind,
        "checker_result_kind": checker_kind,
        "checker_output": checker_output,
        "errors": checker_output.get("errors", []),
    }


def evaluate_simulation(path: Path) -> dict[str, Any]:
    payload = load_json(path)

    required = [
        "simulation_id",
        "simulation_version",
        "simulation_class",
        "expected_result_kind",
        "downstream_mapping_receipt",
        "market_system_analogue",
    ]

    missing = [key for key in required if key not in payload]
    if missing:
        return {
            "simulation_id": payload.get("simulation_id", str(path)),
            "simulation_class": payload.get("simulation_class", "UNKNOWN"),
            "path": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
            "result_kind": SIMULATION_INPUT_GAP,
            "expected_result_kind": payload.get("expected_result_kind"),
            "expectation_recorded": False,
            "errors": [{"code": "SIMULATION_REQUIRED_FIELD_MISSING", "message": ",".join(missing)}],
        }

    receipt_result = run_receipt_checker(payload["downstream_mapping_receipt"])
    result_kind = receipt_result["result_kind"]
    expected = payload["expected_result_kind"]

    expectation_recorded = result_kind == expected
    if not expectation_recorded:
        result_kind = SIMULATION_EXPECTATION_MISMATCH

    return {
        "simulation_id": payload["simulation_id"],
        "simulation_class": payload["simulation_class"],
        "path": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "result_kind": result_kind,
        "observed_result_kind": receipt_result["result_kind"],
        "expected_result_kind": expected,
        "checker_result_kind": receipt_result.get("checker_result_kind"),
        "expectation_recorded": expectation_recorded,
        "market_system_analogue": payload["market_system_analogue"],
        "errors": receipt_result["errors"],
    }


def load_manifest_paths(manifest_path: Path) -> list[Path]:
    manifest = load_json(manifest_path)
    paths = []
    for entry in manifest.get("simulations", []):
        paths.append(REPO_ROOT / entry["path"])
    return paths


def build_output(manifest_path: Path) -> dict[str, Any]:
    results = [evaluate_simulation(path) for path in load_manifest_paths(manifest_path)]
    all_expectations_recorded = all(result["expectation_recorded"] for result in results)

    return {
        "runner": {
            "runner_id": "SYSTEM_MAPPING_RECORD_SIMULATION_HARNESS",
            "runner_version": "0.1",
            "manifest_ref": str(manifest_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        },
        "result": {
            "result_kind": SIMULATION_RECORDED if all_expectations_recorded else SIMULATION_EXPECTATION_MISMATCH,
            "decision_boundary": "NON_DECISIONAL_SYNTHETIC_SIMULATION_RECORD_ONLY",
            "safe_to_automate_decisions": False,
            "requires_human_interpretation_before_any_automation": True,
        },
        "limitations": {
            "synthetic_fixtures_only": True,
            "does_not_represent_real_vendor_behavior": True,
            "does_not_validate_market_system_compliance": True,
            "does_not_validate_truth": True,
            "does_not_validate_safety": True,
            "does_not_validate_approval": True,
            "does_not_validate_authorization": True,
            "do_not_map_to": DO_NOT_MAP_TO,
        },
        "simulation_results": results,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run SYSTEM_MAPPING_RECORD synthetic simulations.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args(argv)

    output = build_output(args.manifest)

    if args.compact:
        print(json.dumps(output, sort_keys=True, separators=(",", ":")))
    else:
        print(json.dumps(output, indent=2, sort_keys=True))

    return 0 if output["result"]["result_kind"] == SIMULATION_RECORDED else 1


if __name__ == "__main__":
    sys.exit(main())
