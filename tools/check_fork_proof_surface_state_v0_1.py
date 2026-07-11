#!/usr/bin/env python3
"""Validate Fork's canonical proof-surface state and selected repository summaries."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "jsonschema is required. Install with: python -m pip install jsonschema"
    ) from exc

STATE_PATH = Path("docs/state/FORK_PROOF_SURFACE_STATE_v0_1.json")
SCHEMA_PATH = Path("schemas/fork_proof_surface_state_v0_1.schema.json")
SUMMARY_PATH = Path("docs/state/FORK_PROOF_SURFACE_STATE_SUMMARY_v0_1.md")
README_PATH = Path("README.md")
PROOF_SURFACE_PATH = Path("docs/CURRENT_PROOF_SURFACE_v0_1.md")
ROUNDS_INDEX_PATH = Path("docs/review/public-rounds/README.md")

HYPOTHESIS = "E[U | H = 1] < E[U | H = 0]"

STALE_PATTERNS = (
    "Day-0 replay receipt: not yet implemented",
    "Day-0 packet implemented; replay receipts not yet implemented",
    "Current round:\n- round-004/",
    "Current round:\r\n- round-004/",
    "Current round:\n- round-005/",
    "Current round:\r\n- round-005/",
    "Current round: - round-004/",
    "Current round: - round-005/",
)


def repository_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists() and (candidate / "README.md").exists():
            return candidate
    raise RuntimeError("Could not locate repository root containing .git and README.md")


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def render_summary(state: dict[str, Any]) -> str:
    lines = [
        "# Fork Proof-Surface State Summary v0.1",
        "",
        "This file is generated from `FORK_PROOF_SURFACE_STATE_v0_1.json`.",
        "",
        f"- As of: `{state['as_of_date']}`",
        f"- Current public-review round: `{state['current_public_review_round']}`",
        f"- Current recomputation surface: `{state['current_recomputation_surface']}`",
        f"- Current experimental phase: `{state['current_experimental_phase']}`",
        f"- Hypothesis expression: `{state['hypothesis_expression']}`",
        "",
        "## Surfaces",
        "",
        "| Surface | Implementation | Schema | Enforcement | External recomputation |",
        "|---|---|---|---|---|",
    ]
    for surface in state["surfaces"]:
        lines.append(
            "| {surface_id} | {implementation_status} | {schema_status} | "
            "{schema_enforcement_status} | {external_recomputation_status} |".format(
                **surface
            )
        )

    lines.extend(["", "## Known limitations", ""])
    for limitation in state["known_limitations"]:
        lines.append(
            f"- **{limitation['limitation_id']}** — "
            f"{limitation['status']}: {limitation['summary']}"
        )

    lines.extend(["", "## Invariant non-claims", ""])
    for item in state["invariant_non_claims"]:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "A synchronized state summary is repository hygiene evidence only. "
            "It does not establish truth, compliance, legal sufficiency, safety, "
            "authorization, approval, certification, endorsement, production readiness, "
            "or institutional authority.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--write-summary", action="store_true")
    parser.add_argument("--check-summary", action="store_true")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    root = repository_root(args.root)
    checks: list[dict[str, Any]] = []

    def record(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": passed, "detail": detail})

    state_path = root / STATE_PATH
    schema_path = root / SCHEMA_PATH

    try:
        state = read_json(state_path)
        schema = read_json(schema_path)
        Draft202012Validator.check_schema(schema)
        errors = sorted(
            Draft202012Validator(schema).iter_errors(state),
            key=lambda error: list(error.absolute_path),
        )
        record(
            "state_schema_validation",
            not errors,
            "valid" if not errors else "; ".join(error.message for error in errors),
        )
    except Exception as exc:
        record("state_schema_validation", False, str(exc))
        state = {}

    if state:
        surface_ids = [surface["surface_id"] for surface in state["surfaces"]]
        record(
            "surface_ids_unique",
            len(surface_ids) == len(set(surface_ids)),
            f"{len(surface_ids)} declared surface identifiers",
        )

        missing: list[str] = []
        for surface in state["surfaces"]:
            for relative in surface.get("required_artifacts", []):
                if not (root / relative).exists():
                    missing.append(f"{surface['surface_id']}: {relative}")
        record(
            "required_artifacts_exist",
            not missing,
            "all declared artifacts exist" if not missing else "; ".join(missing),
        )

        readme_text = (root / README_PATH).read_text(encoding="utf-8")
        record(
            "readme_hypothesis_sync",
            state.get("hypothesis_expression") in readme_text,
            "README contains canonical hypothesis expression",
        )

        rounds_text = (root / ROUNDS_INDEX_PATH).read_text(encoding="utf-8")
        expected_round = state.get("current_public_review_round", "")
        record(
            "public_round_index_sync",
            expected_round in rounds_text,
            f"public-round index references {expected_round}",
        )

        proof_text = (root / PROOF_SURFACE_PATH).read_text(encoding="utf-8")
        stale_found = [pattern for pattern in STALE_PATTERNS if pattern in proof_text or pattern in rounds_text]
        record(
            "known_status_contradictions_absent",
            not stale_found,
            "no known stale status pattern found"
            if not stale_found
            else "; ".join(stale_found),
        )

        expected_summary = render_summary(state)
        if args.write_summary:
            SUMMARY_PATH_ABS = root / SUMMARY_PATH
            SUMMARY_PATH_ABS.parent.mkdir(parents=True, exist_ok=True)
            SUMMARY_PATH_ABS.write_text(expected_summary, encoding="utf-8", newline="\n")
            record("summary_written", True, str(SUMMARY_PATH))

        if args.check_summary:
            summary_path = root / SUMMARY_PATH
            actual = summary_path.read_text(encoding="utf-8") if summary_path.exists() else ""
            record(
                "summary_sync",
                actual == expected_summary,
                "generated summary matches canonical state"
                if actual == expected_summary
                else "summary missing or stale; run with --write-summary",
            )

    failed = [check for check in checks if not check["passed"]]
    result = {
        "checker": Path(__file__).name,
        "state_path": str(STATE_PATH).replace("\\", "/"),
        "total": len(checks),
        "passed": len(checks) - len(failed),
        "failed": len(failed),
        "checks": checks,
        "interpretation": {
            "proves": [
                "the canonical state file satisfies its schema",
                "declared required artifacts are present",
                "selected summary surfaces are synchronized",
                "known stale-status patterns are absent",
            ],
            "does_not_prove": [
                "truth",
                "compliance",
                "legal sufficiency",
                "safety",
                "authorization",
                "approval",
                "certification",
                "endorsement",
                "production readiness",
                "institutional authority",
            ],
        },
    }

    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for check in checks:
            status = "PASS" if check["passed"] else "FAIL"
            print(f"[{status}] {check['name']}: {check['detail']}")
        print(
            "FORK_PROOF_SURFACE_STATE_CHECK_PASS"
            if not failed
            else "FORK_PROOF_SURFACE_STATE_CHECK_FAIL"
        )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
