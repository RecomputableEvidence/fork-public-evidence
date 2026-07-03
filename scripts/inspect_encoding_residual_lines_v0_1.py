#!/usr/bin/env python3
from pathlib import Path

TARGETS = [
    "docs/PUBLIC_SURFACE_CLEANUP_CHECKLIST_v0_1.md",
    "docs/viewer/ahi-viewer-v0_1/data/scenarios_bundle.json",
    "docs/viewer/ahi-viewer-v0_2/data/comparison_pairs.json",
    "scripts/add_surface_top_layer_to_readme.ps1",
    "scripts/build_ahi_viewer_comparison_data_v0_2.py",
    "scripts/create_public_surface_cleanup_files_v0_1.py",
    "scripts/fix_encoding_regression_allowlisted_v0_1.py",
    "white-paper/Reconstructive_Fidelity_in_the_Age_of_AI_v1_0.md",
    "encoding_repair_manifest.json",
    "docs/reviewer/CATEGORIZED_ENCODING_REGRESSION_FIX_LIST_v0_1.md",
]

SUSPECT = {0x00C3, 0x00C2, 0x00E2, 0xFFFD}

for path_text in TARGETS:
    path = Path(path_text)
    if not path.exists():
        continue

    text = path.read_text(encoding="utf-8")
    print(f"\n===== {path_text} =====")
    found = False

    for i, line in enumerate(text.splitlines(), start=1):
        if any(ord(ch) in SUSPECT for ch in line):
            found = True
            print(f"L{i}: {line}")
            cps = " ".join(f"U+{ord(ch):04X}" for ch in line if ord(ch) in SUSPECT)
            print(f"     suspicious: {cps}")

    if not found:
        print("No suspicious lines found.")
