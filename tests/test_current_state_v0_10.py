"""Regression checks for v0.10 coordinate and set-trajectory semantics."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("routing", ROOT / "scripts/check_current_state_routing_v0_1.py")
routing = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(routing)

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def test_current_routing_v010_passes():
    result = routing.evaluate(ROOT)
    assert result["failed"] == 0, result["checks"]

def test_numeric_pr_horizon_is_not_terminal_merge_event():
    standing = load("docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_10.json")
    assert standing["snapshot_max_pr_number"] == 183
    assert standing["snapshot_terminal_merge_pr"] == 182
    assert standing["merged_event_order"] == [179, 180, 181, 183, 182]
    assert standing["snapshot_max_pr_number"] != standing["snapshot_terminal_merge_pr"]

def test_open_set_equality_preserves_intervening_events():
    obs = load("docs/current-standing/OPEN_CANDIDATE_SET_REOBSERVATION_20260925_v0_1.json")
    assert obs["open_count"] == 18
    assert obs["predecessor_set_equal"] is True
    assert set(obs["current_open_pr_numbers"]) == set(obs["predecessor_open_pr_numbers"])
    assert {row["pr"] for row in obs["intervening_events"]} == {182, 183}
    assert all(row["head_reverified"] is False for row in obs["candidates"])

def test_closed_rrd_and_exterior_return_do_not_promote():
    standing = load("docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_10.json")
    rrd = next(x for x in standing["delta_objects"] if x["id"] == "FORK-RELATIONAL-RESOLUTION-DEMONSTRATION-001")
    ext = next(x for x in standing["delta_objects"] if x["id"] == "EXTERIOR-REPOSITORY-RECOMPUTATION-RETURN-001")
    assert rrd["research_state"] == "CLOSED_HISTORICAL_EVIDENCE"
    assert rrd["independent_recomputation"]["overall_match"] is True
    assert ext["gate"] == "DISPOSITION_UNASSIGNED_REMEDIATION_NONE"
    assert all(f["disposition"] == "UNASSIGNED" and f["remediation"] == "NONE" for f in ext["findings"])
