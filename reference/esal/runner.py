import json
import sys
from pathlib import Path
from typing import Any

from .canonicalization import canonicalize
from .errors import StructuralError
from .fingerprint import canonical_event_sequence_hash, hash_state
from .models import INITIAL_STATE, state_to_dict
from .reducer import reduce_state
from .taxonomy import classify, exception_to_dict
from .validator import validate_event_shape, validate_lineage


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8-sig") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()

            if not stripped:
                continue

            if stripped.startswith("#"):
                continue

            try:
                value = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise StructuralError(
                    f"invalid JSONL at {path}:{line_number}: {exc}",
                    error_code="INVALID_JSONL",
                    path=str(path),
                ) from exc

            if not isinstance(value, dict):
                raise StructuralError(
                    f"JSONL event must be object at {path}:{line_number}",
                    error_code="JSONL_EVENT_NOT_OBJECT",
                    path=str(path),
                )

            events.append(value)

    return events


def replay(events: list[dict[str, Any]]) -> dict[str, Any]:
    validate_event_shape(events)

    canonical_events = canonicalize(events)

    validate_lineage(canonical_events)

    state = reduce_state(
        INITIAL_STATE,
        canonical_events,
    )

    fingerprint = hash_state(state)

    return {
        "canonical_events": canonical_events,
        "canonical_events_hash": canonical_event_sequence_hash(canonical_events),
        "state": state,
        "state_dict": state_to_dict(state),
        "fingerprint": fingerprint,
        "classification": classify(state=state),
        "exception": None,
    }


def replay_file(path: Path) -> dict[str, Any]:
    try:
        events = load_jsonl(path)
        result = replay(events)

        return {
            "log": str(path),
            "fingerprint": result["fingerprint"],
            "canonical_events_hash": result["canonical_events_hash"],
            "classification": result["classification"],
            "state": result["state_dict"],
            "exception": None,
        }

    except Exception as exc:
        return {
            "log": str(path),
            "fingerprint": None,
            "canonical_events_hash": None,
            "classification": classify(exc=exc),
            "state": None,
            "exception": exception_to_dict(exc),
        }


def iter_jsonl_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root]

    return sorted(
        path
        for path in root.rglob("*.jsonl")
        if path.is_file()
    )


def run_corpus(root: Path) -> dict[str, Any]:
    results = [
        replay_file(path)
        for path in iter_jsonl_files(root)
    ]

    return {
        "root": str(root),
        "results": results,
        "counts": {
            "PASS": sum(1 for r in results if r["classification"] == "PASS"),
            "G": sum(1 for r in results if r["classification"] == "G"),
            "S": sum(1 for r in results if r["classification"] == "S"),
            "D": sum(1 for r in results if r["classification"] == "D"),
        },
    }


def print_report(report: dict[str, Any]) -> None:
    print("== ESAL v0.1 Reference Oracle Verification ==")
    print(f"Corpus: {report['root']}")
    print("")

    for result in report["results"]:
        name = Path(result["log"]).name
        print(f"Log: {name}")
        print(f"Fingerprint: {result['fingerprint']}")
        print(f"Classification: {result['classification']}")

        if result["exception"] is not None:
            print(f"Exception: {result['exception']['type']}: {result['exception']['message']}")

        print("")

    print("Summary:")
    for key in ("PASS", "G", "S", "D"):
        print(f"  {key}: {report['counts'][key]}")


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    root = Path(argv[0]) if argv else Path("esal-tests")

    report = run_corpus(root)

    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    latest_report = reports_dir / "latest-report.json"

    latest_report.write_text(
        json.dumps(
            report,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print_report(report)
    print(f"Report written: {latest_report}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())