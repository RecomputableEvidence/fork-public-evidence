import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PKG=ROOT/"docs/exterior-observations/reviews"

def test_editorial_correction_is_bounded():
    review=(PKG/"EXTERIOR_REVIEW_PR89_PR90_RECOMPUTATION_v0_1.md").read_text(encoding="utf-8")
    note=(PKG/"EDITORIAL_CORRECTION_GOVERNED_PRESERVATION_SHA_v0_1.md").read_text(encoding="utf-8")
    assert "1241c008…e296" not in review
    assert review.count("1241c008…b4a7") == 2
    assert "Substantive-review effect:** `NONE`" in note

def test_receipt_preserves_non_effects_and_coordinates():
    r=json.loads((PKG/"EXTERIOR_REVIEW_PR89_PR90_RECEIPT_v0_1.json").read_text(encoding="utf-8"))
    assert r["disposition"]=="REPRODUCED_WITHIN_DECLARED_SCOPE"
    assert r["coordinates"]["pr_89_head"]=="b93f9a1bce094e8c65e0d1ef04dbe52a11aab0b1"
    assert r["coordinates"]["pr_90_reviewed_head"]=="bac40d9bdbd7f6b4927a676fef8def70756ad9d5"
    assert r["coordinates"]["pr_90_reviewed_tree"]=="aa8b1e5f47d2ca062588b8f50c58fa6014ee29ba"
    assert all(v is False for k,v in r["effects"].items() if isinstance(v,bool))
    assert r["effects"]["pair_001_calls"]==0
    assert r["effects"]["pair_001_repetitions"]==0

def test_receipt_payload_digest_recomputes():
    p=PKG/"EXTERIOR_REVIEW_PR89_PR90_RECEIPT_v0_1.json"
    r=json.loads(p.read_text(encoding="utf-8")); declared=r["integrity"].pop("receipt_payload_sha256")
    canonical=json.dumps(r,sort_keys=True,ensure_ascii=False,separators=(",",":")).encode("utf-8")
    assert hashlib.sha256(canonical).hexdigest()==declared
