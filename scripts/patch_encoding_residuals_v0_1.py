#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re

SUSPICIOUS = ["\u00c3", "\u00c2", "\u00e2", "\ufffd"]

FIX_LIST_LINE = "- [ ] Repair documented encoding artifacts by codepoint sequence, including U+00C3, U+00C2, U+00E2-prefixed mojibake, and corrupted arrow artifacts."


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def replace_in_file(path_text: str, replacements: list[tuple[str, str]]) -> None:
    path = Path(path_text)
    if not path.exists():
        print(f"SKIP missing: {path_text}")
        return

    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in replacements:
        text = text.replace(old, new)

    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
        print(f"UPDATED: {path_text}")
    else:
        print(f"NOCHANGE: {path_text}")


def patch_checklist() -> None:
    path = Path("docs/PUBLIC_SURFACE_CLEANUP_CHECKLIST_v0_1.md")
    if not path.exists():
        return

    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if "Repair `" in line and "corrupted arrow artifacts" in line:
            out.append(FIX_LIST_LINE)
        else:
            out.append(line)

    path.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    print("UPDATED: docs/PUBLIC_SURFACE_CLEANUP_CHECKLIST_v0_1.md")


def patch_create_public_surface_cleanup_script() -> None:
    path = Path("scripts/create_public_surface_cleanup_files_v0_1.py")
    if not path.exists():
        return

    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"- \[ \] Repair `.*?corrupted arrow artifacts\.",
        FIX_LIST_LINE,
        text,
    )
    path.write_text(text, encoding="utf-8", newline="\n")
    print("UPDATED: scripts/create_public_surface_cleanup_files_v0_1.py")


def patch_comparison_labels() -> None:
    replacements = [
        (
            "Scenario 01 vs Scenario 02 \u00c3\u0192\u00c2\u00a2\u00c3\u00a2\u00e2\u20ac\u0161\u00c2\u00ac\u00c3\u00a2\u00e2\u201a\u00ac\u00c2\u00a0 baseline versus preserved handoff",
            "Scenario 01 vs Scenario 02 \u2014 baseline versus preserved handoff",
        ),
        (
            "Scenario 03 vs Scenario 04 \u00c3\u0192\u00c2\u00a2\u00c3\u00a2\u00e2\u20ac\u0161\u00c2\u00ac\u00c3\u00a2\u00e2\u201a\u00ac\u00c2\u00a0 scope expansion versus authority leakage",
            "Scenario 03 vs Scenario 04 \u2014 scope expansion versus authority leakage",
        ),
        (
            "Scenario 05 vs Scenario 06 \u00c3\u0192\u00c2\u00a2\u00c3\u00a2\u00e2\u20ac\u0161\u00c2\u00ac\u00c3\u00a2\u00e2\u201a\u00ac\u00c2\u00a0 policy laundering versus distributed handoff",
            "Scenario 05 vs Scenario 06 \u2014 policy laundering versus distributed handoff",
        ),
        (
            "Scenario 06 vs Scenario 07 \u00c3\u0192\u00c2\u00a2\u00c3\u00a2\u00e2\u20ac\u0161\u00c2\u00ac\u00c3\u00a2\u00e2\u201a\u00ac\u00c2\u00a0 internal distributed boundary versus external authority bridge",
            "Scenario 06 vs Scenario 07 \u2014 internal distributed boundary versus external authority bridge",
        ),
        (
            "Scenario 07 vs Scenario 08 \u00c3\u0192\u00c2\u00a2\u00c3\u00a2\u00e2\u20ac\u0161\u00c2\u00ac\u00c3\u00a2\u00e2\u201a\u00ac\u00c2\u00a0 external authority bridge versus stale validity",
            "Scenario 07 vs Scenario 08 \u2014 external authority bridge versus stale validity",
        ),
        (
            "Scenario 08 vs Scenario 09 \u00e2\u20ac\u201d stale validity versus revocation visibility",
            "Scenario 08 vs Scenario 09 \u2014 stale validity versus revocation visibility",
        ),
    ]

    replace_in_file("scripts/build_ahi_viewer_comparison_data_v0_2.py", replacements)
    replace_in_file("docs/viewer/ahi-viewer-v0_2/data/comparison_pairs.json", replacements)


def patch_add_surface_script() -> None:
    path = Path("scripts/add_surface_top_layer_to_readme.ps1")
    if not path.exists():
        return

    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "AI-assisted vendor-risk recommendation \u00e2\u2020\u2019 internal decision memo \u00e2\u2020\u2019 downstream reliance attempt.",
        "AI-assisted vendor-risk recommendation -> internal decision memo -> downstream reliance attempt.",
    )

    text = re.sub(
        r'\$text = \$text -replace "Copyright.*?", "Copyright.*?"',
        '$text = $text -replace ("Copyright" + [char]0x00C3 + [char]0x0082 + [char]0x00C2 + [char]0x00A9), ("Copyright" + [char]0x00A9)',
        text,
    )

    path.write_text(text, encoding="utf-8", newline="\n")
    print("UPDATED: scripts/add_surface_top_layer_to_readme.ps1")


def patch_fix_script_map() -> None:
    path = Path("scripts/fix_encoding_regression_allowlisted_v0_1.py")
    if not path.exists():
        return

    replacement_map = r"""MOJIBAKE_MAP: Dict[str, str] = {
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

SUSPICIOUS_CHARS = {"\u00c3", "\u00c2", "\u00e2", "\ufffd"}"""

    text = path.read_text(encoding="utf-8")
    updated = re.sub(
        r'MOJIBAKE_MAP: Dict\[str, str\] = \{.*?\}\s*SUSPICIOUS_CHARS = \{.*?\}',
        lambda _m: replacement_map,
        text,
        flags=re.S,
    )

    if updated == text:
        print("WARN: map block unchanged in scripts/fix_encoding_regression_allowlisted_v0_1.py")
    else:
        path.write_text(updated, encoding="utf-8", newline="\n")
        print("UPDATED: scripts/fix_encoding_regression_allowlisted_v0_1.py")


def patch_whitepaper() -> None:
    replacements = [
        ("\u00e2\u20ac\u201d", "\u2014"),
        ("\u00e2\u20ac\u201c", "\u2013"),
        ("\u00e2\u20ac\u2122", "\u2019"),
        ("\u00e2\u20ac\u02dc", "\u2018"),
        ("\u00e2\u20ac\u0153", "\u201c"),
        ("\u00e2\u20ac\u009d", "\u201d"),
        ("\u00e2\u20ac", "\u201d"),
        ("\u00e2\u2020\u2019", "\u2192"),
        ("\u00e2\u20ac\u00b2", "\u2032"),
        ("\u00e2\u2030", "\u2260"),
        ("\u00c2\u00a7", "\u00a7"),
        ("\u00c2", ""),
    ]
    replace_in_file("white-paper/Reconstructive_Fidelity_in_the_Age_of_AI_v1_0.md", replacements)


def main() -> int:
    if not Path(".git").exists():
        fail("run from repository root")

    patch_checklist()
    patch_create_public_surface_cleanup_script()
    patch_comparison_labels()
    patch_add_surface_script()
    patch_fix_script_map()
    patch_whitepaper()

    for app_js in [
        Path("docs/viewer/ahi-viewer-v0_1/app.js"),
        Path("docs/viewer/ahi-viewer-v0_2/app.js"),
    ]:
        if app_js.exists():
            print(f"CONFIRMED_UNTOUCHED_BY_THIS_SCRIPT: {app_js}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
