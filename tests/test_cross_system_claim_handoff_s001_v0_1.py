from pathlib import Path
import importlib.util, json
from jsonschema import Draft202012Validator

def load_module(path_text,name):
    path=Path(path_text); spec=importlib.util.spec_from_file_location(name,path); module=importlib.util.module_from_spec(spec)
    assert spec and spec.loader; spec.loader.exec_module(module); return module
def load(name): return json.loads(Path(f"tests/fixtures/csh_s001/{name}").read_text(encoding="utf-8"))

def test_clean_fixture_has_zero_rule_findings():
    c=load_module("tools/classify_unsupported_inheritance_s001_v0_1.py","c1"); assert c.classify(load("classifier_input_clean.json"))["event_count"]==0

def test_phantom_boundary_id_does_not_suppress_expansion_finding():
    c=load_module("tools/classify_unsupported_inheritance_s001_v0_1.py","c2"); r=c.classify(load("classifier_input_phantom_boundary.json"))
    assert r["event_count"]==1 and r["events"][0]["event_type"]=="claim_expansion_without_boundary"
    assert r["events"][0]["evidence"]["boundary_contract_substantiated"] is False

def test_substantiated_boundary_suppresses_boundaryless_expansion_finding():
    c=load_module("tools/classify_unsupported_inheritance_s001_v0_1.py","c3"); assert c.classify(load("classifier_input_substantiated_boundary.json"))["event_count"]==0

def test_classifier_output_schema():
    c=load_module("tools/classify_unsupported_inheritance_s001_v0_1.py","c4"); r=c.classify(load("classifier_input_phantom_boundary.json"))
    s=json.loads(Path("schemas/unsupported_inheritance_classification_s001_v0_1.schema.json").read_text(encoding="utf-8"))
    assert not list(Draft202012Validator(s).iter_errors(r))
