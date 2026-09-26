#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any

ROUTING = Path("docs/state/CURRENT_STATE_ROUTING_v0_2.json")
PREDECESSOR_ROUTING = Path("docs/state/CURRENT_STATE_ROUTING_v0_1.json")
README = Path("README.md")
CURRENT_STANDING = Path("CURRENT_STANDING.md")
CURRENT_DIR_README = Path("docs/current-standing/README.md")


def repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists() and (candidate / "README.md").exists():
            return candidate
    raise RuntimeError("Repository root not found")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def finish(checks):
    failed = [x for x in checks if not x["passed"]]
    return {
        "checker": Path(__file__).name,
        "total": len(checks),
        "passed": len(checks) - len(failed),
        "failed": len(failed),
        "checks": checks,
        "interpretation": {
            "proves": [
                "the preserved v0.1 routing record remains byte-identical and v0.2 is an additive successor",
                "v0.9 remains the repository-wide program-standing route at its own bounded coordinate",
                "FORK_II_CURRENT_STANDING_001 is exact-hash bound as the authoritative Fork II orientation subroute",
                "the Fork II orientation does not promote indexed objects and preserves its bounded-world/external-behavior boundary",
                "human entry points and machine routing agree on the global-route/subroute distinction"
            ],
            "does_not_prove": [
                "semantic completeness", "truth", "compliance", "legal sufficiency", "authorization",
                "production readiness", "institutional authority", "external behavioral validation"
            ]
        }
    }


def evaluate(root: Path) -> dict[str, Any]:
    checks = []
    def record(name, passed, detail):
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    if not (root / ROUTING).is_file():
        record("routing_v0_2_present", False, ROUTING.as_posix())
        return finish(checks)
    routing = load(root / ROUTING)
    record("routing_v0_2_present", True, ROUTING.as_posix())

    pred = routing.get("predecessor_routing", {})
    pred_path = root / str(pred.get("path", ""))
    record(
        "predecessor_routing_exact",
        pred_path == root / PREDECESSOR_ROUTING and pred_path.is_file() and git_blob_sha(pred_path) == pred.get("git_blob_sha"),
        f"path={pred.get('path')} blob={git_blob_sha(pred_path) if pred_path.is_file() else 'missing'}"
    )

    program = routing.get("current_program_standing", {})
    program_path = root / str(program.get("path", ""))
    if not program_path.is_file():
        record("global_program_route_present", False, str(program.get("path")))
    else:
        current = load(program_path)
        coord = routing.get("current_repository_coordinate", {})
        ok = (
            current.get("schema_id") == program.get("schema_id")
            and current.get("snapshot_date") == program.get("snapshot_date")
            and current.get("snapshot_base_commit") == coord.get("commit")
            and current.get("snapshot_through_pr") == coord.get("through_pr")
        )
        record("global_program_route_preserved", ok, f"{current.get('schema_id')} @ {coord.get('commit')}")

    fork2 = routing.get("fork_ii_orientation", {})
    md = root / str(fork2.get("markdown_path", ""))
    js = root / str(fork2.get("json_path", ""))
    record("fork_ii_orientation_files_present", md.is_file() and js.is_file(), f"md={md.is_file()} json={js.is_file()}")
    if md.is_file() and js.is_file():
        data = load(js)
        record("fork_ii_orientation_hash_bound",
               sha256(md) == fork2.get("markdown_sha256") and sha256(js) == fork2.get("json_sha256"),
               f"md={sha256(md)} json={sha256(js)}")
        record("fork_ii_orientation_identity",
               data.get("object_id") == fork2.get("object_id")
               and data.get("classification") == fork2.get("classification")
               and data.get("standing_effect") == fork2.get("standing_effect"),
               f"object={data.get('object_id')} classification={data.get('classification')}")
        record("fork_ii_observation_coordinate",
               data.get("main_coordinate") == routing.get("routing_observation_coordinate", {}).get("commit")
               and data.get("main_coordinate") == fork2.get("observed_main_coordinate"),
               str(data.get("main_coordinate")))
        pred_orientation = data.get("predecessor_orientation", {})
        record("fork_ii_additive_predecessor",
               pred_orientation.get("register") == fork2.get("predecessor_program_orientation")
               and pred_orientation.get("coordinate") == fork2.get("predecessor_program_coordinate")
               and pred_orientation.get("relationship") == "ADDITIVE_SYNCHRONIZATION_NOT_REWRITE",
               str(pred_orientation))
        closure = data.get("bounded_world_closure", {})
        record("bounded_world_closure_boundary",
               closure.get("disposition") == "SUPPORTED_IN_BOUNDED_MECHANISTIC_PILOT__CLOSED"
               and closure.get("external_behavioral_validation") == "NOT_ESTABLISHED",
               str(closure))
        successor = data.get("next_successor", {})
        record("external_successor_noninheritance",
               successor.get("state") == "OPENED_NOT_EXECUTED" and successor.get("standing_inheritance") == "NONE",
               str(successor))

    missing = [p for p in routing.get("fork_ii_companion_records", []) if not (root / p).is_file()]
    record("fork_ii_companion_records_present", not missing, "all present" if not missing else ", ".join(missing))

    cs = (root / CURRENT_STANDING).read_text(encoding="utf-8")
    record("top_level_routes_fork_ii_subroute",
           "FORK_II_CURRENT_STANDING_001_20260926.md" in cs
           and "CURRENT_STATE_ROUTING_v0_2.json" in cs
           and "authoritative Fork II orientation subroute" in cs,
           "CURRENT_STANDING.md names the Fork II subroute and v0.2 machine route")
    record("top_level_preserves_global_v0_9",
           "FORK_CURRENT_WORK_REGISTER_v0_9" in cs and "repository-wide" in cs,
           "v0.9 remains the global program route")

    dr = (root / CURRENT_DIR_README).read_text(encoding="utf-8")
    record("current_directory_routes_fork_ii_subroute",
           "FORK_II_CURRENT_STANDING_001_20260926.md" in dr and "CURRENT_STATE_ROUTING_v0_2.json" in dr,
           "docs/current-standing/README.md exposes the Fork II subroute")

    readme = (root / README).read_text(encoding="utf-8")
    record("root_readme_routes_to_current_standing", "[`CURRENT_STANDING.md`](CURRENT_STANDING.md)" in readme,
           "README continues to route reviewers through CURRENT_STANDING.md")

    record("routing_nonpromotion_boundary",
           "AUTHORITATIVE_FORK_II_ORIENTATION != GLOBAL_PROGRAM_REGISTER_REPLACEMENT" in routing.get("non_claims", [])
           and "INDEX_ENTRY != STANDING_PROMOTION" in routing.get("non_claims", []),
           "authority is scoped to orientation, not underlying standing")

    return finish(checks)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=Path.cwd())
    p.add_argument("--json", action="store_true", dest="as_json")
    a = p.parse_args()
    result = evaluate(repo_root(a.root))
    if a.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for item in result["checks"]:
            print(f"[{'PASS' if item['passed'] else 'FAIL'}] {item['name']}: {item['detail']}")
        print("CURRENT_STATE_ROUTING_V0_2_PASS" if result["failed"] == 0 else "CURRENT_STATE_ROUTING_V0_2_FAIL")
    return 1 if result["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
