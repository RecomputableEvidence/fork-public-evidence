#!/usr/bin/env python3
"""Recompute Fork Proof 001 from the admitted v0.2 replay lineage."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import stat
import sys
from typing import Any


PROOF_ID = "PROOF-001"
PACKAGE_ROOT = Path(
    "docs/proof-atlas/"
    "PROOF-001-review-does-not-silently-travel-v0.1"
)
MANIFEST_PATH = PACKAGE_ROOT / "PROOF-MANIFEST.json"
STANDING_PATH = PACKAGE_ROOT / "STANDING.json"
SUMMARY_PATH = PACKAGE_ROOT / "PROOF-SUMMARY.md"
ROUTE_CONTRACT_PATH = PACKAGE_ROOT / "PUBLIC-ROUTE-FRESHNESS-CONTRACT.json"
PROOF_INDEX_PATH = Path("docs/proof-atlas/PROOF_INDEX_v0_1.json")
LONGITUDINAL_CHECKER_PATH = Path(
    "tools/check_longitudinal_recomputation_v0_2.py"
)
ROUTE_CHECKER_PATH = Path("tools/check_public_route_freshness_v0_1.py")

REPLAY_START = "bac40d9bdbd7f6b4927a676fef8def70756ad9d5"
REPLAY_CLOSURE = "f955834681d2f2ee257276acbf68afde0ae0e69d"
PR91_HEAD = "e848ea0825bafc1aa3754d89e719d71b5a9f3982"
PR91_TREE = "0b5f11eb6c1cd8c90b4cacce2a747045da917741"
PR91_MERGE = "9f65a3b3d0dda3a0116a6438a6e24118ff63fddb"
PR97_ADMISSION_MERGE = "9c779c305be8455f355051a561e9ea89e7feee36"
CONSTRUCTION_BASE = "96e17cd5ae8a923b9074cfdfe6718cf0e15611b0"
CONSTRUCTION_TREE = "a9addcb4903ce4e4098a7f554cef85bc60e2ccb8"

EXPECTED_PACKAGE_FILES = {
    (PACKAGE_ROOT / "PROOF-MANIFEST.json").as_posix(),
    (PACKAGE_ROOT / "PROOF-SUMMARY.md").as_posix(),
    (PACKAGE_ROOT / "PUBLIC-ROUTE-FRESHNESS-CONTRACT.json").as_posix(),
    (PACKAGE_ROOT / "README.md").as_posix(),
    (PACKAGE_ROOT / "STANDING.json").as_posix(),
}

EXPECTED_BINDING_PATHS = {
    (PACKAGE_ROOT / "PROOF-SUMMARY.md").as_posix(),
    (PACKAGE_ROOT / "PUBLIC-ROUTE-FRESHNESS-CONTRACT.json").as_posix(),
    (PACKAGE_ROOT / "README.md").as_posix(),
    (PACKAGE_ROOT / "STANDING.json").as_posix(),
    "docs/proof-atlas/PROOF_INDEX_v0_1.json",
    "docs/proof-atlas/README.md",
    (
        "docs/evidence/tp-001/admission/"
        "PR98-ADMISSION-ANCHOR-001/ADMISSION-ANCHOR.json"
    ),
    (
        "docs/exterior-observations/reviews/pr91-chatgpt-20260724/"
        "EXTERIOR_RECOMPUTATION_RECEIPT_PR91_CHATGPT_20260724_NORMALIZED_v0_1_1.json"
    ),
    (
        "docs/exterior-observations/reviews/pr91-chatgpt-20260724/"
        "ORIGINAL_EXTERIOR_RECOMPUTATION_RECEIPT_PR91_CHATGPT_20260724_v0_1.json"
    ),
    (
        "docs/preservation/admission/"
        "FORK_LONGITUDINAL_OBSERVATION_ADMISSION_ANCHOR_2026_07_26_v0_1.json"
    ),
    (
        "docs/preservation/admission/"
        "FORK_LONGITUDINAL_OBSERVATION_ADMISSION_ANCHOR_2026_07_26_v0_1.md"
    ),
    (
        "docs/state/longitudinal-recomputation-v0.2/"
        "ADVERSARIAL_CASES_v0_2.json"
    ),
    (
        "docs/state/longitudinal-recomputation-v0.2/"
        "LONGITUDINAL_EVENT_REGISTRY_v0_2.json"
    ),
    (
        "docs/state/longitudinal-recomputation-v0.2/"
        "LONGITUDINAL_REPLAY_CONTRACT_v0_2.json"
    ),
    (
        "receipts/claim-admission/"
        "FORK_CLAIM_ADMISSION_HARDENING_SELF_CHECK_RECEIPT_v0_1.json"
    ),
    "tests/test_longitudinal_recomputation_v0_2.py",
    "tests/test_proof_001_review_does_not_silently_travel_v0_1.py",
    "tools/check_longitudinal_recomputation_v0_2.py",
    "tools/check_public_route_freshness_v0_1.py",
    "tools/run_proof_001_review_does_not_silently_travel_v0_1.py",
}


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_regular_file(root: Path, relative: Any) -> Path:
    if not isinstance(relative, str) or not relative:
        raise ValueError("path must be a non-empty repository-relative string")
    pure = PurePosixPath(relative)
    if (
        pure.is_absolute()
        or "." in pure.parts
        or ".." in pure.parts
        or "\\" in relative
        or relative != pure.as_posix()
    ):
        raise ValueError(f"unsafe or non-canonical path: {relative!r}")
    root_real = root.resolve(strict=True)
    current = root
    for part in pure.parts:
        current = current / part
        mode = current.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise ValueError(f"symlink substitution rejected: {relative}")
    if not stat.S_ISREG(current.stat().st_mode):
        raise ValueError(f"not a regular file: {relative}")
    current.resolve(strict=True).relative_to(root_real)
    return current


def add_finding(
    findings: list[dict[str, str]],
    code: str,
    detail: str,
    path: str,
) -> None:
    findings.append({"code": code, "detail": detail, "path": path})


def validate_manifest(
    root: Path,
    longitudinal: Any,
    findings: list[dict[str, str]],
) -> dict[str, Any] | None:
    try:
        manifest = longitudinal.strict_load(
            safe_regular_file(root, MANIFEST_PATH.as_posix())
        )
    except Exception as exc:
        add_finding(
            findings,
            "PROOF_MANIFEST_INVALID",
            str(exc),
            MANIFEST_PATH.as_posix(),
        )
        return None
    if not isinstance(manifest, dict):
        add_finding(
            findings,
            "PROOF_MANIFEST_INVALID",
            "manifest must be an object",
            MANIFEST_PATH.as_posix(),
        )
        return None

    expected_self_exclusion = {
        "path": MANIFEST_PATH.as_posix(),
        "reason": "AVOIDS_CIRCULAR_FULL_FILE_DIGEST",
    }
    if manifest.get("self_exclusion") != expected_self_exclusion:
        add_finding(
            findings,
            "PROOF_MANIFEST_SELF_EXCLUSION_INVALID",
            f"expected {expected_self_exclusion!r}",
            MANIFEST_PATH.as_posix(),
        )
    if manifest.get("construction_base") != {
        "commit_sha": CONSTRUCTION_BASE,
        "tree_sha": CONSTRUCTION_TREE,
    }:
        add_finding(
            findings,
            "PROOF_CONSTRUCTION_BASE_MISMATCH",
            "manifest construction base differs from the declared exact checkpoint",
            MANIFEST_PATH.as_posix(),
        )

    actual_package_files = {
        path.relative_to(root).as_posix()
        for path in (root / PACKAGE_ROOT).rglob("*")
        if path.is_file()
    }
    if actual_package_files != EXPECTED_PACKAGE_FILES:
        add_finding(
            findings,
            "PROOF_PACKAGE_FILE_SET_MISMATCH",
            (
                f"expected {sorted(EXPECTED_PACKAGE_FILES)!r}, "
                f"found {sorted(actual_package_files)!r}"
            ),
            PACKAGE_ROOT.as_posix(),
        )

    bindings = manifest.get("bindings", [])
    if not isinstance(bindings, list):
        add_finding(
            findings,
            "PROOF_MANIFEST_INVALID",
            "bindings must be an array",
            MANIFEST_PATH.as_posix(),
        )
        return manifest
    listed: set[str] = set()
    for binding in bindings:
        if not isinstance(binding, dict):
            add_finding(
                findings,
                "PROOF_BINDING_INVALID",
                "binding must be an object",
                MANIFEST_PATH.as_posix(),
            )
            continue
        relative = binding.get("path")
        if not isinstance(relative, str):
            add_finding(
                findings,
                "PROOF_BINDING_INVALID",
                "binding path must be a string",
                MANIFEST_PATH.as_posix(),
            )
            continue
        if relative in listed:
            add_finding(
                findings,
                "PROOF_BINDING_DUPLICATE",
                "duplicate binding path",
                relative,
            )
            continue
        listed.add(relative)
        try:
            path = safe_regular_file(root, relative)
            observed_size = path.stat().st_size
            observed_sha256 = sha256_file(path)
            if binding.get("size_bytes") != observed_size:
                add_finding(
                    findings,
                    "PROOF_BINDING_SIZE_MISMATCH",
                    (
                        f"expected {binding.get('size_bytes')!r}, "
                        f"found {observed_size}"
                    ),
                    relative,
                )
            if binding.get("sha256") != observed_sha256:
                add_finding(
                    findings,
                    "PROOF_BINDING_DIGEST_MISMATCH",
                    (
                        f"expected {binding.get('sha256')!r}, "
                        f"found {observed_sha256}"
                    ),
                    relative,
                )
        except Exception as exc:
            add_finding(
                findings,
                "PROOF_BINDING_INVALID",
                str(exc),
                relative,
            )
    if listed != EXPECTED_BINDING_PATHS:
        add_finding(
            findings,
            "PROOF_BINDING_SET_MISMATCH",
            (
                f"expected {sorted(EXPECTED_BINDING_PATHS)!r}, "
                f"found {sorted(listed)!r}"
            ),
            MANIFEST_PATH.as_posix(),
        )
    return manifest


def validate_index(
    root: Path,
    longitudinal: Any,
    findings: list[dict[str, str]],
) -> dict[str, Any] | None:
    try:
        index = longitudinal.strict_load(
            safe_regular_file(root, PROOF_INDEX_PATH.as_posix())
        )
    except Exception as exc:
        add_finding(
            findings,
            "PROOF_INDEX_INVALID",
            str(exc),
            PROOF_INDEX_PATH.as_posix(),
        )
        return None
    proofs = index.get("proofs") if isinstance(index, dict) else None
    if not isinstance(proofs, list) or len(proofs) != 1:
        add_finding(
            findings,
            "PROOF_INDEX_INVALID",
            "v0.1 index must contain exactly one proof",
            PROOF_INDEX_PATH.as_posix(),
        )
        return index
    proof = proofs[0]
    expected = {
        "proof_id": PROOF_ID,
        "title": "A Review Does Not Silently Travel",
        "path": PACKAGE_ROOT.as_posix(),
        "manifest_path": MANIFEST_PATH.as_posix(),
        "standing_path": STANDING_PATH.as_posix(),
        "wrapper_path": Path(__file__).relative_to(root).as_posix(),
        "expected_result": (
            "PROOF_001_REPRODUCED_PACKAGING_CANDIDATE_NOT_ADMITTED"
        ),
        "packaging_standing": (
            "BOUNDED_NONSEMANTIC_PACKAGING_CANDIDATE_NOT_ADMITTED"
        ),
        "underlying_lineage_standing": (
            "ADMITTED_LINEAR_REPLAY_WITH_CORRECTION_REQUIRED_RETAINED"
        ),
        "exterior_recomputation_disposition": (
            "REPRODUCED_WITH_CORRECTION_REQUIRED"
        ),
    }
    if proof != expected:
        add_finding(
            findings,
            "PROOF_INDEX_ENTRY_MISMATCH",
            f"expected {expected!r}, found {proof!r}",
            PROOF_INDEX_PATH.as_posix(),
        )
    return index


def validate_standing(
    root: Path,
    longitudinal: Any,
    findings: list[dict[str, str]],
) -> dict[str, Any] | None:
    try:
        standing = longitudinal.strict_load(
            safe_regular_file(root, STANDING_PATH.as_posix())
        )
    except Exception as exc:
        add_finding(
            findings,
            "PROOF_STANDING_INVALID",
            str(exc),
            STANDING_PATH.as_posix(),
        )
        return None
    checks = (
        (
            standing.get("packaging_candidate", {}).get("standing"),
            "BOUNDED_NONSEMANTIC_PACKAGING_CANDIDATE_NOT_ADMITTED",
            "packaging standing",
        ),
        (
            standing.get("underlying_replay", {}).get("reviewed_head"),
            PR91_HEAD,
            "PR #91 reviewed head",
        ),
        (
            standing.get("underlying_replay", {}).get("reviewed_tree"),
            PR91_TREE,
            "PR #91 reviewed tree",
        ),
        (
            standing.get("underlying_replay", {}).get("merge_commit"),
            PR91_MERGE,
            "PR #91 merge",
        ),
        (
            standing.get("underlying_replay", {}).get("replay_start_commit"),
            REPLAY_START,
            "replay start",
        ),
        (
            standing.get("underlying_replay", {}).get("replay_closure_commit"),
            REPLAY_CLOSURE,
            "replay closure",
        ),
        (
            standing.get("underlying_replay", {}).get(
                "admission_effect_inside_replay_interval"
            ),
            "NONE",
            "replay admission effect",
        ),
        (
            standing.get("exterior_recomputation", {}).get("disposition"),
            "REPRODUCED_WITH_CORRECTION_REQUIRED",
            "exterior disposition",
        ),
        (
            standing.get("later_admission", {}).get("merge_commit"),
            PR97_ADMISSION_MERGE,
            "PR #97 admission merge",
        ),
        (
            standing.get("later_admission", {}).get("standing_after_merge"),
            "ADMITTED_LINEAR_REPLAY_WITH_CORRECTION_REQUIRED_RETAINED",
            "later admission standing",
        ),
        (
            standing.get("later_admission", {}).get(
                "retroactive_effect_inside_replay_interval"
            ),
            "NONE",
            "later admission retroactive effect",
        ),
    )
    for actual, expected, label in checks:
        if actual != expected:
            add_finding(
                findings,
                "PROOF_STANDING_MISMATCH",
                f"{label}: expected {expected!r}, found {actual!r}",
                STANDING_PATH.as_posix(),
            )

    normalized_path = standing.get("exterior_recomputation", {}).get(
        "normalized_receipt_path"
    )
    source_path = standing.get("exterior_recomputation", {}).get(
        "source_receipt_path"
    )
    try:
        normalized = longitudinal.strict_load(
            safe_regular_file(root, normalized_path)
        )
        if normalized.get("disposition") != "REPRODUCED_WITH_CORRECTION_REQUIRED":
            add_finding(
                findings,
                "EXTERIOR_RECEIPT_STANDING_MISMATCH",
                "normalized PR #91 disposition changed",
                str(normalized_path),
            )
        target = normalized.get("review_target", {})
        if (
            target.get("head_sha") != PR91_HEAD
            or target.get("tree_sha") != PR91_TREE
        ):
            add_finding(
                findings,
                "EXTERIOR_RECEIPT_TARGET_MISMATCH",
                "normalized PR #91 target coordinate changed",
                str(normalized_path),
            )
        adverse = normalized.get("measurements", {}).get(
            "adversarial_results", []
        )
        matches = [
            item
            for item in adverse
            if isinstance(item, dict)
            and item.get("case_id") == "FLR-ADV-003"
            and item.get("conforms") is True
            and "CURRENT_HEAD_REVIEW_STALE" in str(item.get("observed"))
        ]
        if len(matches) != 1:
            add_finding(
                findings,
                "EXTERIOR_ADVERSARIAL_BINDING_MISMATCH",
                "normalized PR #91 return no longer binds FLR-ADV-003",
                str(normalized_path),
            )
        if sha256_file(safe_regular_file(root, normalized_path)) != standing.get(
            "exterior_recomputation", {}
        ).get("normalized_receipt_sha256"):
            add_finding(
                findings,
                "EXTERIOR_RECEIPT_DIGEST_MISMATCH",
                "normalized receipt digest differs",
                str(normalized_path),
            )
        if sha256_file(safe_regular_file(root, source_path)) != standing.get(
            "exterior_recomputation", {}
        ).get("source_receipt_sha256"):
            add_finding(
                findings,
                "EXTERIOR_RECEIPT_DIGEST_MISMATCH",
                "source receipt digest differs",
                str(source_path),
            )
    except Exception as exc:
        add_finding(
            findings,
            "EXTERIOR_RECEIPT_INVALID",
            str(exc),
            str(normalized_path),
        )
    return standing


def derive_evidence(root: Path) -> tuple[dict[str, Any], str]:
    longitudinal = load_module(
        root / LONGITUDINAL_CHECKER_PATH,
        "fork_longitudinal_recomputation_for_proof_001",
    )
    route_checker = load_module(
        root / ROUTE_CHECKER_PATH,
        "fork_public_route_freshness_for_proof_001",
    )
    findings: list[dict[str, str]] = []

    replay = longitudinal.evaluate(root)
    if replay.get("status") != "LONGITUDINAL_STATE_REPRODUCED":
        add_finding(
            findings,
            "UNDERLYING_REPLAY_NOT_REPRODUCED",
            f"observed {replay.get('status')!r}",
            LONGITUDINAL_CHECKER_PATH.as_posix(),
        )
    delta = longitudinal.state_diff(root, REPLAY_START, REPLAY_CLOSURE)
    if delta.get("status") != "LONGITUDINAL_DIFF_REPRODUCED":
        add_finding(
            findings,
            "UNDERLYING_DIFF_NOT_REPRODUCED",
            f"observed {delta.get('status')!r}",
            LONGITUDINAL_CHECKER_PATH.as_posix(),
        )

    contract = longitudinal.strict_load(root / longitudinal.CONTRACT)
    registry = longitudinal.strict_load(root / longitudinal.REGISTRY)
    mutated_registry = copy.deepcopy(registry)
    mutated_registry["events"][0]["dimension_effects"]["verification_state"][
        "after"
    ]["standing"] = "CURRENT_HEAD_INDEPENDENTLY_RECOMPUTED"
    adverse = longitudinal.evaluate(
        root,
        contract_override=contract,
        registry_override=mutated_registry,
        verify_committed=False,
    )
    adverse_codes = sorted(set(adverse.get("finding_codes", [])))
    if (
        adverse.get("status") != "LONGITUDINAL_RECOMPUTATION_INVALID"
        or "CURRENT_HEAD_REVIEW_STALE" not in adverse_codes
    ):
        add_finding(
            findings,
            "ADVERSARIAL_REJECTION_NOT_REPRODUCED",
            (
                f"status={adverse.get('status')!r}; "
                f"finding_codes={adverse_codes!r}"
            ),
            (
                "docs/state/longitudinal-recomputation-v0.2/"
                "ADVERSARIAL_CASES_v0_2.json"
            ),
        )

    route = route_checker.evaluate(root)
    if route.get("status") != "PUBLIC_ROUTE_STALE":
        add_finding(
            findings,
            "PUBLIC_ROUTE_STALENESS_NOT_REPRODUCED",
            f"observed {route.get('status')!r}",
            ROUTE_CONTRACT_PATH.as_posix(),
        )
    if route.get("findings") or not route.get("expectation_matches"):
        add_finding(
            findings,
            "PUBLIC_ROUTE_CHECK_INVALID",
            (
                f"findings={route.get('findings')!r}; "
                f"expectation_matches={route.get('expectation_matches')!r}"
            ),
            ROUTE_CONTRACT_PATH.as_posix(),
        )

    transition = replay.get("transition_receipt") or {}
    evidence = {
        "proof_id": PROOF_ID,
        "source_replay_status": replay.get("status"),
        "diff_status": delta.get("status"),
        "replay_start": REPLAY_START,
        "replay_closure": REPLAY_CLOSURE,
        "dimension_deltas": transition.get("dimension_deltas", {}),
        "changed_dimensions": transition.get("changed_dimensions", []),
        "preserved_dimensions": transition.get("preserved_dimensions", []),
        "effects": delta.get("effects"),
        "adversarial": {
            "case_id": "FLR-ADV-003",
            "mutation": "PROMOTE_REVIEW_TO_CURRENT_HEAD",
            "status": adverse.get("status"),
            "finding_codes": adverse_codes,
            "required_code": "CURRENT_HEAD_REVIEW_STALE",
            "required_code_observed": "CURRENT_HEAD_REVIEW_STALE" in adverse_codes,
        },
        "public_route": {
            "status": route.get("status"),
            "expected_status": route.get("expected_status"),
            "expectation_matches": route.get("expectation_matches"),
            "latest_admitted_checkpoint": route.get(
                "latest_admitted_checkpoint"
            ),
            "routes": route.get("routes"),
        },
        "findings": findings,
    }
    return evidence, render_summary(evidence)


def render_summary(evidence: dict[str, Any]) -> str:
    lines = [
        "# PROOF-001 Generated Summary",
        "",
        "> Generated from the existing v0.2 longitudinal checker by",
        "> `tools/run_proof_001_review_does_not_silently_travel_v0_1.py`.",
        "",
        "## Exact replay",
        "",
        f"- Start: `{evidence['replay_start']}`",
        f"- Closure: `{evidence['replay_closure']}`",
        f"- Replay: `{evidence['source_replay_status']}`",
        f"- Diff: `{evidence['diff_status']}`",
        "",
        "## Changed and preserved dimensions",
        "",
        "| Dimension | T1 standing | Effect | T2 standing |",
        "|---|---|---|---|",
    ]
    for dimension, delta in evidence.get("dimension_deltas", {}).items():
        effect = "CHANGED" if delta.get("changed") else "PRESERVED"
        before = str(delta.get("before_standing")).replace("|", "\\|")
        after = str(delta.get("after_standing")).replace("|", "\\|")
        lines.append(
            f"| `{dimension}` | `{before}` | **{effect}** | `{after}` |"
        )
    lines.extend(
        [
            "",
            "Changed dimensions: "
            + ", ".join(
                f"`{item}`" for item in evidence.get("changed_dimensions", [])
            ),
            "",
            "Preserved dimensions: "
            + ", ".join(
                f"`{item}`" for item in evidence.get("preserved_dimensions", [])
            ),
            "",
            "## Adversarial demonstration",
            "",
            "- Case: `FLR-ADV-003`",
            "- Mutation: `PROMOTE_REVIEW_TO_CURRENT_HEAD`",
            "- Result: `CURRENT_HEAD_REVIEW_STALE`",
            "- Disposition: mutation rejected; review remains exact-head bound.",
            "",
            "## Public-route observation",
            "",
            f"- Result: `{evidence.get('public_route', {}).get('status')}`",
            "- Effect: routing gap detected and preserved; not repaired by this candidate.",
            "",
            "## Boundary",
            "",
            "The replay interval has admission, authority, and execution effects `NONE`.",
            "Later admission of the replay lineage does not rewrite the earlier interval.",
            "This summary does not establish truth, correctness, causality, endorsement,",
            "compliance, legal sufficiency, safety, production readiness, present reliance,",
            "institutional authority, or execution permission.",
            "",
        ]
    )
    return "\n".join(lines)


def evaluate_package(root: Path) -> dict[str, Any]:
    root = root.resolve()
    evidence, rendered_summary = derive_evidence(root)
    findings = list(evidence["findings"])
    longitudinal = load_module(
        root / LONGITUDINAL_CHECKER_PATH,
        "fork_longitudinal_recomputation_for_proof_001_package",
    )
    manifest = validate_manifest(root, longitudinal, findings)
    standing = validate_standing(root, longitudinal, findings)
    index = validate_index(root, longitudinal, findings)
    try:
        committed_summary = safe_regular_file(
            root, SUMMARY_PATH.as_posix()
        ).read_text(encoding="utf-8")
        if committed_summary != rendered_summary:
            add_finding(
                findings,
                "PROOF_SUMMARY_DIVERGENCE",
                "committed summary differs from deterministic rendering",
                SUMMARY_PATH.as_posix(),
            )
    except Exception as exc:
        add_finding(
            findings,
            "PROOF_SUMMARY_DIVERGENCE",
            str(exc),
            SUMMARY_PATH.as_posix(),
        )

    status = (
        "PROOF_001_REPRODUCED_PACKAGING_CANDIDATE_NOT_ADMITTED"
        if not findings
        else "PROOF_001_PACKAGING_CANDIDATE_INVALID"
    )
    return {
        "checker": Path(__file__).name,
        "proof_id": PROOF_ID,
        "status": status,
        "source_replay_status": evidence["source_replay_status"],
        "diff_status": evidence["diff_status"],
        "replay_start": evidence["replay_start"],
        "replay_closure": evidence["replay_closure"],
        "changed_dimensions": evidence["changed_dimensions"],
        "preserved_dimensions": evidence["preserved_dimensions"],
        "dimension_deltas": evidence["dimension_deltas"],
        "effects": evidence["effects"],
        "adversarial": evidence["adversarial"],
        "public_route": evidence["public_route"],
        "packaging_standing": (
            standing.get("packaging_candidate", {}).get("standing")
            if isinstance(standing, dict)
            else None
        ),
        "manifest_id": (
            manifest.get("manifest_id") if isinstance(manifest, dict) else None
        ),
        "index_id": index.get("index_id") if isinstance(index, dict) else None,
        "summary_sha256": hashlib.sha256(
            rendered_summary.encode("utf-8")
        ).hexdigest(),
        "findings": findings,
        "non_claims": [
            "Packaging conformance is not admission.",
            "The wrapper does not alter underlying evidence or standing.",
            "The result does not establish truth, correctness, causality, endorsement, compliance, legal sufficiency, safety, production readiness, present reliance, institutional authority, or execution permission.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--render-summary-only",
        action="store_true",
        help="Render the mechanically derived Markdown summary without package checks.",
    )
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    if args.render_summary_only:
        evidence, summary = derive_evidence(root)
        print(summary, end="")
        return 0 if not evidence["findings"] else 1

    result = evaluate_package(root)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        _, summary = derive_evidence(root)
        print(summary, end="")
        print(result["status"])
        if result["findings"]:
            for finding in result["findings"]:
                print(
                    f"{finding['code']}: {finding['detail']} "
                    f"({finding['path']})"
                )
    return 0 if not result["findings"] else 1


if __name__ == "__main__":
    sys.exit(main())
