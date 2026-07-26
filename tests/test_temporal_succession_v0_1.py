from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = REPO_ROOT / "tools/check_temporal_succession_v0_1.py"
spec = importlib.util.spec_from_file_location("temporal_succession_checker", CHECKER_PATH)
assert spec and spec.loader
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")


def copied_surface(parent: Path) -> Path:
    target = parent / "repo"
    ledger = json.loads((REPO_ROOT / checker.LEDGER_PATH).read_text(encoding="utf-8"))
    current = json.loads((REPO_ROOT / checker.CURRENT_PATH).read_text(encoding="utf-8"))
    paths = {
        checker.LEDGER_PATH.as_posix(),
        checker.CURRENT_PATH.as_posix(),
        checker.HISTORICAL_PATH.as_posix(),
        checker.AUDIT_PATH.as_posix(),
        "README.md",
        "docs/state/FORK_PROOF_SURFACE_STATE_SUMMARY_v0_1.md",
    }
    paths.update(item["path"] for item in ledger["records"])
    paths.update(item["source_path"] for item in ledger["admitted_state_changing_events"])
    paths.update(item["path"] for item in ledger["bounded_exterior_observations"])
    paths.update(item["path"] for item in current["source_bindings"])
    for relative in sorted(paths):
        source = REPO_ROOT / relative
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    return target


def test_exact_temporal_succession_surface_conforms() -> None:
    assert checker.check(REPO_ROOT) == []


def test_july_11_projection_remains_byte_identical() -> None:
    digest = hashlib.sha256((REPO_ROOT / checker.HISTORICAL_PATH).read_bytes()).hexdigest()
    assert digest == checker.HISTORICAL_SHA256


def test_duplicate_json_key_is_rejected() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = copied_surface(Path(directory))
        path = root / checker.LEDGER_PATH
        path.write_text('{"ledger_id":"first","ledger_id":"second"}\n', encoding="utf-8")
        errors = checker.check(root)
        assert any("duplicate JSON key" in error for error in errors)


def test_later_admitted_event_requires_successor_reconciliation() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = copied_surface(Path(directory))
        path = root / checker.LEDGER_PATH
        ledger = json.loads(path.read_text(encoding="utf-8"))
        ledger["declared_event_registry_complete_through"]["as_of_utc"] = "2026-07-21T00:00:00Z"
        ledger["admitted_state_changing_events"].append(
            {
                "event_id": "FTS-TEST-LATER-ADMITTED-EVENT",
                "admitted_at_utc": "2026-07-21T00:00:00Z",
                "admission_coordinate": "test-coordinate",
                "state_change_admitted": True,
                "affected_scope": ["proof_surface"],
                "source_path": checker.AUDIT_PATH.as_posix(),
                "source_sha256": hashlib.sha256((root / checker.AUDIT_PATH).read_bytes()).hexdigest(),
                "transition": "TEST_ONLY_LATER_STATE_CHANGE",
            }
        )
        write_json(path, ledger)
        errors = checker.check(root)
        assert any(checker.FAILURE_CODE in error for error in errors)


def test_current_projection_cannot_promote_execution_effect() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = copied_surface(Path(directory))
        path = root / checker.CURRENT_PATH
        projection = json.loads(path.read_text(encoding="utf-8"))
        projection["effects"]["pair_001_calls"] = 1
        write_json(path, projection)
        errors = checker.check(root)
        assert any("current zero effects" in error for error in errors)
