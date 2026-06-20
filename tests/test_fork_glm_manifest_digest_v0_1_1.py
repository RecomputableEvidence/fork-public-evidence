from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "tools" / "compute_fork_glm_manifest_digest.py"


spec = importlib.util.spec_from_file_location("compute_fork_glm_manifest_digest", TOOL_PATH)
assert spec is not None
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_canonical_well_known_manifest_digest_recomputes() -> None:
    result = module.compute_sha256(ROOT / ".well-known" / "governance-layer-manifest.json")
    assert result["ok"] is True
    assert result["declared"]["type"] == "sha256"
    assert result["declared"]["value"] == result["computed"]["value"]


def test_repo_glm_manifest_digest_recomputes() -> None:
    result = module.compute_sha256(ROOT / "glm" / "fork_governance_layer_manifest_v0_1.json")
    assert result["ok"] is True
    assert result["declared"]["type"] == "sha256"
    assert result["declared"]["value"] == result["computed"]["value"]
