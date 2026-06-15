import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "ai_governance_system_placement_profile_v0_1.schema.json"
FIXTURE_DIR = ROOT / "examples" / "ai_governance_system_placement_profile" / "records_v0_1"
DOC_PATH = ROOT / "docs" / "AI_GOVERNANCE_SYSTEM_PLACEMENT_PROFILE_SCHEMA_AND_FIXTURES_v0_1.md"
REQUIRED_TOP_LEVEL = ["profile_version","system_identity","role_classification","authority_boundary","supported_claims","explicit_non_claims","evidence_inputs","evidence_outputs","handoff_requirements","unresolved_unknowns","verification_state"]
VALID_FIXTURES = ["VALID_EVALUATION_SYSTEM_PLACEMENT_v0_1.json","VALID_MONITORING_SYSTEM_PLACEMENT_v0_1.json","VALID_COMPLIANCE_MAPPING_PLACEMENT_v0_1.json"]

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def all_ids(record):
    ids=[]
    ids += [i["claim_id"] for i in record.get("supported_claims", []) if "claim_id" in i]
    ids += [i["non_claim_id"] for i in record.get("explicit_non_claims", []) if "non_claim_id" in i]
    ids += [i["evidence_input_id"] for i in record.get("evidence_inputs", []) if "evidence_input_id" in i]
    ids += [i["evidence_output_id"] for i in record.get("evidence_outputs", []) if "evidence_output_id" in i]
    ids += [i["handoff_id"] for i in record.get("handoff_requirements", []) if "handoff_id" in i]
    unknowns = record.get("unresolved_unknowns", {})
    ids += [i["unknown_id"] for i in unknowns.get("declared_unknown_classes", []) if "unknown_id" in i]
    ids += [i["unknown_id"] for i in unknowns.get("active_unresolved_unknowns", []) if "unknown_id" in i]
    ids += [i["clause_id"] for i in record.get("non_transitive_clauses", []) if "clause_id" in i]
    return ids

def assert_valid_local_references(testcase, record):
    input_ids = {i["evidence_input_id"] for i in record["evidence_inputs"]}
    claim_ids = {i["claim_id"] for i in record["supported_claims"]}
    non_claim_ids = {i["non_claim_id"] for i in record["explicit_non_claims"]}
    output_ids = {i["evidence_output_id"] for i in record["evidence_outputs"]}
    unknowns = record["unresolved_unknowns"]
    unknown_ids = {i["unknown_id"] for i in unknowns.get("declared_unknown_classes", [])}
    unknown_ids.update(i["unknown_id"] for i in unknowns.get("active_unresolved_unknowns", []))
    for claim in record["supported_claims"]:
        testcase.assertTrue(set(claim["evidence_basis"]).issubset(input_ids), claim["claim_id"])
    for output in record["evidence_outputs"]:
        testcase.assertTrue(set(output["supports_claim_ids"]).issubset(claim_ids), output["evidence_output_id"])
        testcase.assertTrue(set(output["carries_non_claim_ids"]).issubset(non_claim_ids), output["evidence_output_id"])
    for handoff in record["handoff_requirements"]:
        testcase.assertTrue(set(handoff["evidence_output_ids"]).issubset(output_ids), handoff["handoff_id"])
        testcase.assertTrue(set(handoff["non_claim_ids_to_preserve"]).issubset(non_claim_ids), handoff["handoff_id"])
        testcase.assertTrue(set(handoff["unknown_ids_to_preserve"]).issubset(unknown_ids), handoff["handoff_id"])

class TestAIGovernanceSystemPlacementProfileSchemaFixturesV01(unittest.TestCase):
    def test_schema_and_doc_files_exist(self):
        self.assertTrue(SCHEMA_PATH.exists())
        self.assertTrue(DOC_PATH.exists())
    def test_schema_declares_minimal_required_core(self):
        schema=load_json(SCHEMA_PATH)
        self.assertEqual(schema["properties"]["profile_version"]["const"], "ai_governance_system_placement_profile.v0.1")
        self.assertEqual(schema["required"], REQUIRED_TOP_LEVEL)
        self.assertFalse(schema["additionalProperties"])
        self.assertFalse(schema["$defs"]["system_identity"]["additionalProperties"])
        self.assertFalse(schema["$defs"]["authority_boundary"]["additionalProperties"])
    def test_valid_fixtures_have_required_core_and_unique_ids(self):
        schema=load_json(SCHEMA_PATH); allowed=set(schema["$defs"]["role_classification"]["enum"])
        for filename in VALID_FIXTURES:
            record=load_json(FIXTURE_DIR/filename)
            for field in REQUIRED_TOP_LEVEL: self.assertIn(field, record, filename)
            self.assertEqual(record["profile_version"], "ai_governance_system_placement_profile.v0.1")
            self.assertTrue(set(record["role_classification"]).issubset(allowed), filename)
            ids=all_ids(record); self.assertEqual(len(ids), len(set(ids)), filename)
            assert_valid_local_references(self, record)
    def test_invalid_missing_required_field_fixture_omits_non_claims(self):
        self.assertNotIn("explicit_non_claims", load_json(FIXTURE_DIR/"INVALID_MISSING_REQUIRED_FIELD_v0_1.json"))
    def test_invalid_claim_nonclaim_overlap_fixture_contains_exact_overlap(self):
        record=load_json(FIXTURE_DIR/"INVALID_CLAIM_NONCLAIM_OVERLAP_v0_1.json")
        claims={i["statement"].strip().lower() for i in record["supported_claims"]}
        nonclaims={i["statement"].strip().lower() for i in record["explicit_non_claims"]}
        self.assertTrue(claims.intersection(nonclaims))
    def test_invalid_restricted_claim_fixture_contains_restricted_authority_language(self):
        text=" ".join(i["statement"].lower() for i in load_json(FIXTURE_DIR/"INVALID_RESTRICTED_CLAIM_v0_1.json")["supported_claims"])
        self.assertIn("compliance satisfied", text); self.assertIn("legally approved", text)
    def test_invalid_duplicate_id_fixture_contains_duplicate_identifier(self):
        ids=all_ids(load_json(FIXTURE_DIR/"INVALID_DUPLICATE_ID_v0_1.json")); self.assertNotEqual(len(ids), len(set(ids)))
    def test_invalid_role_classification_fixture_uses_unknown_role(self):
        allowed=set(load_json(SCHEMA_PATH)["$defs"]["role_classification"]["enum"])
        record=load_json(FIXTURE_DIR/"INVALID_ROLE_CLASSIFICATION_v0_1.json")
        self.assertFalse(set(record["role_classification"]).issubset(allowed))
    def test_invalid_handoff_reference_fixture_contains_reference_gap(self):
        record=load_json(FIXTURE_DIR/"INVALID_HANDOFF_REFERENCE_v0_1.json")
        output_ids={i["evidence_output_id"] for i in record["evidence_outputs"]}
        referenced=set(record["handoff_requirements"][0]["evidence_output_ids"])
        self.assertFalse(referenced.issubset(output_ids))
    def test_indeterminate_fixture_declares_active_unknown_and_state(self):
        record=load_json(FIXTURE_DIR/"INDETERMINATE_ACTIVE_UNRESOLVED_UNKNOWN_v0_1.json")
        self.assertEqual(record["verification_state"]["state"], "INDETERMINATE")
        self.assertGreater(len(record["unresolved_unknowns"]["active_unresolved_unknowns"]), 0)
        assert_valid_local_references(self, record)
if __name__ == "__main__": unittest.main()
