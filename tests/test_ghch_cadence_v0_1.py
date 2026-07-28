#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TOOLS = REPO / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from build_ghch_fixtures_v0_1 import fixtures  # noqa: E402
from check_ghch_cadence_v0_1 import evaluate  # noqa: E402
from ghch_common_v0_1 import pretty_json, sha256_value  # noqa: E402

FIXTURE_ROOT = REPO / "fixtures/governed-handoff-cadence/v0_1"
SPECS_PATH = FIXTURE_ROOT / "FIXTURE-SPECS.json"
CORPUS_ROOT_PATH = FIXTURE_ROOT / "FIXTURE-CORPUS-ROOT.json"

class GovernedHandoffCadenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = fixtures()
        cls.specs = json.loads(SPECS_PATH.read_text(encoding="utf-8"))
        cls.corpus_root = json.loads(CORPUS_ROOT_PATH.read_text(encoding="utf-8"))

    def load(self, relative: str):
        return self.records[relative]

    def test_valid_profiles(self):
        expected = {
            "valid/clean_round_trip.json": "GHCH_CADENCE_CONFORMS_PRESERVED",
            "valid/permissible_narrowing.json": (
                "GHCH_CADENCE_CONFORMS_WITH_PERMISSIBLE_NARROWING"
            ),
            "valid/sidecar_unavailable_fail_open.json": (
                "GHCH_CADENCE_CONFORMS_WITH_OBSERVATION_GAPS"
            ),
        }
        for relative, disposition in expected.items():
            with self.subTest(relative=relative):
                observed, findings = evaluate(self.load(relative))
                self.assertEqual(observed, disposition)
                self.assertEqual(findings, [])

    def test_adversarial_profiles(self):
        expected_findings = {
            "invalid/authority_inheritance.json": {
                "AUTHORITY_INHERITANCE:DOWNSTREAM_INGEST",
                "LOCAL_EFFECTS:DOWNSTREAM_INGEST",
            },
            "invalid/standing_promotion.json": {
                "STANDING_INHERITANCE:DOWNSTREAM_LOCAL_DISPOSITION",
                "LOCAL_EFFECTS:DOWNSTREAM_LOCAL_DISPOSITION",
            },
            "invalid/missing_non_claim.json": {"NON_CLAIM_GAP"},
            "invalid/unresolved_resolved_by_assumption.json": {
                "UNRESOLVED_RESOLVED_BY_ASSUMPTION:UPSTREAM_RECONCILE"
            },
            "invalid/evidence_reference_promotion.json": {
                "EVIDENCE_REFERENCE_PROMOTION:DOWNSTREAM_INGEST"
            },
            "invalid/stale_predecessor.json": {
                "LINEAGE:DOWNSTREAM_INGEST",
                "LINEAGE:DOWNSTREAM_LOCAL_DISPOSITION",
            },
            "invalid/duplicate_event_id.json": {
                "DUPLICATE_EVENT_ID",
                "EVENT_ID_SEQUENCE",
            },
            "invalid/hidden_claim_expansion.json": {
                "UNPERMITTED_CLAIM_OPERATION:EXPAND",
                "UNDECLARED_DELTA",
            },
            "invalid/sidecar_unavailability_blocks_workflow.json": {
                "FAIL_OPEN_CONTINUITY_INGEST",
                "FAIL_OPEN_CONTINUITY_DISPOSITION",
                "FAIL_OPEN_CLOSE_STANDING",
            },
            "invalid/stage_order_regression.json": {
                "STAGE_ORDER",
                "EVENT_ID_SEQUENCE",
            },
        }
        for relative, required in expected_findings.items():
            with self.subTest(relative=relative):
                disposition, findings = evaluate(self.load(relative))
                self.assertEqual(disposition, "GHCH_CADENCE_REJECTED")
                self.assertTrue(required.issubset(set(findings)), (relative, findings))

    def test_fixture_specs_match_builder_inventory(self):
        observed = {
            item["fixture_path"]: item["fixture_class"]
            for item in self.specs["fixtures"]
        }
        expected = {
            path: "VALID" if path.startswith("valid/") else "ADVERSARIAL"
            for path in self.records
        }
        self.assertEqual(observed, expected)
        self.assertNotIn("expected_disposition", json.dumps(self.specs))
        self.assertNotIn("expected_findings", json.dumps(self.specs))

    def test_generated_corpus_matches_digest_root(self):
        observed_entries = []
        for relative, record in sorted(self.records.items()):
            data = pretty_json(record)
            observed_entries.append(
                {
                    "fixture_path": relative,
                    "byte_size": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                }
            )
        self.assertEqual(observed_entries, self.corpus_root["fixtures"])
        self.assertEqual(len(observed_entries), self.corpus_root["fixture_count"])
        self.assertEqual(
            sha256_value(observed_entries),
            self.corpus_root["corpus_root_sha256"],
        )

    def test_compact_control_plane_has_no_stale_file_routes(self):
        stale_routes = {
            "PROTOCOL.md",
            "SEMANTIC-INVARIANTS.json",
            "NEXT-STAGE-GATES.json",
            "NO-EFFECTS.json",
        }
        route_text = (
            REPO / "docs/experiments/governed-handoff-cadence-v0.1/README.md"
        ).read_text(encoding="utf-8") + "\n" + (
            REPO
            / "docs/experiments/governed-handoff-cadence-v0.1/GHCH-CONTROL-PLANE.json"
        ).read_text(encoding="utf-8")
        for stale_route in stale_routes:
            with self.subTest(stale_route=stale_route):
                self.assertNotIn(stale_route, route_text)

    def test_schema_and_control_documents_are_valid_json(self):
        json_paths = [
            REPO / "schemas/ghch_cadence_record_v0_1.schema.json",
            REPO
            / "docs/experiments/governed-handoff-cadence-v0.1/GHCH-CONTROL-PLANE.json",
            SPECS_PATH,
            CORPUS_ROOT_PATH,
        ]
        for path in json_paths:
            with self.subTest(path=path):
                json.loads(path.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
