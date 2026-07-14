#!/usr/bin/env python3
"""Validate the Corpus 001 source-selection ledger and admission invariants."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

import jsonschema
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_DEFAULT = REPO_ROOT / (
    "manifests/experiment-meta-evidence/corpus-001/"
    "FORK_META_EVIDENCE_CORPUS_001_SOURCE_SELECTION_LEDGER_v0_1.json"
)
DIGEST_DEFAULT = LEDGER_DEFAULT.with_suffix(".jcs.sha256")
LEDGER_SCHEMA_PATH = (
    REPO_ROOT / "schemas/corpus_source_selection_ledger_v0_1.schema.json"
)
SOURCE_SCHEMA_PATH = (
    REPO_ROOT / "schemas/corpus_source_artifact_record_v0_1.schema.json"
)
TRANSITION_SCHEMA_PATH = (
    REPO_ROOT / "schemas/corpus_admission_transition_v0_1.schema.json"
)
CANONICALIZER_PATH = (
    REPO_ROOT / "tools/canonicalize_corpus_source_selection_ledger_v0_1.py"
)

EXPECTED = {
    "OBS-001": "FAVORABLE",
    "OBS-002": "UNFAVORABLE",
    "OBS-003": "MIXED",
    "OBS-004": "NULL",
    "OBS-005": "AMBIGUOUS",
    "OBS-006": "CORRECTED",
}
FROZEN_OR_LATER = {
    "ADMISSION_FROZEN",
    "RECORDS_INSTANTIATED",
    "INTERNAL_DRY_RUN_COMPLETE",
    "REVIEW_PACKET_FROZEN",
    "INDEPENDENT_REVIEW_IN_PROGRESS",
}
ABSOLUTE_PATH_PATTERNS = [
    re.compile(r"[A-Za-z]:[\\/]+"),
    re.compile(r"\\\\[A-Za-z0-9._-]+[\\/]"),
    re.compile(r"/Users/"),
    re.compile(r"/home/"),
    re.compile(r"file://", re.IGNORECASE),
]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def json_pointer(error: jsonschema.ValidationError) -> str:
    if not error.absolute_path:
        return "/"
    return "/" + "/".join(str(item) for item in error.absolute_path)


def walk_strings(value: Any, pointer: str = ""):
    if isinstance(value, str):
        yield pointer or "/", value
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from walk_strings(item, f"{pointer}/{index}")
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from walk_strings(item, f"{pointer}/{key}")


def verify_detached_digest(
    canonicalizer: Any,
    ledger: Any,
    digest_path: Path,
) -> tuple[bool, str, str | None]:
    canonical = canonicalizer.canonicalize_bytes(ledger)
    actual = canonicalizer.digest_bytes(canonical)
    expected = canonicalizer.read_expected_digest(digest_path)
    return actual == expected, actual, expected


def check_ledger(ledger_path: Path, digest_path: Path) -> dict[str, Any]:
    defects: list[dict[str, Any]] = []
    canonicalizer = load_module(
        CANONICALIZER_PATH,
        "corpus_001_canonicalizer",
    )

    try:
        ledger = canonicalizer.load_json_strict(ledger_path)
    except Exception as exc:
        return {
            "checker": "check_corpus_source_selection_ledger_v0_1.py",
            "defect_count": 1,
            "defects": [
                {
                    "code": "LEDGER_PARSE_FAILED",
                    "detail": str(exc),
                }
            ],
            "state": "NON_CONFORMING",
        }

    ledger_schema = json.loads(
        LEDGER_SCHEMA_PATH.read_text(encoding="utf-8")
    )
    source_schema = json.loads(
        SOURCE_SCHEMA_PATH.read_text(encoding="utf-8")
    )
    transition_schema = json.loads(
        TRANSITION_SCHEMA_PATH.read_text(encoding="utf-8")
    )

    registry = Registry().with_resources(
        [
            (
                source_schema["$id"],
                Resource.from_contents(
                    source_schema,
                    default_specification=DRAFT202012,
                ),
            ),
            (
                transition_schema["$id"],
                Resource.from_contents(
                    transition_schema,
                    default_specification=DRAFT202012,
                ),
            ),
        ]
    )
    validator = jsonschema.Draft202012Validator(
        ledger_schema,
        registry=registry,
        format_checker=jsonschema.FormatChecker(),
    )

    for error in sorted(
        validator.iter_errors(ledger),
        key=lambda item: tuple(
            str(component) for component in item.absolute_path
        ),
    ):
        defects.append(
            {
                "code": "SCHEMA_VALIDATION_FAILED",
                "path": json_pointer(error),
                "detail": error.message,
            }
        )

    observations = ledger.get("observations", [])
    by_id: dict[str, dict[str, Any]] = {}

    for observation in observations:
        observation_id = observation.get("observation_id")
        if observation_id in by_id:
            defects.append(
                {
                    "code": "DUPLICATE_OBSERVATION_ID",
                    "observation_id": observation_id,
                }
            )
        elif isinstance(observation_id, str):
            by_id[observation_id] = observation

    if set(by_id) != set(EXPECTED):
        defects.append(
            {
                "code": "OBSERVATION_SET_MISMATCH",
                "expected": sorted(EXPECTED),
                "actual": sorted(by_id),
            }
        )

    for observation_id, required_stratum in EXPECTED.items():
        observation = by_id.get(observation_id)
        if observation is None:
            continue

        if observation.get("required_stratum") != required_stratum:
            defects.append(
                {
                    "code": "STRATUM_MISMATCH",
                    "observation_id": observation_id,
                    "expected": required_stratum,
                    "actual": observation.get("required_stratum"),
                }
            )

        status = observation.get("selection_status")
        admitted = observation.get("admitted")
        source = observation.get("source", {})
        admission = observation.get("admission", {})
        disclosure = observation.get("disclosure", {})

        if admitted is True:
            required_source_fields = [
                "source_artifact_id",
                "canonical_private_locator",
                "source_media_type",
                "source_byte_length",
                "source_sha256",
                "acquired_at_utc",
                "acquired_by_actor_id",
                "source_temporal_status",
            ]
            missing = [
                field
                for field in required_source_fields
                if source.get(field) is None
            ]
            if status != "ADMITTED":
                defects.append(
                    {
                        "code": "ADMITTED_STATUS_MISMATCH",
                        "observation_id": observation_id,
                        "selection_status": status,
                    }
                )
            if missing:
                defects.append(
                    {
                        "code": "ADMITTED_SOURCE_METADATA_INCOMPLETE",
                        "observation_id": observation_id,
                        "missing_fields": missing,
                    }
                )
            if admission.get("eligibility_result") != "CONFIRMED":
                defects.append(
                    {
                        "code": "ADMITTED_WITHOUT_CONFIRMED_ELIGIBILITY",
                        "observation_id": observation_id,
                    }
                )
            if admission.get("decision_actor_id") is None or admission.get(
                "decision_at_utc"
            ) is None:
                defects.append(
                    {
                        "code": "ADMITTED_WITHOUT_DECISION_METADATA",
                        "observation_id": observation_id,
                    }
                )
            if disclosure.get("status") == "PENDING":
                defects.append(
                    {
                        "code": "ADMITTED_WITH_PENDING_DISCLOSURE",
                        "observation_id": observation_id,
                    }
                )

        authorization_flags = [
            disclosure.get("named_attribution_authorized"),
            disclosure.get("direct_quotation_authorized"),
            disclosure.get("public_excerpt_authorized"),
        ]
        if any(flag is True for flag in authorization_flags):
            if disclosure.get("authorization_record_id") is None:
                defects.append(
                    {
                        "code": "AUTHORIZATION_FLAG_WITHOUT_RECORD",
                        "observation_id": observation_id,
                    }
                )

    obs4 = by_id.get("OBS-004")
    if obs4 is not None and ledger.get("ledger_status") == "DRAFT_SELECTION":
        if obs4.get("selection_status") != "OPEN_SLOT":
            defects.append(
                {
                    "code": "INITIAL_NULL_SLOT_NOT_OPEN",
                    "observation_id": "OBS-004",
                }
            )
        if obs4.get("admitted") is not False:
            defects.append(
                {
                    "code": "OPEN_NULL_SLOT_MARKED_ADMITTED",
                    "observation_id": "OBS-004",
                }
            )
        if obs4.get("source", {}).get("source_artifact_id") is not None:
            defects.append(
                {
                    "code": "OPEN_NULL_SLOT_HAS_SOURCE_ID",
                    "observation_id": "OBS-004",
                }
            )
        if not obs4.get("open_slot_reason"):
            defects.append(
                {
                    "code": "OPEN_NULL_SLOT_REASON_MISSING",
                    "observation_id": "OBS-004",
                }
            )

    if ledger.get("ledger_status") in FROZEN_OR_LATER:
        open_slots = [
            observation.get("observation_id")
            for observation in observations
            if observation.get("selection_status") == "OPEN_SLOT"
        ]
        not_admitted = [
            observation.get("observation_id")
            for observation in observations
            if observation.get("admitted") is not True
        ]
        if open_slots:
            defects.append(
                {
                    "code": "ADMISSION_FREEZE_BLOCKED_BY_OPEN_SLOT",
                    "observation_ids": open_slots,
                }
            )
        if not_admitted:
            defects.append(
                {
                    "code": "ADMISSION_FREEZE_REQUIRES_ALL_STRATA_ADMITTED",
                    "observation_ids": not_admitted,
                }
            )

    for pointer, value in walk_strings(ledger):
        for pattern in ABSOLUTE_PATH_PATTERNS:
            if pattern.search(value):
                defects.append(
                    {
                        "code": "ABSOLUTE_PRIVATE_PATH_DISCLOSED",
                        "path": pointer,
                    }
                )
                break

    digest_state = "NOT_CHECKED"
    digest_sha256 = None

    try:
        valid_digest, digest_sha256, _ = verify_detached_digest(
            canonicalizer,
            ledger,
            digest_path,
        )
        digest_state = "PASS" if valid_digest else "FAIL"
        if not valid_digest:
            defects.append(
                {
                    "code": "DETACHED_LEDGER_DIGEST_MISMATCH",
                    "actual_sha256": digest_sha256,
                }
            )
    except Exception as exc:
        digest_state = "FAIL"
        defects.append(
            {
                "code": "DETACHED_LEDGER_DIGEST_CHECK_FAILED",
                "detail": str(exc),
            }
        )

    return {
        "checker": "check_corpus_source_selection_ledger_v0_1.py",
        "ledger_id": ledger.get("ledger_id"),
        "ledger_status": ledger.get("ledger_status"),
        "observation_count": len(observations),
        "detached_digest_state": digest_state,
        "ledger_jcs_sha256": digest_sha256,
        "defect_count": len(defects),
        "defects": defects,
        "state": "CONFORMING" if not defects else "NON_CONFORMING",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("ledger", type=Path, nargs="?", default=LEDGER_DEFAULT)
    parser.add_argument("--digest", type=Path, default=DIGEST_DEFAULT)
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = check_ledger(args.ledger, args.digest)

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            f"{result['state']}: "
            f"{result['observation_count']} observations, "
            f"{result['defect_count']} defects"
        )

    return 0 if result["state"] == "CONFORMING" else 1


if __name__ == "__main__":
    sys.exit(main())