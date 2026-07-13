from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

BASE = Path("docs/experiments/cross-system-claim-handoff-v0.1")
AMENDMENT_DIR = BASE / "amendments" / "CSH-AMEND-002"
SEAL = AMENDMENT_DIR / "ORIGINAL_ATTEMPT_SEAL_v0_1_1.json"
AMENDMENT = AMENDMENT_DIR / "CSH-AMEND-002_v0_1_1.json"
IDENTITY = AMENDMENT_DIR / "V0_1_FREEZE_BYTE_IDENTITY_REPORT_v0_1_1.json"
STATE = BASE / "execution-state" / "PAIR-001_EXECUTION_STATE_v0_1_1.json"
SCHEMA = Path("schemas/cross_system_claim_handoff_execution_state_v0_1_1.schema.json")
INSTRUMENTATION_FREEZE = AMENDMENT_DIR / "INSTRUMENTATION_FREEZE_v0_1_1.json"
RESULT_JSON = BASE / "results" / "bounded-rounds" / "CSH_PAIR001_REPAIR_REPETITION_BOUNDED_RESULT_v0_1_1.json"

ORIGINAL_IDS = {"CSH-RUN-001", "CSH-RUN-002"}
REQUIRED_ATTEMPT_FILES = {"exact-request.json", "execution-metadata.json", "raw-provider-response.json"}


def repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists() and (candidate / "README.md").exists():
            return candidate
    raise RuntimeError("Repository root not found")


def load(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def schema_errors(instance: Any, schema: Any) -> list[str]:
    return [
        f"{'/'.join(str(item) for item in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema, format_checker=None).iter_errors(instance),
            key=lambda item: list(item.absolute_path),
        )
    ]


