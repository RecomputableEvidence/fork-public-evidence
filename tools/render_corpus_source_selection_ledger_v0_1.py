#!/usr/bin/env python3
"""Render a non-canonical Markdown projection from the Corpus 001 ledger."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CANONICALIZER_PATH = (
    REPO_ROOT / "tools/canonicalize_corpus_source_selection_ledger_v0_1.py"
)


def load_canonicalizer():
    spec = importlib.util.spec_from_file_location(
        "corpus_001_canonicalizer",
        CANONICALIZER_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load canonicalizer.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def render(ledger: dict) -> str:
    lines = [
        "# Corpus 001 Source-Selection Ledger Projection",
        "",
        "> Non-canonical human-readable projection generated from the JSON ledger.",
        "",
        "| Observation | Stratum | Selection status | Admitted | Disclosure | Source SHA-256 | Admission reason |",
        "|---|---|---|---:|---|---|---|",
    ]

    for observation in ledger["observations"]:
        source_hash = observation["source"]["source_sha256"]
        if source_hash is None:
            source_hash = "NOT_ACQUIRED"

        reason = observation["admission"]["admission_reason"]
        if reason is None:
            reason = observation["open_slot_reason"] or "NOT_SUPPLIED"

        safe_reason = reason.replace("|", "\\|").replace("\n", " ")
        lines.append(
            "| {id} | {stratum} | {status} | {admitted} | "
            "{disclosure} | {digest} | {reason} |".format(
                id=observation["observation_id"],
                stratum=observation["required_stratum"],
                status=observation["selection_status"],
                admitted=str(observation["admitted"]).lower(),
                disclosure=observation["disclosure"]["status"],
                digest=source_hash,
                reason=safe_reason,
            )
        )

    lines.extend(
        [
            "",
            "## Authority boundary",
            "",
            "- Selection does not confer validation.",
            "- Selection does not confer endorsement.",
            "- Selection does not confer partnership.",
            "- Selection does not confer publication authority.",
            "- Missing external context is not inferred.",
            "",
        ]
    )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--output", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()

    try:
        canonicalizer = load_canonicalizer()
        ledger = canonicalizer.load_json_strict(args.ledger)
        markdown = render(ledger)

        if "canonical_private_locator" in markdown:
            raise RuntimeError(
                "Private locator field leaked into Markdown projection."
            )

        if args.output is None:
            print(markdown)
        else:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(
                markdown,
                encoding="utf-8",
                newline="\n",
            )
        return 0
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())