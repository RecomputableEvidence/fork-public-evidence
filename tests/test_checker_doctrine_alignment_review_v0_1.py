import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "CHECKER_DOCTRINE_ALIGNMENT_REVIEW_v0_1.md"
JSON_RECEIPT = REPO_ROOT / "output" / "semantic_alignment_reviews" / "CHECKER_DOCTRINE_ALIGNMENT_REVIEW_v0_1.json"


class TestCheckerDoctrineAlignmentReviewV01(unittest.TestCase):
    def test_alignment_review_files_exist(self):
        self.assertTrue(DOC.is_file())
        self.assertTrue(JSON_RECEIPT.is_file())

    def test_alignment_receipt_status(self):
        payload = json.loads(JSON_RECEIPT.read_text(encoding="utf-8"))
        self.assertEqual(payload["review_id"], "checker_doctrine_alignment_review.v0.1")
        self.assertEqual(payload["review_status"], "ALIGNED_WITH_LIMITED_V0_1_SCOPE")

    def test_alignment_receipt_has_required_status_variety(self):
        payload = json.loads(JSON_RECEIPT.read_text(encoding="utf-8"))
        statuses = {item["status"] for item in payload["alignment_checks"]}
        self.assertIn("ALIGNED", statuses)
        self.assertIn("PARTIALLY_ALIGNED", statuses)
        self.assertIn("GAP", statuses)
        self.assertIn("NOT_CLAIMED", statuses)

    def test_alignment_receipt_preserves_non_claims(self):
        payload = json.loads(JSON_RECEIPT.read_text(encoding="utf-8"))
        non_claim_text = " ".join(payload["non_claims"]).lower()
        for term in [
            "legal admissibility",
            "compliance satisfaction",
            "audit sufficiency",
            "ai output correctness",
            "decision correctness",
            "source completeness",
            "institutional acceptance",
            "production completeness",
        ]:
            self.assertIn(term, non_claim_text)

    def test_alignment_doc_mentions_core_boundaries(self):
        text = DOC.read_text(encoding="utf-8").lower()
        for term in [
            "silent claim",
            "non-claims",
            "indeterminate",
            "authority boundary",
            "safe handoff",
            "not a policy engine",
            "not a full semantic verifier",
        ]:
            self.assertIn(term, text)


if __name__ == "__main__":
    unittest.main()