from pathlib import Path
import importlib.util


def load_checker():
    path = Path("tools/check_public_review_round_006_observations_v0_1.py")
    spec = importlib.util.spec_from_file_location("round006_checker", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_round006_observations_are_bounded_and_schema_valid():
    module = load_checker()
    result = module.evaluate(Path.cwd())
    assert result["total"] == 2
    assert result["failed"] == 0
