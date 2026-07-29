#!/usr/bin/env python3
"""Validate the proof-first public-route successor candidate."""

from __future__ import annotations

import json
import math
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = "723aa9aee8c329f760bcdabd323fd471a916e822"
ROUTE_PATH = Path("docs/state/FORK_STATE_ROUTING_v0_4.json")
PROJECTION_PATH = Path("docs/state/FORK_PUBLIC_ROUTE_CURRENT_PROJECTION_v0_1.json")
HISTORICAL_CONTRACT = Path(
    "docs/proof-atlas/"
    "PROOF-001-review-does-not-silently-travel-v0.1/"
    "PUBLIC-ROUTE-FRESHNESS-CONTRACT.json"
)
README_PATH = Path("README.md")
PROOF_ATLAS = "docs/proof-atlas/README.md"
PROOF_001 = (
    "docs/proof-atlas/"
    "PROOF-001-review-does-not-silently-travel-v0.1/README.md"
)
SHA1_RE = re.compile(r"^[0-9a-f]{40}$")


class DuplicateKeyError(ValueError):
    pass


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number: {value}")


def assert_finite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("non-finite JSON number")
    if isinstance(value, dict):
        for child in value.values():
            assert_finite(child)
    elif isinstance(value, list):
        for child in value:
            assert_finite(child)


def strict_load(path: Path) -> Any:
    with (ROOT / path).open("r", encoding="utf-8") as handle:
        value = json.load(
            handle,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_constant,
        )
    assert_finite(value)
    return value


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if check and completed.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed ({completed.returncode}): "
            f"{completed.stderr.strip()}"
        )
    return completed


def evaluate() -> dict[str, Any]:
    findings: list[dict[str, str]] = []

    def add(code: str, detail: str, path: str) -> None:
        findings.append({"code": code, "detail": detail, "path": path})

    try:
        route = strict_load(ROUTE_PATH)
        projection = strict_load(PROJECTION_PATH)
        historical = strict_load(HISTORICAL_CONTRACT)
        readme = (ROOT / README_PATH).read_text(encoding="utf-8")
    except Exception as exc:
        return {
            "status": "PUBLIC_PROOF_FIRST_ROUTE_SUCCESSOR_CANDIDATE_INVALID",
            "findings": [
                {"code": "ROUTE_INPUT_INVALID", "detail": str(exc), "path": "$input"}
            ],
        }

    if route.get("route_id") != "FORK_STATE_ROUTING_v0_4":
        add("ROUTE_ID_MISMATCH", "unexpected route identifier", ROUTE_PATH.as_posix())
    governed = route.get("governed_projection", {})
    if (
        governed.get("path") != PROJECTION_PATH.as_posix()
        or governed.get("source_commit") != CHECKPOINT
    ):
        add(
            "GOVERNED_ROUTE_COORDINATE_MISMATCH",
            "v0.4 governed route does not bind the exact checkpoint and projection",
            ROUTE_PATH.as_posix(),
        )

    source = projection.get("source_coordinate", {})
    if (
        source.get("branch") != "preservation/clean-continuance-v0.1"
        or source.get("commit_sha") != CHECKPOINT
        or projection.get("projection_scope")
        != "PUBLIC_DISCOVERY_AND_PROOF_ROUTING_ONLY"
    ):
        add(
            "PUBLIC_ROUTE_PROJECTION_MISMATCH",
            "narrow projection source or scope changed",
            PROJECTION_PATH.as_posix(),
        )

    pattern = re.compile(
        re.escape("preservation/clean-continuance-v0.1")
        + r"@([0-9a-f]{40})"
    )
    coordinates = pattern.findall(readme)
    if coordinates != [CHECKPOINT]:
        add(
            "README_COORDINATE_MISMATCH",
            f"expected one checkpoint coordinate, found {coordinates!r}",
            README_PATH.as_posix(),
        )
    for required in (PROOF_ATLAS, PROOF_001, ROUTE_PATH.as_posix()):
        if required not in readme:
            add(
                "README_PROOF_ROUTE_MISSING",
                f"missing public route {required}",
                README_PATH.as_posix(),
            )

    proof_route = route.get("proof_atlas", {})
    if (
        proof_route.get("index_path") != PROOF_ATLAS
        or proof_route.get("first_proof_path") != PROOF_001
    ):
        add(
            "PROOF_ATLAS_ROUTE_MISMATCH",
            "Proof Atlas or Proof 001 route changed",
            ROUTE_PATH.as_posix(),
        )

    observation = historical.get("observation", {})
    if (
        observation.get("commit_sha")
        != "a273ab0a95decb0d43f1c091743a72ac4261027e"
        or historical.get("expected_status") != "PUBLIC_ROUTE_STALE"
    ):
        add(
            "HISTORICAL_STALE_OBSERVATION_NOT_PRESERVED",
            "Proof 001 historical route standing changed",
            HISTORICAL_CONTRACT.as_posix(),
        )

    try:
        observed = run_git("rev-parse", f"{CHECKPOINT}^{{commit}}").stdout.strip()
        if observed != CHECKPOINT or SHA1_RE.fullmatch(observed) is None:
            add("CHECKPOINT_UNAVAILABLE", f"found {observed!r}", "$git")
        head = run_git("rev-parse", "HEAD").stdout.strip()
        descendant = run_git(
            "merge-base", "--is-ancestor", CHECKPOINT, head, check=False
        )
        if descendant.returncode != 0:
            add(
                "CANDIDATE_NOT_DESCENDED_FROM_CHECKPOINT",
                f"HEAD {head} is not descended from {CHECKPOINT}",
                "$git",
            )
        for path in (PROOF_ATLAS, PROOF_001):
            exists = run_git("cat-file", "-e", f"{CHECKPOINT}:{path}", check=False)
            if exists.returncode != 0:
                add(
                    "CHECKPOINT_PROOF_ROUTE_UNAVAILABLE",
                    f"{path} not available at checkpoint",
                    "$git",
                )
    except Exception as exc:
        add("GIT_BINDING_UNRESOLVED", str(exc), "$git")

    effects = projection.get("effects", {})
    if (
        effects.get("evidence_standing") != "NONE"
        or effects.get("review_standing") != "NONE"
        or effects.get("authority_state") != "NONE"
        or effects.get("execution_state") != "NONE"
        or effects.get("provider_calls") != 0
        or effects.get("pair_001_calls") != 0
    ):
        add(
            "ROUTING_EFFECT_WIDENED",
            "one or more required routing non-effects changed",
            PROJECTION_PATH.as_posix(),
        )

    status = (
        "PUBLIC_PROOF_FIRST_ROUTE_SUCCESSOR_CANDIDATE_CONFORMS_NOT_ADMITTED"
        if not findings
        else "PUBLIC_PROOF_FIRST_ROUTE_SUCCESSOR_CANDIDATE_INVALID"
    )
    return {
        "checker": Path(__file__).name,
        "status": status,
        "checkpoint": CHECKPOINT,
        "findings": findings,
        "non_claims": [
            "Route conformance is not self-admission.",
            "The routing-only successor does not create a new evidentiary checkpoint.",
            "Historical PUBLIC_ROUTE_STALE evidence remains preserved.",
            "Routing does not establish truth, correctness, authority, approval, compliance, legal sufficiency, safety, production readiness, present reliance, or execution permission.",
        ],
    }


def main() -> int:
    result = evaluate()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not result["findings"] else 1


if __name__ == "__main__":
    sys.exit(main())
