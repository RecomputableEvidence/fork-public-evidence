#!/usr/bin/env python3
"""
fix_encoding_regression_allowlisted_v0_1.py

Strict allowlist-driven encoding repair.
Dry-run by default. Writes only when --write is provided.

Boundary:
- No os.walk broad mutation.
- Hard-excludes app.js.
- Logs manual-review cases without modifying them.
- Does not blanket-exclude docs/ or examples/.
- Does not establish correctness, compliance, legal sufficiency, fault, excuse, or execution eligibility.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

MOJIBAKE_MAP: Dict[str, str] = {
    "\u00e2\u20ac\u0153": "\u201c",
    "\u00e2\u20ac\u009d": "\u201d",
    "\u00e2\u20ac": "\u201d",
    "\u00e2\u20ac ": "\u201d",
    "\u00e2\u20ac\u2122": "\u2019",
    "\u00e2\u20ac\u02dc": "\u2018",
    "\u00e2\u20ac\u201c": "\u2013",
    "\u00e2\u20ac\u201d": "\u2014",
    "\u00e2\u20ac\u00a6": "\u2026",
    "\u00c3\u00a9": "\u00e9",
    "\u00c3\u00a1": "\u00e1",
    "\u00c3\u00b3": "\u00f3",
    "\u00c3\u00b1": "\u00f1",
    "\u00c3\u00bc": "\u00fc",
    "\u00c3\u00a0": "\u00e0",
    "\u00c3\u00a2": "\u00e2",
    "\u00c3\u00aa": "\u00ea",
    "\u00c3\u00ae": "\u00ee",
    "\u00c3\u00b4": "\u00f4",
    "\u00c3\u00a7": "\u00e7",
    "\u00c2\u00a0": " ",
    "\u00c2": "",
}

SUSPICIOUS_CHARS = {"\u00c3", "\u00c2", "\u00e2", "\ufffd"}

CONTROL_CHAR_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")

HARD_EXCLUDE_BASENAMES = {"app.js"}

PROTECTED_PATH_FRAGMENTS = {
    "computed_scenario_09_demo",
}

MANIFEST_PATH = Path("encoding_repair_manifest.json")
MANUAL_LOG_PATH = Path("encoding_manual_review.log")


def normalize_repo_path(path_text: str) -> Path:
    return Path(path_text.replace("\\", "/"))


def suspicious_score(text: str) -> int:
    return sum(text.count(ch) for ch in SUSPICIOUS_CHARS)


def has_control_chars(text: str) -> bool:
    return CONTROL_CHAR_RE.search(text) is not None


def is_hard_excluded(path: Path) -> bool:
    if path.name in HARD_EXCLUDE_BASENAMES:
        return True
    lower_parts = {part.lower() for part in path.parts}
    return any(fragment.lower() in lower_parts for fragment in PROTECTED_PATH_FRAGMENTS)


def load_allowlist(path: Path) -> List[Path]:
    targets: List[Path] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        targets.append(normalize_repo_path(line))
    return targets


def apply_literal_replacements(text: str) -> Tuple[str, List[Dict[str, object]]]:
    changes: List[Dict[str, object]] = []
    updated = text

    for bad, good in MOJIBAKE_MAP.items():
        count = updated.count(bad)
        if count:
            updated = updated.replace(bad, good)
            changes.append({"from": bad, "to": good, "count": count})

    return updated, changes


def try_roundtrip_line_repair(line: str) -> str:
    """
    Conservative fallback for lines with remaining suspicious chars.
    Applies cp1252 -> utf-8 roundtrip only when suspicious score strictly decreases
    and no control characters are introduced.
    """
    current = line
    for _ in range(3):
        before = suspicious_score(current)
        if before == 0:
            break
        try:
            candidate = current.encode("cp1252").decode("utf-8")
        except UnicodeError:
            break

        after = suspicious_score(candidate)
        if after < before and not has_control_chars(candidate):
            current = candidate
        else:
            break

    return current


def repair_text(text: str) -> Tuple[str, List[Dict[str, object]]]:
    literal_repaired, changes = apply_literal_replacements(text)

    if suspicious_score(literal_repaired) == 0:
        return literal_repaired, changes

    repaired_lines: List[str] = []
    roundtrip_lines = 0
    for line in literal_repaired.splitlines(keepends=True):
        new_line = try_roundtrip_line_repair(line)
        if new_line != line:
            roundtrip_lines += 1
        repaired_lines.append(new_line)

    repaired = "".join(repaired_lines)
    if roundtrip_lines:
        changes.append({"roundtrip_lines_repaired": roundtrip_lines})

    return repaired, changes


def process_file(path: Path, write: bool) -> Dict[str, object]:
    record: Dict[str, object] = {
        "path": str(path).replace("\\", "/"),
        "status": "CLEAN",
        "changes": [],
        "before_suspicious_score": None,
        "after_suspicious_score": None,
    }

    if is_hard_excluded(path):
        record["status"] = "SKIPPED_HARD_EXCLUDE"
        return record

    if not path.exists():
        record["status"] = "ERROR_NOT_FOUND"
        return record

    raw = path.read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    if had_bom:
        raw = raw[3:]

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        record["status"] = "MANUAL_REVIEW_NON_UTF8"
        record["error"] = str(exc)
        return record

    if has_control_chars(text):
        record["status"] = "MANUAL_REVIEW_CONTROL_CHARS"
        return record

    before_score = suspicious_score(text)
    repaired, changes = repair_text(text)
    after_score = suspicious_score(repaired)

    record["before_suspicious_score"] = before_score
    record["after_suspicious_score"] = after_score

    if has_control_chars(repaired):
        record["status"] = "MANUAL_REVIEW_REPAIR_INTRODUCED_CONTROL_CHARS"
        return record

    if had_bom:
        changes.insert(0, {"strip_bom": True})

    if not changes:
        record["status"] = "CLEAN"
        return record

    if after_score > before_score:
        record["status"] = "MANUAL_REVIEW_SUSPICIOUS_SCORE_INCREASED"
        record["changes"] = changes
        return record

    if after_score != 0:
        # Keep this manual rather than partially writing ambiguous double/triple-encoded cases.
        record["status"] = "MANUAL_REVIEW_RESIDUAL_SUSPICIOUS_CHARS"
        record["changes"] = changes
        return record

    record["changes"] = changes
    record["status"] = "FIXED" if write else "DRY_RUN_FIXED"

    if write:
        path.write_text(repaired, encoding="utf-8", newline="\n")

    return record


def write_logs(records: List[Dict[str, object]]) -> None:
    MANIFEST_PATH.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    manual = [r for r in records if str(r["status"]).startswith("MANUAL_REVIEW") or str(r["status"]).startswith("ERROR")]
    with MANUAL_LOG_PATH.open("w", encoding="utf-8", newline="\n") as f:
        f.write("Files requiring manual review for encoding anomalies:\n")
        f.write("=" * 60 + "\n")
        for r in manual:
            f.write(f"[{r['status']}] {r['path']}\n")
            if "error" in r:
                f.write(f"  error: {r['error']}\n")
            if r.get("before_suspicious_score") is not None:
                f.write(f"  suspicious_score: {r['before_suspicious_score']} -> {r['after_suspicious_score']}\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Allowlisted encoding regression repair.")
    parser.add_argument("--allowlist", required=True, help="line-separated repo-relative paths")
    parser.add_argument("--write", action="store_true", help="write changes; default is dry-run")
    args = parser.parse_args()

    if not Path(".git").exists():
        raise SystemExit("FAIL: run from repository root")

    allowlist = Path(args.allowlist)
    if not allowlist.exists():
        raise SystemExit(f"FAIL: allowlist not found: {allowlist}")

    targets = load_allowlist(allowlist)
    print(f"Starting allowlisted encoding repair on {len(targets)} files")
    print(f"Mode: {'WRITE' if args.write else 'DRY-RUN'}")

    records = []
    for target in targets:
        record = process_file(target, args.write)
        records.append(record)
        status = record["status"]
        if status != "CLEAN":
            print(f"[{status}] {record['path']}")

    write_logs(records)

    print("")
    print("Summary:")
    counts: Dict[str, int] = {}
    for record in records:
        counts[record["status"]] = counts.get(record["status"], 0) + 1
    for status in sorted(counts):
        print(f"  {status}: {counts[status]}")

    manual_count = sum(1 for r in records if str(r["status"]).startswith("MANUAL_REVIEW") or str(r["status"]).startswith("ERROR"))
    if manual_count:
        print(f"\nManual review required for {manual_count} file(s). See {MANUAL_LOG_PATH}.")

    print(f"Manifest written to {MANIFEST_PATH}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
