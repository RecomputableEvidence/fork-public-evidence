from pathlib import Path
import importlib.util


def load_module(path_text, name):
    path = Path(path_text)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_schema_bundle_is_mechanically_enforced():
    module = load_module("tools/validate_json_schema_bundle_v0_1.py", "schema_bundle")
    result = module.evaluate(Path.cwd())
    assert result["failed"] == 0


def test_canonical_state_and_repository_summaries_are_synchronized():
    module = load_module("tools/check_fork_proof_surface_state_v0_1.py", "state_checker")
    # Exercise through main-facing state functions indirectly by validating expected summary.
    import json
    state = json.loads(Path("docs/state/FORK_PROOF_SURFACE_STATE_v0_1.json").read_text(encoding="utf-8"))
    expected = module.render_summary(state)
    actual = Path("docs/state/FORK_PROOF_SURFACE_STATE_SUMMARY_v0_1.md").read_text(encoding="utf-8")
    assert actual == expected
