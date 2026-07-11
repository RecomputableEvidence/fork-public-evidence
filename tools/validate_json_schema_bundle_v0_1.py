#!/usr/bin/env python3
"""Mechanically exercise applicable Fork JSON Schemas against governed artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:
    raise SystemExit("Install jsonschema: python -m pip install jsonschema") from exc


def repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists() and (candidate / "README.md").exists():
            return candidate
    raise RuntimeError("Repository root not found")


def load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_pair(root: Path, schema_path: Path, artifact_path: Path) -> dict[str, Any]:
    schema = load(root / schema_path)
    artifact = load(root / artifact_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [
        {
            "path": "/".join(str(part) for part in error.absolute_path) or "<root>",
            "message": error.message,
        }
        for error in sorted(
            validator.iter_errors(artifact),
            key=lambda error: list(error.absolute_path),
        )
    ]
    return {
        "schema": schema_path.as_posix(),
        "artifact": artifact_path.as_posix(),
        "passed": not errors,
        "errors": errors,
    }


def glob_pairs(root: Path, schema: str, pattern: str) -> Iterable[tuple[Path, Path]]:
    for path in sorted(root.glob(pattern)):
        yield Path(schema), path.relative_to(root)


def evaluate(root: Path) -> dict[str, Any]:
    pairs: list[tuple[Path, Path]] = [
        (
            Path("schemas/longitudinal_reconstruction_day0_packet_manifest_v0_1.schema.json"),
            Path("docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/packet_manifest.json"),
        ),
        (
            Path("schemas/longitudinal_day0_temporal_replay_receipt_v0_1.schema.json"),
            Path("docs/reconstruction/longitudinal/day0/replay/DAY0_TEMPORAL_REPLAY_RECEIPT_v0_1.json"),
        ),
        (
            Path("schemas/fork_proof_surface_state_v0_1.schema.json"),
            Path("docs/state/FORK_PROOF_SURFACE_STATE_v0_1.json"),
        ),
        (
            Path("schemas/cross_system_claim_handoff_manifest_v0_1.schema.json"),
            Path("docs/experiments/cross-system-claim-handoff-v0.1/EXPERIMENT_MANIFEST_v0_1.json"),
        ),
        (
            Path("schemas/cross_system_claim_handoff_corpus_freeze_v0_1.schema.json"),
            Path("docs/experiments/cross-system-claim-handoff-v0.1/CORPUS_FREEZE_v0_1.json"),
        ),
        (
            Path("schemas/cross_system_claim_handoff_system_registry_v0_1.schema.json"),
            Path("docs/experiments/cross-system-claim-handoff-v0.1/SYSTEM_REGISTRY_v0_1.json"),
        ),
        (
            Path("schemas/unsupported_inheritance_classifier_input_v0_1.schema.json"),
            Path("tests/fixtures/csh/classifier_input_clean.json"),
        ),
        (
            Path("schemas/unsupported_inheritance_classifier_input_v0_1.schema.json"),
            Path("tests/fixtures/csh/classifier_input_unsupported.json"),
        ),
    ]

    # ASI_SCHEMA_BUNDLE_START
    pairs.extend([
        (
            Path("schemas/validity_state_transition_event_v0_1.schema.json"),
            Path("tests/fixtures/authority-state-invariance/schema-samples/validity_state_transition_event.json"),
        ),
        (
            Path("schemas/authority_transition_event_v0_1.schema.json"),
            Path("tests/fixtures/authority-state-invariance/schema-samples/authority_transition_event.json"),
        ),
        (
            Path("schemas/reliance_event_v0_1.schema.json"),
            Path("tests/fixtures/authority-state-invariance/schema-samples/reliance_event.json"),
        ),
        (
            Path("schemas/reliance_authority_misalignment_event_v0_1.schema.json"),
            Path("tests/fixtures/authority-state-invariance/schema-samples/reliance_authority_misalignment_event.json"),
        ),
    ])
    # ASI_SCHEMA_BUNDLE_END
    pairs.extend(
        glob_pairs(
            root,
            "schemas/reviewer_access_path_observation_v0_1.schema.json",
            "docs/recomputation/boundary-state-interop-v0.1.2/fixtures/**/*.json",
        )
    )
    pairs.extend(
        glob_pairs(
            root,
            "schemas/public_review_round_006_observation_v0_1.schema.json",
            "docs/review/public-rounds/round-006/observations/*.json",
        )
    )
    pairs.extend(
        glob_pairs(
            root,
            "schemas/cross_system_claim_handoff_scenario_v0_1.schema.json",
            "docs/experiments/cross-system-claim-handoff-v0.1/corpus/SIM_*.json",
        )
    )
    pairs.extend(
        glob_pairs(
            root,
            "schemas/cross_system_claim_handoff_run_v0_1.schema.json",
            "docs/experiments/cross-system-claim-handoff-v0.1/runs/**/*.json",
        )
    )
    pairs.extend(
        glob_pairs(
            root,
            "schemas/cross_system_claim_handoff_result_v0_1.schema.json",
            "docs/experiments/cross-system-claim-handoff-v0.1/results/**/*.json",
        )
    )

    results = []
    for schema_path, artifact_path in pairs:
        if not (root / schema_path).exists():
            results.append(
                {
                    "schema": schema_path.as_posix(),
                    "artifact": artifact_path.as_posix(),
                    "passed": False,
                    "errors": [{"path": "<schema>", "message": "schema file missing"}],
                }
            )
        elif not (root / artifact_path).exists():
            results.append(
                {
                    "schema": schema_path.as_posix(),
                    "artifact": artifact_path.as_posix(),
                    "passed": False,
                    "errors": [{"path": "<artifact>", "message": "artifact file missing"}],
                }
            )
        else:
            results.append(validate_pair(root, schema_path, artifact_path))

    failed = [result for result in results if not result["passed"]]
    return {
        "checker": Path(__file__).name,
        "total": len(results),
        "passed": len(results) - len(failed),
        "failed": len(failed),
        "results": results,
        "interpretation": {
            "proves": [
                "listed governed JSON artifacts satisfy the listed JSON Schemas",
                "the schemas themselves are valid Draft 2020-12 schemas",
            ],
            "does_not_prove": [
                "semantic truth",
                "evidence sufficiency",
                "compliance",
                "legal sufficiency",
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
    result = evaluate(repo_root(args.root))
    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for item in result["results"]:
            print(
                f"[{'PASS' if item['passed'] else 'FAIL'}] "
                f"{item['artifact']} <- {item['schema']}"
            )
        print("SCHEMA_BUNDLE_PASS" if result["failed"] == 0 else "SCHEMA_BUNDLE_FAIL")
    return 1 if result["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
