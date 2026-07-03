#!/usr/bin/env python3
"""Deterministic comparison data builder for AHI Viewer v0.2.

Reads:
  docs/viewer/ahi-viewer-v0_1/data/scenarios_bundle.json

Writes:
  docs/viewer/ahi-viewer-v0_2/data/comparison_pairs.json

This builder is static and deterministic. It does not call external services.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SOURCE_BUNDLE = Path("docs/viewer/ahi-viewer-v0_1/data/scenarios_bundle.json")
OUT = Path("docs/viewer/ahi-viewer-v0_2/data/comparison_pairs.json")

CANONICAL_PAIRS: list[dict[str, Any]] = [
    {
        "pair_id": "PAIR-S01-S02",
        "label": "Scenario 01 vs Scenario 02 — baseline versus preserved handoff",
        "left_scenario_id": "SCENARIO_01_BASELINE_UNBOUNDED_HANDOFF",
        "right_scenario_id": "SCENARIO_02_FORK_PRESERVED_HANDOFF",
        "comparison_posture": "BOUNDARY_PRESERVATION_COMPARISON",
        "purpose": "Show the difference between an unbounded AI-assisted handoff and a Fork-preserved handoff.",
        "boundary_movement": [
            "Scenario 01 shows insufficient boundary preservation.",
            "Scenario 02 introduces explicit claim boundary and non-claim preservation.",
        ],
        "attempted_inference": [
            "Scenario 01 allows downstream ambiguity about what the artifact supports.",
            "Scenario 02 records what must not be inferred.",
        ],
        "required_revalidation": [
            "Scenario 02 preserves unresolved requirements rather than converting them into authority-bearing conclusions.",
        ],
        "fork_can_show": [
            "whether a boundary record exists",
            "whether non-claims are preserved",
            "whether artifact paths remain inspectable",
        ],
        "fork_does_not_show": [
            "truth of the upstream claim",
            "approval",
            "compliance",
            "legal sufficiency",
            "correctness",
        ],
        "reviewer_use": [
            "Use this pair to understand Fork's basic difference from an ordinary audit trail or unbounded handoff.",
        ],
    },
    {
        "pair_id": "PAIR-S03-S04",
        "label": "Scenario 03 vs Scenario 04 — scope expansion versus authority leakage",
        "left_scenario_id": "SCENARIO_03_SCOPE_EXPANSION_ATTEMPT",
        "right_scenario_id": "SCENARIO_04_AUTHORITY_LEAKAGE_ATTEMPT",
        "comparison_posture": "EXPANSION_AND_AUTHORITY_COMPARISON",
        "purpose": "Compare claim scope expansion with authority-context leakage.",
        "boundary_movement": [
            "Scenario 03 tests whether a narrow claim silently becomes broader downstream.",
            "Scenario 04 tests whether authority context is improperly inherited.",
        ],
        "attempted_inference": [
            "Narrow claim treated as broad claim.",
            "Authority possessed or referenced treated as authority exercised for a specific reliance decision.",
        ],
        "required_revalidation": [
            "Expanded claim scope requires fresh support.",
            "Authority-bearing reliance requires authority context specific to the decision, policy, purpose, and time window.",
        ],
        "fork_can_show": [
            "whether scope was expanded",
            "whether authority context leaked",
            "whether the expansion or leakage was unsupported",
        ],
        "fork_does_not_show": [
            "whether the broader claim is true",
            "whether authority legally existed",
            "whether authority was validly exercised",
            "whether the downstream decision was correct",
        ],
        "reviewer_use": [
            "Use this pair to distinguish semantic claim expansion from authority-context inheritance.",
        ],
    },
    {
        "pair_id": "PAIR-S05-S06",
        "label": "Scenario 05 vs Scenario 06 — policy laundering versus distributed handoff",
        "left_scenario_id": "SCENARIO_05_POLICY_REFERENCE_LAUNDERING_ATTEMPT",
        "right_scenario_id": "SCENARIO_06_MULTI_SYSTEM_DISTRIBUTED_HANDOFF",
        "comparison_posture": "POLICY_AND_DISTRIBUTED_AUTHORITY_COMPARISON",
        "purpose": "Compare policy-reference laundering with distributed authority inheritance across multiple systems.",
        "boundary_movement": [
            "Scenario 05 tests policy reference treated as policy satisfaction.",
            "Scenario 06 tests authority inheritance across a multi-system handoff.",
        ],
        "attempted_inference": [
            "Policy cited, therefore policy satisfied.",
            "Distributed handoff produced a routing or approval authority conclusion.",
        ],
        "required_revalidation": [
            "Policy satisfaction requires separate support.",
            "Approval authority, policy satisfaction, and execution eligibility require separate authority and revalidation.",
        ],
        "fork_can_show": [
            "whether non-claims were suppressed",
            "whether policy reference was promoted",
            "whether distributed authority inference was attempted",
            "whether required revalidation remained visible",
        ],
        "fork_does_not_show": [
            "policy satisfaction",
            "compliance",
            "approval authority",
            "execution eligibility",
            "correctness",
        ],
        "reviewer_use": [
            "Use this pair to see the transition from a single-document semantic failure to a multi-system transition failure.",
        ],
    },
    {
        "pair_id": "PAIR-S06-S07",
        "label": "Scenario 06 vs Scenario 07 — internal distributed boundary versus external authority bridge",
        "left_scenario_id": "SCENARIO_06_MULTI_SYSTEM_DISTRIBUTED_HANDOFF",
        "right_scenario_id": "SCENARIO_07_EXTERNAL_AUTHORITY_BRIDGE",
        "comparison_posture": "INTERNAL_TO_EXTERNAL_AUTHORITY_COMPARISON",
        "purpose": "Compare internal distributed authority inheritance with an external authority bridge attempt.",
        "boundary_movement": [
            "Scenario 06 tests authority non-inheritance inside a multi-system internal workflow.",
            "Scenario 07 tests whether internal record inspectability is treated as external authority.",
        ],
        "attempted_inference": [
            "Internal routing or summary treated as approval authority.",
            "Inspectable Fork record treated as external admissibility, compliance, approval, legal sufficiency, acceptance, or execution eligibility.",
        ],
        "required_revalidation": [
            "Internal approval authority requires separate decision support.",
            "External admissibility, compliance, legal sufficiency, acceptance, and execution eligibility require separate external authority, rule, standard, or decision process.",
        ],
        "fork_can_show": [
            "whether internal authority inheritance was attempted",
            "whether external authority bridge inference was attempted",
            "whether external revalidation requirements were preserved",
        ],
        "fork_does_not_show": [
            "external admissibility",
            "regulatory compliance",
            "legal sufficiency",
            "customer acceptance",
            "board authorization",
            "insurance coverage",
            "execution eligibility",
        ],
        "reviewer_use": [
            "Use this pair to distinguish internal transition-state failure from external authority-bridge overclaim.",
        ],
    },
]


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    if not SOURCE_BUNDLE.exists():
        raise SystemExit(f"missing source bundle: {SOURCE_BUNDLE}")

    bundle = read_json(SOURCE_BUNDLE)
    scenarios = bundle.get("scenarios", [])
    scenario_ids = {s.get("scenario_id") for s in scenarios if isinstance(s, dict)}

    pairs = [
        pair for pair in CANONICAL_PAIRS
        if pair["left_scenario_id"] in scenario_ids and pair["right_scenario_id"] in scenario_ids
    ]

    output = {
        "artifact_type": "AHI_VIEWER_COMPARISON_PAIRS",
        "artifact_version": "0.2",
        "generation_mode": "deterministic",
        "source_bundle": str(SOURCE_BUNDLE).replace("\\", "/"),
        "viewer": "docs/viewer/ahi-viewer-v0_2/index.html",
        "source_scenario_count": len(scenarios),
        "comparison_pair_count": len(pairs),
        "non_authority_statement": (
            "Viewer v0.2 does not approve, certify, score, authorize, determine compliance, "
            "determine admissibility, establish legal sufficiency, decide acceptance, or judge correctness."
        ),
        "comparison_pairs": pairs,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
