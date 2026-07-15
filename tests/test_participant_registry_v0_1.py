import os
import json
from tools.check_participant_registry_v0_1 import check_registry_record

FIXTURE_DIR = "fixtures/participant-profile-registry/v0_1"

def test_valid_fixtures():
    valid_dir = os.path.join(FIXTURE_DIR, "valid")
    for f in os.listdir(valid_dir):
        if f.endswith(".json"):
            with open(os.path.join(valid_dir, f), 'r', encoding='utf-8') as file:
                result = check_registry_record(json.load(file))
                assert result["status"] == "CONFORMING", f"Failed on {f}"

def test_adversarial_fixtures():
    adv_dir = os.path.join(FIXTURE_DIR, "adversarial")
    
    # ADV_001: Attribution without consent
    with open(os.path.join(adv_dir, "PPR_ADV_001_attribution_without_consent.json"), 'r', encoding='utf-8') as f:
        res1 = check_registry_record(json.load(f))
        assert res1["status"] == "SPECIFICATION_PRESSURE"
        
    # ADV_002: Improper endorsement object attachment
    with open(os.path.join(adv_dir, "PPR_ADV_002_improper_endorsement.json"), 'r', encoding='utf-8') as f:
        res2 = check_registry_record(json.load(f))
        assert res2["status"] == "NON_CONFORMING"
        assert "Additional properties are not allowed" in res2["reason"]
