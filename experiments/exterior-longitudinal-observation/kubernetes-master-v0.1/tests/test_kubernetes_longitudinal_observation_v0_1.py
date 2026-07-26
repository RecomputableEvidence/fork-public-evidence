from __future__ import annotations

import copy
import datetime as dt
import hashlib
import importlib.util
import json
import shutil
from pathlib import Path
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[1]
TOOLS = BASE / "tools"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = load_module("k8s_checker_test", TOOLS / "check_kubernetes_observation_v0_1.py")
comparer = load_module("k8s_comparer_test", TOOLS / "compare_kubernetes_observations_v0_1.py")
package_checker = load_module(
    "k8s_package_checker_test",
    TOOLS / "check_kubernetes_experiment_package_v0_1.py",
)


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def make_package(root: Path, timestamp: str, head: str, tree: str,
                 branch_extra: dict | None = None, parser_version: str = "0.1"):
    branch = {
        "name": "master",
        "commit": {"sha": head},
        "protected": False,
    }
    if branch_extra:
        branch.update(branch_extra)
    commit = {
        "sha": head,
        "commit": {"tree": {"sha": tree}},
        "parents": [{"sha": "1" * 40}],
    }
    branch_raw = canonical_bytes(branch)
    commit_raw = canonical_bytes(commit)
    (root / "raw").mkdir(parents=True)
    (root / "raw/branch_representation.bin").write_bytes(branch_raw)
    (root / "raw/commit_representation.bin").write_bytes(commit_raw)
    projection = {
        "branch_name": "master",
        "head_sha": head,
        "head_tree_sha": tree,
        "parent_shas": ["1" * 40],
        "protected": False,
    }
    suffix = sha((timestamp + head).encode())[:12]
    record = {
        "schema_version": "0.1",
        "experiment_id": "FORK_ELO_KUBERNETES_MASTER_v0_1",
        "observation_id": "K8S-MASTER-OBS-" + timestamp.replace("-", "").replace(":", "") + "-" + suffix,
        "observer": {
            "tool": "tools/observe_kubernetes_master_v0_1.py",
            "tool_sha256": "a" * 64,
            "parser_version": parser_version,
            "runtime": "3.12.0",
        },
        "source": {
            "operator": "GitHub",
            "repository": "kubernetes/kubernetes",
            "branch": "master",
            "branch_endpoint": "https://api.github.com/repos/kubernetes/kubernetes/branches/master",
            "commit_endpoint_template": "https://api.github.com/repos/kubernetes/kubernetes/commits/{sha}",
        },
        "request_policy": {
            "method": "GET", "authenticated": False, "automatic_retries": 0,
            "redirects_followed": False, "maximum_requests": 2,
        },
        "timing": {
            "started_at_utc": timestamp,
            "completed_at_utc": timestamp,
            "source_date_header": None,
        },
        "retrieval_status": "OBSERVED",
        "retrievals": [
            {
                "role": "BRANCH_REPRESENTATION",
                "url": "https://api.github.com/repos/kubernetes/kubernetes/branches/master",
                "method": "GET",
                "http_status": 200,
                "headers": {},
                "headers_path": "raw/branch_representation.headers.json",
                "raw_path": "raw/branch_representation.bin",
                "raw_sha256": sha(branch_raw),
                "raw_size_bytes": len(branch_raw),
            },
            {
                "role": "COMMIT_REPRESENTATION",
                "url": f"https://api.github.com/repos/kubernetes/kubernetes/commits/{head}",
                "method": "GET",
                "http_status": 200,
                "headers": {},
                "headers_path": "raw/commit_representation.headers.json",
                "raw_path": "raw/commit_representation.bin",
                "raw_sha256": sha(commit_raw),
                "raw_size_bytes": len(commit_raw),
            },
        ],
        "projection": projection,
        "projection_sha256": sha(canonical_bytes(projection)),
        "previous_observation": None,
        "findings": [],
        "unresolved": [
            "UNDERLYING_CHANGE_TIME", "CAUSE", "INTERMEDIATE_STATE_COMPLETENESS",
            "SOURCE_TRUTH_AND_COMPLETENESS", "EXTERNAL_AUTHORITY_EFFECT",
        ],
        "effects": {
            "source_modification": "NONE", "fork_repository_mutation": "NONE",
            "authority": "NONE", "admission": "NONE", "execution": "NONE",
            "truth": "NONE", "causality": "NONE", "endorsement": "NONE",
        },
        "non_claims": ["bounded"],
    }
    raw = canonical_bytes(record)
    (root / "observation.json").write_bytes(raw)
    return record, raw


