#!/usr/bin/env python3
"""
Fork client discovery return checker v0.1.

Purpose:
    Classify a completed Client Discovery Return Packet as REVIEWABLE,
    INCOMPLETE, or BLOCKED.

This tool does not decide whether a client is suitable for Fork.
It only decides whether the returned discovery packet contains enough
structured information to support responsible review.

Exit codes:
    0 = REVIEWABLE
    1 = INCOMPLETE
    2 = BLOCKED
    3 = TOOL_ERROR
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


REQUIRED_FILES = [
    "README.md",
    "PACKAGE_MANIFEST.json",
    "CLAIMS_AND_NON_CLAIMS.md",
    "CLIENT_WORKFLOW_PROFILE.md",
    "SOURCE_SYSTEM_INVENTORY.md",
    "ACCESS_AND_EXPORT_MODEL.md",
    "AI_ASSISTED_SURFACE.md",
    "EVIDENCE_ARTIFACT_MAP.md",
    "STATE_TRANSITION_MAP.md",
    "SECURITY_AND_DATA_HANDLING_CONSTRAINTS.md",
    "INSTITUTIONAL_OWNERSHIP_MAP.md",
    "CLAIMS_AND_NON_CLAIMS_ACKNOWLEDGMENT.md",
    "CO_INTEGRATION_BOUNDARY.md",
    "CONFIGURATION_OUTPUT_TARGETS.md",
    "RELEASE_NOTES.md",
    "NEXT_STEPS.md",
    "SHA256SUMS.txt",
]

CLIENT_COMPLETION_FILES = [
    "CLIENT_WORKFLOW_PROFILE.md",
    "SOURCE_SYSTEM_INVENTORY.md",
    "ACCESS_AND_EXPORT_MODEL.md",
    "AI_ASSISTED_SURFACE.md",
    "EVIDENCE_ARTIFACT_MAP.md",
    "STATE_TRANSITION_MAP.md",
    "SECURITY_AND_DATA_HANDLING_CONSTRAINTS.md",
    "INSTITUTIONAL_OWNERSHIP_MAP.md",
    "CLAIMS_AND_NON_CLAIMS_ACKNOWLEDGMENT.md",
    "CO_INTEGRATION_BOUNDARY.md",
    "CONFIGURATION_OUTPUT_TARGETS.md",
]

PLACEHOLDER_PATTERN = re.compile(
    r"\[[^\]]*(CLIENT_TO_COMPLETE|DESCRIBE|YYYY-MM-DD)[^\]]*\]",
    re.IGNORECASE,
)

CHECKED_PATTERN = re.compile(r"^\s*-\s*\[[xX]\]\s+")
UNCHECKED_PATTERN = re.compile(r"^\s*-\s*\[\s\]\s+")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def find_section(text: str, title: str) -> str:
    """
    Return the markdown section body for a heading title.

    This is deliberately simple and robust enough for the packet templates.
    It starts at a line like '## Title' or '### Title' and ends at the next
    heading of equal or higher level.
    """
    lines = text.splitlines()
    heading_re = re.compile(r"^(#{1,6})\s+" + re.escape(title) + r"\s*$", re.IGNORECASE)

    start_index = None
    start_level = None

    for i, line in enumerate(lines):
        match = heading_re.match(line.strip())
        if match:
            start_index = i + 1
            start_level = len(match.group(1))
            break

    if start_index is None or start_level is None:
        return ""

    out: List[str] = []
    next_heading_re = re.compile(r"^(#{1,6})\s+")
    for line in lines[start_index:]:
        match = next_heading_re.match(line.strip())
        if match and len(match.group(1)) <= start_level:
            break
        out.append(line)

    return "\n".join(out).strip()


def checkbox_lines(section: str) -> List[str]:
    return [line for line in section.splitlines() if CHECKED_PATTERN.match(line) or UNCHECKED_PATTERN.match(line)]


def unchecked_checkbox_lines(section: str) -> List[str]:
    return [line for line in section.splitlines() if UNCHECKED_PATTERN.match(line)]


def checked_checkbox_lines(section: str) -> List[str]:
    return [line for line in section.splitlines() if CHECKED_PATTERN.match(line)]


def normalize_free_text(section: str) -> str:
    cleaned: List[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("|"):
            continue
        if PLACEHOLDER_PATTERN.search(stripped):
            continue
        cleaned.append(stripped)
    return "\n".join(cleaned).strip()


def section_has_meaningful_blocker_text(section: str) -> bool:
    cleaned = normalize_free_text(section).lower()
    if not cleaned:
        return False

    allowed = {
        "none",
        "n/a",
        "na",
        "not applicable",
        "unknown",
        "`none`",
        "`unknown`",
    }

    compact = cleaned.replace(".", "").strip()
    if compact in allowed:
        return False

    # If the section contains a real sentence or a non-placeholder entry,
    # treat it as meaningful.
    return True


def checked_option(text: str, label: str) -> bool:
    pattern = re.compile(
        r"^\s*-\s*\[[xX]\]\s+" + re.escape(label) + r"\s*$",
        re.IGNORECASE | re.MULTILINE,
    )
    return bool(pattern.search(text))


def checked_option_contains(text: str, label_fragment: str) -> bool:
    pattern = re.compile(
        r"^\s*-\s*\[[xX]\]\s+.*" + re.escape(label_fragment) + r".*$",
        re.IGNORECASE | re.MULTILINE,
    )
    return bool(pattern.search(text))


def validate_manifest(packet_dir: Path, issues: List[str], warnings: List[str]) -> None:
    manifest_path = packet_dir / "PACKAGE_MANIFEST.json"
    try:
        manifest = json.loads(read_text(manifest_path))
    except Exception as exc:  # noqa: BLE001
        issues.append(f"PACKAGE_MANIFEST.json is not valid JSON: {exc}")
        return

    expected_name = "FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE"
    actual_name = manifest.get("package_name")
    if actual_name != expected_name:
        warnings.append(
            f"PACKAGE_MANIFEST.json package_name is {actual_name!r}; expected {expected_name!r}."
        )

    manifest_files = manifest.get("package_files")
    if not isinstance(manifest_files, list):
        issues.append("PACKAGE_MANIFEST.json package_files is missing or not a list.")
        return

    missing_from_manifest = [name for name in REQUIRED_FILES if name not in manifest_files]
    if missing_from_manifest:
        issues.append(
            "PACKAGE_MANIFEST.json missing required package_files entries: "
            + ", ".join(missing_from_manifest)
        )


def check_required_files(packet_dir: Path, issues: List[str]) -> Dict[str, str]:
    texts: Dict[str, str] = {}

    for file_name in REQUIRED_FILES:
        path = packet_dir / file_name
        if not path.exists():
            issues.append(f"missing required file: {file_name}")
            continue
        if not path.is_file():
            issues.append(f"required path is not a file: {file_name}")
            continue
        try:
            texts[file_name] = read_text(path)
        except UnicodeDecodeError:
            issues.append(f"file is not valid UTF-8: {file_name}")

    return texts


def check_placeholders(texts: Dict[str, str], issues: List[str]) -> None:
    for file_name in CLIENT_COMPLETION_FILES:
        text = texts.get(file_name, "")
        matches = PLACEHOLDER_PATTERN.findall(text)
        if matches:
            count = len(PLACEHOLDER_PATTERN.findall(text))
            issues.append(f"unresolved client placeholders in {file_name}: {count}")


def check_required_acknowledgments(texts: Dict[str, str], issues: List[str]) -> None:
    ack_text = texts.get("CLAIMS_AND_NON_CLAIMS_ACKNOWLEDGMENT.md", "")

    supported_section = find_section(ack_text, "Supported discovery claim")
    if not checked_checkbox_lines(supported_section):
        issues.append(
            "CLAIMS_AND_NON_CLAIMS_ACKNOWLEDGMENT.md supported discovery claim is not checked."
        )

    required_nonclaims = find_section(ack_text, "Required non-claims")
    unchecked = unchecked_checkbox_lines(required_nonclaims)
    if unchecked:
        issues.append(
            "CLAIMS_AND_NON_CLAIMS_ACKNOWLEDGMENT.md has unchecked required non-claims: "
            + str(len(unchecked))
        )

    client_specific = find_section(ack_text, "Unaccepted non-claims")
    if section_has_meaningful_blocker_text(client_specific):
        issues.append(
            "CLAIMS_AND_NON_CLAIMS_ACKNOWLEDGMENT.md contains unaccepted non-claims; "
            "review cannot proceed until these are resolved."
        )


def check_ai_nonclaims(texts: Dict[str, str], issues: List[str]) -> None:
    ai_text = texts.get("AI_ASSISTED_SURFACE.md", "")
    section = find_section(ai_text, "AI non-claims acknowledged")
    unchecked = unchecked_checkbox_lines(section)
    checked = checked_checkbox_lines(section)

    if unchecked:
        issues.append("AI_ASSISTED_SURFACE.md has unchecked AI non-claims: " + str(len(unchecked)))
    if not checked and section:
        issues.append("AI_ASSISTED_SURFACE.md has no checked AI non-claim acknowledgments.")


def check_blockers(texts: Dict[str, str], blockers: List[str]) -> None:
    access_text = texts.get("ACCESS_AND_EXPORT_MODEL.md", "")
    if checked_option(access_text, "No access available"):
        blockers.append("ACCESS_AND_EXPORT_MODEL.md indicates no access is available.")
    if checked_option_contains(access_text, "ACCESS_MODEL_BLOCKED"):
        blockers.append("ACCESS_AND_EXPORT_MODEL.md indicates ACCESS_MODEL_BLOCKED.")

    security_text = texts.get("SECURITY_AND_DATA_HANDLING_CONSTRAINTS.md", "")
    security_blockers = find_section(security_text, "Security blockers")
    if section_has_meaningful_blocker_text(security_blockers):
        blockers.append("SECURITY_AND_DATA_HANDLING_CONSTRAINTS.md lists security blockers.")

    ack_text = texts.get("CLAIMS_AND_NON_CLAIMS_ACKNOWLEDGMENT.md", "")
    unaccepted = find_section(ack_text, "Unaccepted non-claims")
    if section_has_meaningful_blocker_text(unaccepted):
        blockers.append("CLAIMS_AND_NON_CLAIMS_ACKNOWLEDGMENT.md lists unaccepted non-claims.")

    config_text = texts.get("CONFIGURATION_OUTPUT_TARGETS.md", "")
    implementation_blockers = find_section(config_text, "Implementation blockers")
    if section_has_meaningful_blocker_text(implementation_blockers):
        blockers.append("CONFIGURATION_OUTPUT_TARGETS.md lists implementation blockers.")


def check_minimum_review_signals(texts: Dict[str, str], issues: List[str]) -> None:
    """
    Check that the returned packet has the major sections filled enough to review.
    This is intentionally structural and conservative.
    """
    workflow = texts.get("CLIENT_WORKFLOW_PROFILE.md", "")
    if "Workflow name:" in workflow and "UNKNOWN" in find_section(workflow, "Workflow identification"):
        issues.append("CLIENT_WORKFLOW_PROFILE.md still contains UNKNOWN workflow identification fields.")

    source = texts.get("SOURCE_SYSTEM_INVENTORY.md", "")
    if "Source-system table" in source and PLACEHOLDER_PATTERN.search(source):
        # Already counted as placeholders, but keep the message specific.
        issues.append("SOURCE_SYSTEM_INVENTORY.md does not yet identify source systems cleanly.")

    evidence = texts.get("EVIDENCE_ARTIFACT_MAP.md", "")
    if "Evidence sufficiency concern" in evidence:
        concern = find_section(evidence, "Evidence sufficiency concern")
        if not checked_checkbox_lines(concern):
            issues.append("EVIDENCE_ARTIFACT_MAP.md evidence sufficiency concern is not selected.")

    access = texts.get("ACCESS_AND_EXPORT_MODEL.md", "")
    posture = find_section(access, "Access posture")
    if posture and not checked_checkbox_lines(posture):
        issues.append("ACCESS_AND_EXPORT_MODEL.md access posture has no selected option.")

    ownership = texts.get("INSTITUTIONAL_OWNERSHIP_MAP.md", "")
    response_ownership = find_section(ownership, "Response ownership")
    if not normalize_free_text(response_ownership):
        issues.append("INSTITUTIONAL_OWNERSHIP_MAP.md response ownership is not completed.")


def classify(issues: List[str], blockers: List[str]) -> Tuple[str, int]:
    if blockers:
        return "BLOCKED", 2
    if issues:
        return "INCOMPLETE", 1
    return "REVIEWABLE", 0


def run(packet_dir: Path, emit_json: bool) -> int:
    issues: List[str] = []
    warnings: List[str] = []
    blockers: List[str] = []

    if not packet_dir.exists():
        print(f"CLIENT_DISCOVERY_RETURN_CHECK: TOOL_ERROR")
        print(f"- packet directory does not exist: {packet_dir}")
        return 3

    if not packet_dir.is_dir():
        print(f"CLIENT_DISCOVERY_RETURN_CHECK: TOOL_ERROR")
        print(f"- path is not a directory: {packet_dir}")
        return 3

    texts = check_required_files(packet_dir, issues)

    if "PACKAGE_MANIFEST.json" in texts:
        validate_manifest(packet_dir, issues, warnings)

    check_placeholders(texts, issues)
    check_required_acknowledgments(texts, issues)
    check_ai_nonclaims(texts, issues)
    check_minimum_review_signals(texts, issues)
    check_blockers(texts, blockers)

    status, exit_code = classify(issues, blockers)

    payload = {
        "status": status,
        "packet_dir": str(packet_dir.resolve()),
        "checked_files": len(texts),
        "required_files": len(REQUIRED_FILES),
        "issues": issues,
        "blockers": blockers,
        "warnings": warnings,
    }

    if emit_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return exit_code

    print(f"CLIENT_DISCOVERY_RETURN_CHECK: {status}")
    print(f"packet_dir: {packet_dir.resolve()}")
    print(f"checked_files: {len(texts)}")

    if blockers:
        print("blockers:")
        for item in blockers:
            print(f"- {item}")

    if issues:
        print("issues:")
        for item in issues:
            print(f"- {item}")

    if warnings:
        print("warnings:")
        for item in warnings:
            print(f"- {item}")

    return exit_code


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Check whether a completed Fork Client Discovery Return Packet is reviewable."
    )
    parser.add_argument("packet_dir", help="Path to completed client discovery return packet directory.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON output.")
    args = parser.parse_args(argv)

    return run(Path(args.packet_dir), args.json)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))