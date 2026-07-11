from pathlib import Path
import importlib.util


def load_checker():
    path = Path("tools/check_reviewer_access_path_integrity_v0_1.py")
    spec = importlib.util.spec_from_file_location("rapi_checker", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_shipped_access_path_fixtures_match_expected_classification():
    module = load_checker()
    result = module.evaluate(Path.cwd())
    assert result["total"] >= 7
    assert result["failed"] == 0


def test_retrieval_failure_cannot_become_content_review():
    module = load_checker()
    item = {
        "access_state": "retrieval_failed",
        "retrieval_fidelity": "none",
        "interpreter_state": "not_attempted",
        "execution_state": "not_attempted",
        "content_assessment_permitted": True,
        "content_findings": ["repository is structurally defective"],
        "review_claims": ["negative content review completed"],
    }
    assert module.semantic_errors(item)
