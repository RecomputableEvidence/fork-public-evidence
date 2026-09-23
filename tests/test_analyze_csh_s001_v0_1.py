from pathlib import Path
import importlib.util

def load_module(path_text,name):
    path=Path(path_text); spec=importlib.util.spec_from_file_location(name,path); module=importlib.util.module_from_spec(spec)
    assert spec and spec.loader; spec.loader.exec_module(module); return module

def test_analysis_separates_rule_findings_claims_runs_and_task_state():
    mod=load_module("tools/analyze_csh_s001_v0_1.py","a1")
    records=[
      {"receiver_run_id":"R1","pairing_key":"P1","scenario_id":"S1","receiver_class_id":"A","condition":"control_h0","terminal_state":"COMPLETED_CLASSIFIABLE","task_state":"COMPLETE_TRANSFER_RECORD",
       "classification":{"event_count":2,"events":[
         {"event_type":"claim_expansion_without_boundary","evidence":{"claim_id":"D1"}},
         {"event_type":"declared_observed_mismatch","evidence":{"claim_id":"D1","observed_relationship":"EXPANDED"}}]}},
      {"receiver_run_id":"R2","pairing_key":"P1","scenario_id":"S1","receiver_class_id":"A","condition":"instrumented_h1","terminal_state":"COMPLETED_CLASSIFIABLE","task_state":"BOUNDED_ABSTENTION","classification":{"event_count":0,"events":[]}},
      {"receiver_run_id":"R3","pairing_key":"P2","scenario_id":"S1","receiver_class_id":"A","condition":"control_h0","terminal_state":"EXECUTION_UNAVAILABLE","task_state":None}
    ]
    result=mod.summarize(records)
    assert result["classifiable_run_count"]==2
    assert result["run_rows"][0]["U"]==2 and result["run_rows"][0]["P"]==1 and result["run_rows"][0]["A"]==1
    assert result["run_rows"][2]["U"] is None
    assert result["paired_differences"][0]["D_pair"]==-2
    assert result["task_state_distribution"]["BOUNDED_ABSTENTION"]==1
