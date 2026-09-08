#!/usr/bin/env python3
"""CLI entry point for Governed Handoff Cadence Harness v0.1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from ghch_evaluator_v0_1 import evaluate  # noqa: E402,F401

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    try:
        record = json.loads(args.record.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        result = {
            "disposition": "GHCH_CADENCE_REJECTED",
            "findings": ["UNREADABLE_RECORD:" + str(exc)],
        }
        if args.as_json:
            print(json.dumps(result, indent=2))
        else:
            print(result["disposition"])
            print("\n".join(result["findings"]))
        return 1

    if not isinstance(record, dict):
        disposition, findings = "GHCH_CADENCE_REJECTED", ["TOP_LEVEL_TYPE"]
    else:
        disposition, findings = evaluate(record)
    if args.as_json:
        print(json.dumps({"disposition": disposition, "findings": findings}, indent=2))
    else:
        print(disposition)
        for finding in findings:
            print(finding)
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
