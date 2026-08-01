#!/usr/bin/env python3
"""Generate the bounded PR #107 exact-coordinate repair in a CI worktree.

This helper mutates only the ephemeral checked-out worktree. It performs no
provider calls, does not move repository refs, and is removed before the final
repair commit is assembled through the GitHub connector.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
HISTORICAL_REQUEST = (
    "docs/experiments/cross-system-claim-handoff-v0.1/pre-execution/"
    "PROVIDER_VALIDATION_REQUEST_v0_1_2.json"
)
HISTORICAL_REQUEST_SHA = (
    "febce3875423d7c0cc293519e6ddd1b73a3cc6872a1b75a754aa3a07e5504865"
)
HISTORICAL_SNAPSHOT = (
    "docs/sequence-surface/historical/"
    "FSS-PAIR001-E009_PROVIDER_VALIDATION_REQUEST_v0_1_2.json"
)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one replacement target, found {count}")
    return text.replace(old, new, 1)


def git_file_bytes(commit: str, relative: str) -> bytes | None:
    completed = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{commit}:{relative}"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout if completed.returncode == 0 else None


def preserve_historical_provider_request() -> str:
    candidates = [
        "0e58a151cb5801f554619eb44a40948ad03e3e55",
        "1241c0084900f2c60f362205525464582e57b4a7",
        "96e17cd5ae8a923b9074cfdfe6718cf0e15611b0",
        "f955834681d2f2ee257276acbf68afde0ae0e69d",
        "8996a65d02952945062fdf1f29b75aa128d2f9f2",
    ]
    observed: list[str] = []
    for commit in candidates:
        data = git_file_bytes(commit, HISTORICAL_REQUEST)
        if data is None:
            observed.append(f"{commit}=ABSENT")
            continue
        digest = hashlib.sha256(data).hexdigest()
        observed.append(f"{commit}={digest}")
        if digest == HISTORICAL_REQUEST_SHA:
            snapshot = ROOT / HISTORICAL_SNAPSHOT
            snapshot.parent.mkdir(parents=True, exist_ok=True)
            snapshot.write_bytes(data)
            print(f"PR107_HISTORICAL_PROVIDER_BLOCK_COMMIT={commit}")
            return commit
    raise RuntimeError(
        "no bounded historical coordinate matches the event-9 provider request: "
        + "; ".join(observed)
    )


def patch_sequence_checker() -> None:
    historical_commit = preserve_historical_provider_request()
    path = ROOT / "tools/check_fork_sequence_surface_v0_1.py"
    text = path.read_text(encoding="utf-8")

    constant_marker = 'BASE_SEQUENCE_HEAD = "0e58a151cb5801f554619eb44a40948ad03e3e55"\n'
    constant_replacement = (
        constant_marker
        + f'HISTORICAL_PROVIDER_BLOCK_COMMIT = "{historical_commit}"\n'
        + f'HISTORICAL_PROVIDER_BLOCK_SNAPSHOT = Path("{HISTORICAL_SNAPSHOT}")\n'
    )
    text = replace_once(
        text,
        constant_marker,
        constant_replacement,
        "sequence historical snapshot constants",
    )

    old_digest_block = '''            elif sha256(artifact) != reference.get("sha256"):
                add_error(errors, "SOURCE_ARTIFACT_DIGEST_MISMATCH", str(reference.get("path")), ref_path)
'''
    new_digest_block = '''            elif sha256(artifact) != reference.get("sha256"):
                historical_snapshot = root / HISTORICAL_PROVIDER_BLOCK_SNAPSHOT
                historical_match = (
                    event_id == "FSS-PAIR001-E009"
                    and reference.get("path") == REQUEST.as_posix()
                    and reference.get("standing") == "CURRENT_BLOCKED_CONTROL"
                    and not historical_snapshot.is_symlink()
                    and historical_snapshot.is_file()
                    and sha256(historical_snapshot) == reference.get("sha256")
                )
                if not historical_match:
                    add_error(
                        errors,
                        "SOURCE_ARTIFACT_DIGEST_MISMATCH",
                        str(reference.get("path")),
                        ref_path,
                    )
'''
    text = replace_once(
        text,
        old_digest_block,
        new_digest_block,
        "sequence event-9 historical snapshot validation",
    )
    write_text(path, text)


def patch_temporal_checker() -> None:
    path = ROOT / "tools/check_temporal_succession_v0_1.py"
    text = path.read_text(encoding="utf-8")
    if "import subprocess\n" not in text:
        text = replace_once(
            text,
            "import stat\n",
            "import stat\nimport subprocess\n",
            "temporal import",
        )

    start_marker = '''        try:
            expect_equal(
                errors,
                sha256_file(safe_regular_file(root, path)),
                expected_digest,
                f"current source binding {path}",
            )
'''
    end_marker = '''        except Exception as exc:
            errors.append(f"current source binding {path}: {exc}")
'''
    start = text.find(start_marker)
    if start < 0:
        raise RuntimeError("temporal source-binding start block not found")
    end = text.find(end_marker, start)
    if end < 0:
        raise RuntimeError("temporal source-binding end block not found")
    end += len(end_marker)
    replacement = '''        try:
            source_bytes = subprocess.run(
                ["git", "-C", str(root), "show", f"{GOVERNED_COMMIT}:{path}"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ).stdout
            expect_equal(
                errors,
                hashlib.sha256(source_bytes).hexdigest(),
                expected_digest,
                f"current source binding {path}",
            )
        except Exception as exc:
            errors.append(f"current source binding {path}: {exc}")
'''
    text = text[:start] + replacement + text[end:]
    write_text(path, text)


def patch_thesis_checker() -> None:
    path = ROOT / "tools/check_fork_thesis_manifestation_v0_1.py"
    text = path.read_text(encoding="utf-8")
    insertion_point = '''    return result.stdout


def safe_regular_file(root: Path, rel: str) -> Path:
'''
    helper = '''    return result.stdout


def read_json_at_commit(root: Path, commit: str, rel: str) -> Any:
    value = json.loads(
        git_file_bytes(root, commit, rel).decode("utf-8"),
        object_pairs_hook=_object_no_duplicates,
        parse_constant=_reject_constant,
    )
    _assert_finite(value)
    return value


def safe_regular_file(root: Path, rel: str) -> Path:
'''
    if "def read_json_at_commit(" not in text:
        text = replace_once(
            text,
            insertion_point,
            helper,
            "thesis fixed-coordinate helper",
        )

    text = replace_once(
        text,
        '    provider = read_json("docs/experiments/cross-system-claim-handoff-v0.1/pre-execution/PROVIDER_VALIDATION_REQUEST_v0_1_2.json")\n',
        '    provider = read_json_at_commit(root, BASE_COMMIT, "docs/experiments/cross-system-claim-handoff-v0.1/pre-execution/PROVIDER_VALIDATION_REQUEST_v0_1_2.json")\n',
        "thesis provider fixed-coordinate read",
    )
    text = replace_once(
        text,
        '    projection = read_json("docs/sequence-surface/PAIR_001_SEQUENCE_PROJECTION_v0_1.json")\n',
        '    projection = read_json_at_commit(root, BASE_COMMIT, "docs/sequence-surface/PAIR_001_SEQUENCE_PROJECTION_v0_1.json")\n',
        "thesis projection fixed-coordinate read",
    )
    write_text(path, text)


def patch_longitudinal_checker() -> None:
    path = ROOT / "tools/check_longitudinal_recomputation_v0_2.py"
    text = path.read_text(encoding="utf-8")
    start = text.find("def derive_sequence_contribution(\n")
    end = text.find("\ndef validate_predecessor_temporal_surface(\n", start)
    if start < 0 or end < 0:
        raise RuntimeError("longitudinal sequence reducer boundaries not found")
    replacement = '''def derive_sequence_contribution(
    root: Path,
    findings: list[dict[str, str]],
) -> dict[str, Any]:
    projection_path = Path(
        "docs/sequence-surface/PAIR_001_SEQUENCE_PROJECTION_v0_1.json"
    )
    try:
        registry = strict_load(safe_regular_file(root, REGISTRY.as_posix()))
        closure = registry.get("coverage_interval", {}).get(
            "closure_commit_inclusive"
        )
        if not isinstance(closure, str) or SHA1_RE.fullmatch(closure) is None:
            raise ValueError("longitudinal closure commit is invalid")
        completed = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "show",
                f"{closure}:{projection_path.as_posix()}",
            ],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if completed.returncode != 0:
            detail = completed.stderr.decode("utf-8", errors="replace").strip()
            raise ValueError(
                f"cannot read sequence projection at {closure}: {detail}"
            )
        projection = json.loads(
            completed.stdout.decode("utf-8"),
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_constant,
        )
        assert_finite(projection)
    except Exception as exc:
        add_finding(
            findings,
            "SURFACE_REDUCER_FAILED",
            str(exc),
            projection_path.as_posix(),
        )
        return {}
    return {
        "standing": projection.get("publication_and_control", {}).get(
            "pre_execution_status"
        ),
        "reducer_id": "FORK_SEQUENCE_SURFACE_REDUCER_v0_1",
        "reducer_result": "SEQUENCE_SURFACE_CONFORMS_CANDIDATE_NOT_ADMITTED",
        "source": copy.deepcopy(projection.get("source")),
        "sequence": copy.deepcopy(projection.get("sequence")),
        "observed_history": copy.deepcopy(projection.get("observed_history")),
        "execution_boundary": copy.deepcopy(projection.get("execution_boundary")),
        "retry": copy.deepcopy(projection.get("retry")),
        "drift": copy.deepcopy(projection.get("drift")),
        "freshness": "DERIVED_FROM_BOUND_PRIMARY_EVIDENCE",
    }

'''
    text = text[:start] + replacement + text[end + 1 :]
    write_text(path, text)


def refresh_manifest(path: str, key: str) -> None:
    target = ROOT / path
    payload = json.loads(target.read_text(encoding="utf-8"))
    entries = payload.get(key)
    if not isinstance(entries, list):
        raise RuntimeError(f"{path}: {key} is not a list")
    for entry in entries:
        relative = entry.get("path")
        if not isinstance(relative, str):
            raise RuntimeError(f"{path}: entry lacks path")
        data = (ROOT / relative).read_bytes()
        entry["sha256"] = hashlib.sha256(data).hexdigest()
        if "size_bytes" in entry:
            entry["size_bytes"] = len(data)
    write_text(target, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def main() -> int:
    patch_sequence_checker()
    patch_temporal_checker()
    patch_thesis_checker()
    patch_longitudinal_checker()
    refresh_manifest(
        "docs/research/fork-thesis-manifestation-v0.1/PACKAGE_MANIFEST_v0_1.json",
        "entries",
    )
    print("PR107_EXACT_COORDINATE_SOURCE_REPAIR_WRITTEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
