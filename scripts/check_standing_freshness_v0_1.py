#!/usr/bin/env python3
"""Bounded change accounting, including predecessor-ledger closure; not semantic freshness."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from functools import lru_cache
from pathlib import Path

ACCOUNTING = "docs/current-standing/PROGRAM_CHANGE_ACCOUNTING_v0_2.json"
ROUTING = "docs/state/CURRENT_STATE_ROUTING_v0_1.json"
RECOGNIZED = ("admissions/", "docs/experiments/", "registries/", "receipts/", "schemas/", "tools/")
DISPOSITIONS = {"INCORPORATED", "EXPLICITLY_DEFERRED", "IN_FLIGHT"}


def git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.PIPE)


@lru_cache(maxsize=64)
def committed_blobs(root: Path, ref: str) -> dict[str, str]:
    result = {}
    for entry in git(root, "ls-tree", "-r", "-z", ref).split(b"\0"):
        if entry:
            meta, name = entry.split(b"\t", 1)
            _, kind, sha = meta.decode().split()
            if kind == "blob":
                result[name.decode("utf-8")] = sha
    return result


def blob_at(root: Path, ref: str, path: str) -> bytes:
    return git(root, "cat-file", "blob", committed_blobs(root, ref)[path])


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tree(root: Path, ref: str) -> dict[str, str]:
    result = {}
    for entry in git(root, "ls-tree", "-r", "-z", ref).split(b"\0"):
        if not entry:
            continue
        meta, name = entry.split(b"\t", 1)
        mode, kind, sha = meta.decode().split()
        path = name.decode("utf-8")
        if path.startswith(RECOGNIZED):
            if kind != "blob" or mode not in {"100644", "100755"}:
                raise ValueError(f"Unsupported recognized entry: {path} ({mode}/{kind})")
            result[path] = sha
    return result


def transitions(before: dict, after: dict) -> set[tuple]:
    return {(p, before.get(p), after.get(p)) for p in before.keys() | after.keys()
            if before.get(p) != after.get(p)}


def recognized_transitions_between(root: Path, base: str, end_ref: str) -> set[tuple]:
    """Inspect every first-parent transition from base through an exact committed end ref."""
    git(root, "merge-base", "--is-ancestor", base, end_ref)
    lineage = git(root, "rev-list", "--first-parent", end_ref).decode().splitlines()
    if base not in lineage:
        raise ValueError("Coverage base must be on the first-parent lineage of the closing ref")
    before = tree(root, base)
    result = set()
    for commit in reversed(lineage[:lineage.index(base)]):
        after = tree(root, commit)
        result |= transitions(before, after)
        before = after
    return result


def recognized_transitions(root: Path, base: str) -> set[tuple]:
    """Inspect every first-parent transition through HEAD plus the current checkout."""
    result = recognized_transitions_between(root, base, "HEAD")
    before = tree(root, "HEAD")
    candidates = set(before)
    for name in git(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard").split(b"\0"):
        if name and name.decode().startswith(RECOGNIZED):
            candidates.add(name.decode())
    after = {}
    for name in candidates:
        path = root / name
        if path.is_symlink():
            raise ValueError(f"Recognized symlink is unsupported: {name}")
        if path.is_file():
            after[name] = git(root, "hash-object", "--no-filters", "--", name).decode().strip()
    result |= transitions(before, after)
    return result


def acknowledged_transitions(rows: list[dict], errors: list[str], prefix: str) -> set[tuple]:
    acknowledged = set()
    for row in rows:
        key = (row["path"], row["before_git_blob"], row["after_git_blob"])
        if key in acknowledged:
            errors.append(f"Duplicate {prefix} accounting: {row['path']}")
        acknowledged.add(key)
        if row["disposition"] not in DISPOSITIONS or not row.get("reason", "").strip():
            errors.append(f"Missing {prefix} disposition/reason: {row['path']}")
        reference = row.get("standing_reference", "")
        if not reference or not reference.startswith("docs/current-standing/"):
            errors.append(f"Missing {prefix} standing explanation: {row['path']}")
    return acknowledged


def compare_accounting(actual: set[tuple], acknowledged: set[tuple], errors: list[str], prefix: str) -> None:
    for key in sorted(actual - acknowledged, key=str):
        errors.append(f"Unaccounted {prefix} recognized transition: {key}")
    for key in sorted(acknowledged - actual, key=str):
        errors.append(f"{prefix.capitalize()} accounting does not match observed transition: {key}")


def evaluate(root: Path) -> dict:
    errors = []
    try:
        accounting = load(root / ACCOUNTING)
        route = load(root / ROUTING)["current_program_standing"]["path"]
        standing = load(root / route)
        if accounting["standing_register"] != route:
            errors.append("Accounting does not name the current standing register")
        base = accounting["coverage_base_commit"]
        if base != standing["snapshot_base_commit"]:
            errors.append("Coverage base differs from standing snapshot base")

        predecessor = accounting["predecessor_accounting"]
        predecessor_path = predecessor["path"]
        closing_ref = predecessor["verified_through_commit"]
        predecessor_base = predecessor["coverage_base_commit"]
        if closing_ref != base:
            errors.append("Predecessor accounting does not close at the active coverage base")
        if predecessor_path == ACCOUNTING:
            errors.append("Predecessor accounting points to itself")
        declared_blob = predecessor["git_blob_sha"]
        if committed_blobs(root, closing_ref).get(predecessor_path) != declared_blob:
            errors.append("Predecessor accounting Git blob differs at closing coordinate")
        current_blob = git(root, "hash-object", "--no-filters", "--", predecessor_path).decode().strip()
        if current_blob != declared_blob:
            errors.append("Preserved predecessor accounting bytes changed after closure")
        predecessor_data = load(root / predecessor_path)
        if predecessor_data.get("coverage_base_commit") != predecessor_base:
            errors.append("Predecessor coverage base differs from successor closure declaration")
        predecessor_ack = acknowledged_transitions(predecessor_data["transitions"], errors, "predecessor")
        predecessor_actual = recognized_transitions_between(root, predecessor_base, closing_ref)
        compare_accounting(predecessor_actual, predecessor_ack, errors, "predecessor")

        actual = recognized_transitions(root, base)
        acknowledged = acknowledged_transitions(accounting["transitions"], errors, "active")
        for row in accounting["transitions"]:
            reference = row.get("standing_reference", "")
            if reference and not (root / reference).is_file():
                errors.append(f"Missing active standing explanation file: {row['path']}")
        compare_accounting(actual, acknowledged, errors, "active")

        binding = standing["observation"]
        observation_path = root / binding["path"]
        package = observation_path.parent
        if digest(observation_path.read_bytes()) != binding["sha256"]:
            errors.append("RLO observation binding differs")
        manifest = package / "SHA256SUMS"
        if digest(manifest.read_bytes()) != binding["manifest_sha256"]:
            errors.append("RLO manifest binding differs")
        expected = set()
        for line in manifest.read_text(encoding="utf-8").splitlines():
            sha, name = line.split("  ", 1)
            target = package / name
            if not target.resolve().is_relative_to(package.resolve()) or target.is_symlink():
                raise ValueError("Unsafe manifest path")
            if name in expected:
                errors.append(f"Duplicate RLO manifest path: {name}")
            expected.add(name)
            if digest(target.read_bytes()) != sha:
                errors.append(f"RLO preserved bytes differ: {name}")
        present = {p.relative_to(package).as_posix() for p in package.rglob("*") if p.is_file()}
        if present != expected | {"SHA256SUMS"}:
            errors.append("RLO manifest population differs")
        frozen = binding["preservation_commit"]
        git(root, "merge-base", "--is-ancestor", frozen, "HEAD")
        for name in expected | {"SHA256SUMS"}:
            relative = (package / name).relative_to(root).as_posix()
            if blob_at(root, frozen, relative) != (package / name).read_bytes():
                errors.append(f"RLO differs from preservation commit: {name}")
        frozen_paths = git(root, "ls-tree", "-r", "--name-only", frozen).decode().splitlines()
        if route in frozen_paths:
            errors.append("Successor already existed at observation preservation commit")
        for source in load(observation_path)["source_bindings"]:
            data = (package / source["preserved_copy"]).read_bytes()
            if digest(data) != source["sha256"]:
                errors.append(f"RLO source SHA-256 differs: {source['path']}")
            blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            if blob != source["git_blob_sha"]:
                errors.append(f"RLO source Git blob differs: {source['path']}")
            if source["commit"] == standing["admission_accounting"][-1]["commit"] and blob_at(root, source["commit"], source["path"]) != data:
                errors.append(f"RLO source differs from pinned source commit: {source['path']}")
        for event in standing["admission_accounting"]:
            git(root, "merge-base", "--is-ancestor", event["commit"], base)
        successor = next(x for x in standing["delta_objects"] if x["id"] == "CSH-S001-v0.1")
        if standing["delta_object_count"] != len(standing["delta_objects"]):
            errors.append("Standing delta population differs")
        routing_successor = load(root / ROUTING)["successor_candidate"]
        if (routing_successor["short_id"] != successor["id"] or
                routing_successor["status"] != "MEASUREMENT_AND_EXECUTION_RECORD_FROZEN__HOSTED_ACCESS_BLOCKED__RECEIVER_AND_RUN_ORDER_UNFROZEN"):
            errors.append("Routing and current CSH-S001 successor state differ")
        for source in successor["sources"]:
            data = blob_at(root, source["commit"], source["path"])
            if digest(data) != source["sha256"]:
                errors.append(f"Standing source differs: {source['path']}")
        if successor["receiver_registry_frozen"] or successor["run_order_frozen"] or successor["corpus_execution_established"]:
            errors.append("Bounded CSH-S001 successor state was promoted")
        if successor["remaining_blockers"] != ["G06", "G07", "G08", "G11"]:
            errors.append("CSH-S001 blocker state differs")
        run005 = next(x for x in standing["delta_objects"] if x["id"] == "FIVE-LAYER-HISTORICAL-LIVE-RUN-005-EXTERNAL-ADJUDICATION-001")
        if (run005["research_state"] != "EXTERNAL_ADJUDICATION_DISPATCH_PREPARED_NOT_RETURNED" or
                run005["external_result_repository_preserved"] or
                run005["external_result_repository_admitted"] or
                run005["stage_3_adjudication_delta"] != 0 or
                run005["synthetic_lane_opened"]):
            errors.append("Run 005 repository boundary was promoted")
    except (OSError, ValueError, KeyError, TypeError, StopIteration, subprocess.CalledProcessError) as exc:
        errors.append(f"Cannot establish structural accounting: {exc}")
    return {"status": "FAIL" if errors else "PASS", "errors": errors,
            "boundary": "Preserved predecessor accounting closes exactly through the active base, and post-base recognized first-parent Git blob transitions are accounted for; not semantic completeness, reviewer exposure, authorization, or universal freshness."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = evaluate(args.root.resolve())
    print(json.dumps(result, indent=2) if args.json else result)
    return int(result["status"] != "PASS")


if __name__ == "__main__":
    raise SystemExit(main())