def semantic_errors(state: dict[str, Any], seal: dict[str, Any], instrumentation_freeze: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    originals = state.get("original_attempts", [])
    original_ids = {item.get("run_id") for item in originals}
    if original_ids != ORIGINAL_IDS:
        errors.append(f"original IDs must be {sorted(ORIGINAL_IDS)}; observed={sorted(str(x) for x in original_ids)}")
    for item in originals:
        if item.get("role") != "original_affected_attempt":
            errors.append(f"{item.get('run_id')}: original role changed")
        if item.get("immutable") is not True:
            errors.append(f"{item.get('run_id')}: original attempt must remain immutable")
        if item.get("replaced") is not False or item.get("superseded") is not False:
            errors.append(f"{item.get('run_id')}: original attempt cannot be replaced or superseded")
        if item.get("linked_original_run_id") is not None:
            errors.append(f"{item.get('run_id')}: original attempt cannot link to another original")

    repeats = state.get("repeat_runs", [])
    repeat_ids = [item.get("run_id") for item in repeats]
    if len(repeat_ids) != len(set(repeat_ids)):
        errors.append("repeat run IDs must be unique")
    if ORIGINAL_IDS.intersection(set(repeat_ids)):
        errors.append("repeat run IDs must not reuse original run IDs")
    for item in repeats:
        linked = item.get("linked_original_run_id")
        if linked not in ORIGINAL_IDS:
            errors.append(f"{item.get('run_id')}: linked_original_run_id must reference an original attempt")
        if item.get("role") != "post_repair_repetition":
            errors.append(f"{item.get('run_id')}: repeat role must be post_repair_repetition")
        if item.get("replaced") is not False or item.get("superseded") is not False:
            errors.append(f"{item.get('run_id')}: repeat cannot replace or supersede another attempt")

    transition_ids = [item.get("transition_id") for item in state.get("transitions", [])]
    if len(transition_ids) != len(set(transition_ids)):
        errors.append("transition IDs must be unique")

    seal_ids = {item.get("run_id") for item in seal.get("attempts", [])}
    if seal_ids != ORIGINAL_IDS:
        errors.append("seal must bind exactly the two original run IDs")

    if instrumentation_freeze is not None:
        immutable_paths = {item.get("path") for item in instrumentation_freeze.get("immutable_artifacts", [])}
        if STATE.as_posix() in immutable_paths:
            errors.append("mutable execution-state artifact must not be listed as immutable in instrumentation freeze")
        mutable_paths = {item.get("path") for item in instrumentation_freeze.get("mutable_artifacts", [])}
        if STATE.as_posix() not in mutable_paths:
            errors.append("instrumentation freeze must declare the execution-state artifact as mutable")

    return errors


def verify_artifact_records(root: Path, records: list[dict[str, Any]], label: str) -> list[str]:
    errors: list[str] = []
    for record in records:
        relative = record.get("path")
        expected = record.get("sha256")
        path = root / str(relative)
        if not path.is_file():
            errors.append(f"{label}: missing {relative}")
            continue
        actual = sha256(path)
        if actual != expected:
            errors.append(f"{label}: digest mismatch {relative}: expected={expected} actual={actual}")
        size = record.get("size_bytes")
        if size is not None and path.stat().st_size != size:
            errors.append(f"{label}: size mismatch {relative}")
    return errors


def evaluate(root: Path, require_repeat: bool = False, require_result: bool = False) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def record(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": passed, "detail": detail})

    required = [SCHEMA, SEAL, AMENDMENT, IDENTITY, STATE, INSTRUMENTATION_FREEZE]
    missing = [path.as_posix() for path in required if not (root / path).is_file()]
    record("required_surface", not missing, "present" if not missing else "; ".join(missing))
    if missing:
        return finish(checks)

    schema = load(root / SCHEMA)
    try:
        Draft202012Validator.check_schema(schema)
        record("execution_state_schema_valid", True, SCHEMA.as_posix())
    except Exception as exc:
        record("execution_state_schema_valid", False, str(exc))
        return finish(checks)

    state = load(root / STATE)
    errors = schema_errors(state, schema)
    record("execution_state_schema_conformance", not errors, "valid" if not errors else "; ".join(errors))

    seal = load(root / SEAL)
    amendment = load(root / AMENDMENT)
    identity = load(root / IDENTITY)
    instrumentation_freeze = load(root / INSTRUMENTATION_FREEZE)

    amendment_ok = (
        amendment.get("amendment_id") == "CSH-AMEND-002"
        and amendment.get("amendment_class") == "instrumentation_repair"
        and amendment.get("status") == "final"
        and set(amendment.get("affected_original_run_ids", [])) == ORIGINAL_IDS
        and amendment.get("scope_constraints", {}).get("mutates_v0_1_freeze") is False
        and amendment.get("scope_constraints", {}).get("replaces_original_attempts") is False
    )
    record("amendment_scope", amendment_ok, "instrumentation-only final amendment" if amendment_ok else "amendment scope violation")

    semantic = semantic_errors(state, seal, instrumentation_freeze)
    record("execution_state_semantics", not semantic, "bounded" if not semantic else "; ".join(semantic))

    seal_records: list[dict[str, Any]] = []
    for attempt in seal.get("attempts", []):
        seal_records.extend(attempt.get("artifacts", []))
    seal_errors = verify_artifact_records(root, seal_records, "original seal")
    record("original_attempt_digests", not seal_errors, "verified" if not seal_errors else "; ".join(seal_errors))

    identity_errors = verify_artifact_records(root, identity.get("records", []), "v0.1 identity")
    record("v0_1_freeze_byte_identity", not identity_errors, "byte-identical" if not identity_errors else "; ".join(identity_errors))

    frozen_errors = verify_artifact_records(root, instrumentation_freeze.get("immutable_artifacts", []), "instrumentation freeze")
    record("instrumentation_freeze_digests", not frozen_errors, "verified" if not frozen_errors else "; ".join(frozen_errors))

    state_seal_ref = state.get("original_attempt_seal", {})
    seal_ref_ok = state_seal_ref.get("path") == SEAL.as_posix() and state_seal_ref.get("sha256") == sha256(root / SEAL)
    record("state_to_seal_binding", seal_ref_ok, "bound" if seal_ref_ok else "state seal reference mismatch")

    repeats = state.get("repeat_runs", [])
    repeat_errors: list[str] = []
    if require_repeat and len(repeats) != 2:
        repeat_errors.append(f"expected two repeat runs; observed={len(repeats)}")
    for repeat in repeats:
        directory = root / str(repeat.get("artifact_directory", ""))
        observed_names = {path.name for path in directory.iterdir()} if directory.is_dir() else set()
        missing_names = REQUIRED_ATTEMPT_FILES - observed_names
        if missing_names:
            repeat_errors.append(f"{repeat.get('run_id')}: missing {sorted(missing_names)}")
            continue
        linked = repeat.get("linked_original_run_id")
        original = next((item for item in state.get("original_attempts", []) if item.get("run_id") == linked), None)
        if original is None:
            repeat_errors.append(f"{repeat.get('run_id')}: linked original not found")
            continue
        original_exact = root / original["artifact_directory"] / "exact-request.json"
        repeat_exact = directory / "exact-request.json"
        if sha256(original_exact) != sha256(repeat_exact):
            repeat_errors.append(f"{repeat.get('run_id')}: exact request differs from linked original")
        repeat_errors.extend(verify_artifact_records(root, repeat.get("artifacts", []), f"repeat {repeat.get('run_id')}"))
    record("repeat_lineage", not repeat_errors, "verified" if not repeat_errors else "; ".join(repeat_errors))

    if (root / RESULT_JSON).is_file():
        result = load(root / RESULT_JSON)
        result_ok = (
            result.get("result_scope") == "execution_instrumentation_continuity_only"
            and set(result.get("original_run_ids", [])) == ORIGINAL_IDS
            and set(result.get("repeat_run_ids", [])) == {item.get("run_id") for item in repeats}
            and bool(result.get("non_claims"))
        )
        record("bounded_result", result_ok, "bounded" if result_ok else "result scope or lineage mismatch")
    else:
        record("bounded_result", not require_result, "not yet filed" if not require_result else "required bounded result missing")

    return finish(checks)


def finish(checks: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checks if not item["passed"]]
    return {
        "checker": Path(__file__).name,
        "checks": checks,
        "total": len(checks),
        "passed": len(checks) - len(failed),
        "failed": len(failed),
        "interpretation": {
            "proves": [
                "the listed original attempt bytes still match their preserved seal",
                "the listed v0.1 freeze artifacts remain byte-identical to the captured repair boundary",
                "mutable execution state is separated from the immutable semantic freeze",
                "new repeat identifiers do not replace original identifiers when repeat records are present",
            ],
            "does_not_prove": [
                "semantic truth",
                "the CSH hypothesis",
                "receiver correctness",
                "compliance",
                "legal sufficiency",
                "safety",
                "authorization",
                "approval",
                "certification",
                "production readiness",
                "institutional authority",
            ],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--require-repeat", action="store_true")
    parser.add_argument("--require-result", action="store_true")
    args = parser.parse_args()
    result = evaluate(
        repo_root(args.root),
        require_repeat=args.require_repeat,
        require_result=args.require_result,
    )
    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for item in result["checks"]:
            print(f"[{'PASS' if item['passed'] else 'FAIL'}] {item['name']}: {item['detail']}")
        print("CSH_EXECUTION_V0_1_1_PASS" if result["failed"] == 0 else "CSH_EXECUTION_V0_1_1_FAIL")
    return 1 if result["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
