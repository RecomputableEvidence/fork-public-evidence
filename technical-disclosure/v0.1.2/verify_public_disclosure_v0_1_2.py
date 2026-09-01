#!/usr/bin/env python3
"""Verify Fork Public Technical Disclosure repository successor v0.1.2."""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
ERRORS: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


# 1. The exact inherited v0.1.1 payload must still verify under its own verifier.
base = subprocess.run(
    [sys.executable, "verify_public_disclosure.py"],
    cwd=ROOT,
    text=True,
    capture_output=True,
    check=False,
)
if base.stdout:
    print(base.stdout, end="")
if base.stderr:
    print(base.stderr, end="", file=sys.stderr)
require(base.returncode == 0, f"INHERITED_V0_1_1_VERIFIER_EXIT_NONZERO: {base.returncode}")
require(
    "FORK_PUBLIC_TECHNICAL_DISCLOSURE_V0_1_1_PASS" in base.stdout,
    "INHERITED_V0_1_1_PASS_SIGNAL_MISSING",
)

# 2. The v0.1.2 correction must remain literal text, not control-byte substitution.
readme = ROOT / "README_VERIFY_PUBLIC_DISCLOSURE_v0_1_2.md"
readme_bytes = readme.read_bytes()
require(b"\x0b" not in readme_bytes, "V0_1_2_README_CONTAINS_VERTICAL_TAB")
require(b"\x0c" not in readme_bytes, "V0_1_2_README_CONTAINS_FORM_FEED")
readme_text = readme_bytes.decode("utf-8")
require(
    "Set-Location .\\technical-disclosure\\v0.1.2" in readme_text,
    "V0_1_2_LITERAL_POWERSHELL_PATH_MISSING",
)
require(
    "python .\\verify_public_disclosure_v0_1_2.py" in readme_text,
    "V0_1_2_LITERAL_VERIFIER_PATH_MISSING",
)

# 3. The successor manifest must bind the exact predecessor and exact failed candidate.
manifest_path = ROOT / "PUBLIC_DISCLOSURE_SUCCESSOR_MANIFEST_v0_1_2.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
require(manifest.get("record_id") == "FORK-PUBLIC-TECHNICAL-DISCLOSURE-SUCCESSOR-v0.1.2", "SUCCESSOR_RECORD_ID_MISMATCH")
require(manifest.get("status") == "CANDIDATE_REPOSITORY_SUCCESSOR_NOT_YET_DETACHED_BUNDLE_RELEASE", "SUCCESSOR_STATUS_MISMATCH")
require(
    manifest.get("predecessor", {}).get("governed_source_commit")
    == "0c60bbdd2b7c50e1758968464485fac0dfbf008d",
    "PREDECESSOR_COMMIT_MISMATCH",
)
require(
    manifest.get("failed_repair_candidate", {}).get("commit")
    == "a16b1905923354538d6bed1d231fdc810e3d531f",
    "FAILED_CANDIDATE_COMMIT_MISMATCH",
)
require(
    manifest.get("detached_bundle", {}).get("status") == "NOT_YET_PUBLISHED",
    "DETACHED_BUNDLE_STATUS_MUST_REMAIN_NOT_YET_PUBLISHED",
)
require(
    manifest.get("successor", {}).get("semantic_fixture_changed") is False,
    "SUCCESSOR_MUST_NOT_CLAIM_SEMANTIC_FIXTURE_CHANGE",
)

# 4. requirements.txt must remain comments-only and dependency-free.
requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
non_comment = [line for line in requirements if line.strip() and not line.lstrip().startswith("#")]
require(not non_comment, f"UNEXPECTED_REQUIREMENT_LINES: {non_comment}")

print()
if ERRORS:
    print("FORK_PUBLIC_TECHNICAL_DISCLOSURE_V0_1_2_REPOSITORY_SUCCESSOR_FAIL")
    for error in ERRORS:
        print(f"ERROR: {error}")
    sys.exit(1)

print("FORK_PUBLIC_TECHNICAL_DISCLOSURE_V0_1_2_REPOSITORY_SUCCESSOR_PASS")
print("INHERITED_V0_1_1_VERIFIER: PASS")
print("V0_1_2_CONTROL_BYTE_REPAIR: PASS")
print("V0_1_2_SUCCESSOR_BINDING: PASS")
print("V0_1_2_REQUIREMENTS_SYNTAX_BOUNDARY: PASS")
print("DETACHED_BUNDLE_RELEASE: NOT_YET_PUBLISHED")
