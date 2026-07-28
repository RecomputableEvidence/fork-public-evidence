#!/usr/bin/env python3
"""Build deterministic GHCH v0.1 valid and adversarial fixtures."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any, Dict

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from ghch_common_v0_1 import (  # noqa: E402
    add_integrity,
    build_cadence,
    pretty_json,
    refresh_record,
)

def stage(record: Dict[str, Any], name: str) -> Dict[str, Any]:
    return next(event for event in record["events"] if event["stage"] == name)

def fixtures() -> Dict[str, Dict[str, Any]]:
    result: Dict[str, Dict[str, Any]] = {}

    result["valid/clean_round_trip.json"] = build_cadence("CLEAN_ROUND_TRIP")
    result["valid/permissible_narrowing.json"] = build_cadence("PERMISSIBLE_NARROWING")
    result["valid/sidecar_unavailable_fail_open.json"] = build_cadence(
        "SIDECAR_UNAVAILABLE_FAIL_OPEN"
    )

    record = build_cadence("CLEAN_ROUND_TRIP")
    ingest = stage(record, "DOWNSTREAM_INGEST")
    ingest["detected_flags"]["authority_inheritance"] = True
    ingest["local_effects"]["authority_action"] = "LOCAL_ONLY"
    ingest["local_effects"]["authority_source"] = "UPSTREAM_INHERITED"
    result["invalid/authority_inheritance.json"] = refresh_record(record)

    record = build_cadence("CLEAN_ROUND_TRIP")
    disposition = stage(record, "DOWNSTREAM_LOCAL_DISPOSITION")
    disposition["local_effects"]["standing_action"] = "INHERITED_PROMOTION"
    disposition["local_effects"]["standing_basis"] = "UPSTREAM_STANDING_PROMOTED"
    disposition["detected_flags"]["standing_inheritance"] = True
    result["invalid/standing_promotion.json"] = refresh_record(record)

    record = build_cadence("CLEAN_ROUND_TRIP")
    record["non_claim_set"]["non_claims"].remove("NO_ENDORSEMENT_INHERITANCE")
    result["invalid/missing_non_claim.json"] = refresh_record(record)

    record = build_cadence("CLEAN_ROUND_TRIP")
    reconcile = stage(record, "UPSTREAM_RECONCILE")
    reconcile["detected_flags"]["unresolved_resolved_by_assumption"] = True
    reconcile["notes"].append("An unresolved item was silently treated as resolved.")
    result["invalid/unresolved_resolved_by_assumption.json"] = refresh_record(record)

    record = build_cadence("CLEAN_ROUND_TRIP")
    ingest = stage(record, "DOWNSTREAM_INGEST")
    ingest["detected_flags"]["evidence_reference_promotion"] = True
    ingest["notes"].append("Referenced evidence was treated as independently verified.")
    result["invalid/evidence_reference_promotion.json"] = refresh_record(record)

    record = build_cadence("CLEAN_ROUND_TRIP")
    record["events"][3]["predecessor_ref"] = {
        "event_id": "GHCH-EVT-999",
        "sha256": "9" * 64,
    }
    record["events"][3] = add_integrity(record["events"][3])
    result["invalid/stale_predecessor.json"] = record

    record = build_cadence("CLEAN_ROUND_TRIP")
    record["events"][4]["event_id"] = record["events"][3]["event_id"]
    result["invalid/duplicate_event_id.json"] = refresh_record(record)

    record = build_cadence("CLEAN_ROUND_TRIP")
    disposition = stage(record, "DOWNSTREAM_LOCAL_DISPOSITION")
    disposition["claim_delta"] = [
        {
            "operation": "EXPAND",
            "claim_id": "GHCH-CLM-001",
            "basis": "Unbounded downstream inference.",
        }
    ]
    record["reconciliation"]["relationship"] = "PRESERVED"
    result["invalid/hidden_claim_expansion.json"] = refresh_record(record)

    record = build_cadence("SIDECAR_UNAVAILABLE_FAIL_OPEN")
    stage(record, "DOWNSTREAM_INGEST")["observed_status"] = "BLOCKED"
    stage(record, "DOWNSTREAM_LOCAL_DISPOSITION")["observed_status"] = "BLOCKED"
    stage(record, "CADENCE_CLOSE")["observed_status"] = "FAILED"
    result["invalid/sidecar_unavailability_blocks_workflow.json"] = refresh_record(record)

    record = build_cadence("CLEAN_ROUND_TRIP")
    record["events"][3], record["events"][4] = record["events"][4], record["events"][3]
    result["invalid/stage_order_regression.json"] = refresh_record(record)

    return result

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("/tmp/ghch-fixtures"),
    )
    args = parser.parse_args()
    for relative, record in sorted(fixtures().items()):
        path = args.output_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(pretty_json(record))
        print(path.as_posix())
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