class KubernetesObservationTests(unittest.TestCase):
    def test_valid_observation_conforms(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            record, _ = make_package(root, "2026-07-25T00:00:00Z", "2" * 40, "3" * 40)
            self.assertEqual([], checker.validate_record(record, root))

    def test_raw_digest_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            record, _ = make_package(root, "2026-07-25T00:00:00Z", "2" * 40, "3" * 40)
            (root / "raw/branch_representation.bin").write_bytes(b"mutated")
            self.assertIn("RETRIEVAL_0_RAW_DIGEST_MISMATCH", checker.validate_record(record, root))

    def test_projection_digest_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            record, _ = make_package(root, "2026-07-25T00:00:00Z", "2" * 40, "3" * 40)
            record["projection"]["protected"] = True
            self.assertIn("PROJECTION_DIGEST_MISMATCH", checker.validate_record(record, root))

    def test_false_projection_with_recomputed_digest_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            record, _ = make_package(root, "2026-07-25T00:00:00Z", "2" * 40, "3" * 40)
            record["projection"]["head_tree_sha"] = "9" * 40
            record["projection_sha256"] = sha(canonical_bytes(record["projection"]))
            self.assertIn("PROJECTION_DIVERGES_FROM_RAW_BYTES", checker.validate_record(record, root))

    def test_authority_promotion_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            record, _ = make_package(root, "2026-07-25T00:00:00Z", "2" * 40, "3" * 40)
            record["effects"]["authority"] = "INHERITED"
            self.assertIn("EFFECT_PROMOTION_FORBIDDEN:authority", checker.validate_record(record, root))

    def test_authenticated_request_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            record, _ = make_package(root, "2026-07-25T00:00:00Z", "2" * 40, "3" * 40)
            record["request_policy"]["authenticated"] = True
            self.assertIn("REQUEST_POLICY_INVALID:authenticated", checker.validate_record(record, root))

    def test_changed_head_classified_as_observed_change(self):
        with tempfile.TemporaryDirectory() as left_temp, tempfile.TemporaryDirectory() as right_temp:
            left_root, right_root = Path(left_temp), Path(right_temp)
            left, left_raw = make_package(left_root, "2026-07-25T00:00:00Z", "2" * 40, "3" * 40)
            right, right_raw = make_package(right_root, "2026-07-25T01:00:00Z", "4" * 40, "5" * 40)
            result = comparer.derive_comparison(left, left_raw, right, right_raw)
            self.assertEqual("OBSERVED_REPRESENTATION_CHANGED", result["classification"])
            self.assertTrue(result["differences"]["head_sha_changed"])
            self.assertEqual("NONE", result["effects"]["authority"])
            self.assertEqual("UNRESOLVED", result["cause"])

    def test_raw_change_semantics_stable(self):
        with tempfile.TemporaryDirectory() as left_temp, tempfile.TemporaryDirectory() as right_temp:
            left_root, right_root = Path(left_temp), Path(right_temp)
            left, left_raw = make_package(left_root, "2026-07-25T00:00:00Z", "2" * 40, "3" * 40)
            right, right_raw = make_package(
                right_root, "2026-07-25T01:00:00Z", "2" * 40, "3" * 40,
                branch_extra={"synthetic_nondeterministic_field": "different"}
            )
            result = comparer.derive_comparison(left, left_raw, right, right_raw)
            self.assertEqual("RAW_BYTES_CHANGED_SEMANTICS_STABLE", result["classification"])
            self.assertFalse(result["differences"]["semantic_projection_changed"])

    def test_parser_change_is_unresolved_not_silently_compared(self):
        with tempfile.TemporaryDirectory() as left_temp, tempfile.TemporaryDirectory() as right_temp:
            left_root, right_root = Path(left_temp), Path(right_temp)
            left, left_raw = make_package(left_root, "2026-07-25T00:00:00Z", "2" * 40, "3" * 40)
            right, right_raw = make_package(right_root, "2026-07-25T01:00:00Z", "4" * 40, "5" * 40, parser_version="0.2")
            result = comparer.derive_comparison(left, left_raw, right, right_raw)
            self.assertEqual("PARSER_VERSION_CHANGED_UNRESOLVED", result["classification"])

    def test_failed_retrieval_creates_gap(self):
        with tempfile.TemporaryDirectory() as left_temp, tempfile.TemporaryDirectory() as right_temp:
            left_root, right_root = Path(left_temp), Path(right_temp)
            left, left_raw = make_package(left_root, "2026-07-25T00:00:00Z", "2" * 40, "3" * 40)
            right, right_raw = make_package(right_root, "2026-07-25T01:00:00Z", "2" * 40, "3" * 40)
            right["retrieval_status"] = "RETRIEVAL_FAILED"
            right["projection"] = None
            right["projection_sha256"] = None
            right_raw = canonical_bytes(right)
            result = comparer.derive_comparison(left, left_raw, right, right_raw)
            self.assertEqual("OBSERVATION_GAP", result["classification"])
            self.assertTrue(result["observation_gap_present"])

    def test_backdated_comparison_rejected(self):
        with tempfile.TemporaryDirectory() as left_temp, tempfile.TemporaryDirectory() as right_temp:
            left_root, right_root = Path(left_temp), Path(right_temp)
            left, left_raw = make_package(left_root, "2026-07-25T02:00:00Z", "2" * 40, "3" * 40)
            right, right_raw = make_package(right_root, "2026-07-25T01:00:00Z", "4" * 40, "5" * 40)
            with self.assertRaisesRegex(ValueError, "must precede"):
                comparer.derive_comparison(left, left_raw, right, right_raw)

    def test_duplicate_json_key_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.json"
            path.write_text('{"schema_version":"0.1","schema_version":"0.2"}', encoding="utf-8")
            with self.assertRaises(checker.DuplicateKeyError):
                checker.load_json(path)

    def test_missing_unresolved_boundary_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            record, _ = make_package(root, "2026-07-25T00:00:00Z", "2" * 40, "3" * 40)
            record["unresolved"].remove("CAUSE")
            self.assertIn("UNRESOLVED_BOUNDARY_INCOMPLETE", checker.validate_record(record, root))

    def test_construction_package_manifest_conforms(self):
        repo_root = BASE.parents[2]
        self.assertEqual([], package_checker.validate_manifest(repo_root))

    def test_construction_package_mutation_rejected(self):
        repo_root = BASE.parents[2]
        with tempfile.TemporaryDirectory() as temp:
            copy_root = Path(temp) / "repo"
            shutil.copytree(repo_root / "experiments", copy_root / "experiments")
            (copy_root / ".github/workflows").mkdir(parents=True)
            shutil.copy2(
                repo_root / ".github/workflows/kubernetes-longitudinal-observation-v0-1.yml",
                copy_root / ".github/workflows/kubernetes-longitudinal-observation-v0-1.yml",
            )
            target = copy_root / BASE.relative_to(repo_root) / "README.md"
            target.write_text(target.read_text(encoding="utf-8") + "\nmutation\n", encoding="utf-8")
            findings = package_checker.validate_manifest(copy_root)
            self.assertTrue(any("DIGEST_MISMATCH" in item for item in findings))


if __name__ == "__main__":
    unittest.main()
