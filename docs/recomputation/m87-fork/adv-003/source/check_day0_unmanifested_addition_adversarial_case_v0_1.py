#!/usr/bin/env python3
"""
Day-0 Unmanifested-Artifact-Addition Adversarial Case v0.1

Case ID: LRT_DAY0_ADV_003_UNMANIFESTED_ADDITION_v0_1
Filed by: Mac McFall / M87 (exterior observer), 17 July 2026
Format: matches tools/check_longitudinal_day0_adversarial_cases_v0_1.py conventions.

Question:
    Does the current v0.1 Day-0 packet checker detect an UNMANIFESTED file added
    to a packet evidence directory, or does it verify only the artifacts the
    manifest already lists?

Method (all in a disposable scratch copy; source packet is never mutated):
    1. Copy the Day-0 packet into a temp repository-shaped directory.
    2. CONTROL: run the unmodified Day-0 checker on the clean scratch copy.
    3. MUTATION: write one new file, `evidence/day0_injected_extra_v0_1.json`,
       into the packet. Do NOT touch the manifest, sidecar, or outer receipt.
    4. Run the unmodified Day-0 checker on the mutated scratch copy.

Expected observation (the limitation this case reproduces):
    - CONTROL: failed == 0 (clean packet passes).
    - MUTATION: failed == 0 (injected file is NOT detected).
    A pass of THIS suite means the limitation was reproduced: the checker's
    coverage is manifest-listed artifacts only; it performs no directory-inventory
    completeness sweep, so a fabricated evidence file can ride inside a packet that
    still verifies.

Contrast with ADV_001 (coordinated re-seal): ADV_001 mutates a manifested file and
re-seals all bindings. THIS case adds an UNMANIFESTED file and changes no bindings —
a distinct, simpler gap that requires no re-sealing capability at all.

Non-claim:
    This case does not show the clean Day-0 packet was altered, and asserts no
    authority. It records checker coverage scope only. It does not establish truth,
    compliance, legal sufficiency, safety, authorization, approval, certification,
    endorsement, validation, production readiness, procurement approval, or
    institutional authority.

Exit codes:
    0 = limitation reproduced as expected (control passes AND injection undetected)
    1 = limitation NOT reproduced (injection was detected, or control failed) -> gap
        may already be closed; re-inspect
    3 = tool error
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PACKET_REL = "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1"
DAY0_CHECKER_REL = "tools/check_longitudinal_reconstruction_day0_packet_v0_1.py"
INJECTED_REL = "evidence/day0_injected_extra_v0_1.json"
INJECTED_CONTENT = {
    "injected_by": "LRT_DAY0_ADV_003_unmanifested_addition_case",
    "purpose": "unmanifested artifact added to packet evidence directory",
    "note": "not referenced by packet_manifest.json",
}


def repo_root(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).resolve()
    here = Path(__file__).resolve()
    for cand in [here.parent, *here.parents]:
        if (cand / DAY0_CHECKER_REL).exists() and (cand / PACKET_REL).exists():
            return cand
    return Path.cwd().resolve()


def run_day0(root: Path, packet_dir: Path) -> dict:
    proc = subprocess.run(
        [sys.executable, str(root / DAY0_CHECKER_REL),
         "--packet-root", str(packet_dir), "--json"],
        capture_output=True, text=True,
    )
    out = proc.stdout.strip()
    try:
        data = json.loads(out)
    except Exception:
        return {"_parse_error": True, "_stdout": out[:400], "_stderr": proc.stderr[:400],
                "_exit": proc.returncode}
    data["_exit"] = proc.returncode
    return data


def summarize(tag: str, data: dict) -> dict:
    if data.get("_parse_error"):
        return {"stage": tag, "parse_error": True, "stdout": data.get("_stdout"),
                "stderr": data.get("_stderr")}
    return {"stage": tag, "passed": data.get("passed"), "failed": data.get("failed"),
            "total": data.get("total"), "checker_exit": data.get("_exit")}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", default=None, help="Fork repo root (auto-detected if omitted).")
    ap.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = ap.parse_args(argv)

    root = repo_root(args.repo_root)
    checker = root / DAY0_CHECKER_REL
    packet = root / PACKET_REL
    if not checker.exists() or not packet.exists():
        print(json.dumps({"case_id": "LRT_DAY0_ADV_003_UNMANIFESTED_ADDITION_v0_1",
                          "status": "TOOL_ERROR",
                          "detail": f"checker or packet not found under {root}"}, indent=2))
        return 3

    tmp = Path(tempfile.mkdtemp(prefix="fork_adv003_"))
    try:
        scratch_packet = tmp / "packet"
        shutil.copytree(packet, scratch_packet)

        control = run_day0(root, scratch_packet)
        control_s = summarize("control_clean", control)

        injected = scratch_packet / INJECTED_REL
        injected.parent.mkdir(parents=True, exist_ok=True)
        injected.write_text(json.dumps(INJECTED_CONTENT, indent=2), encoding="utf-8")

        mutated = run_day0(root, scratch_packet)
        mutated_s = summarize("mutation_unmanifested_addition", mutated)

        control_ok = control_s.get("failed") == 0 and not control_s.get("parse_error")
        injection_undetected = mutated_s.get("failed") == 0 and not mutated_s.get("parse_error")
        reproduced = bool(control_ok and injection_undetected)

        outcome_codes = []
        if reproduced:
            outcome_codes = [
                "MANIFEST_LISTED_ARTIFACTS_ONLY_CONFIRMED",
                "UNMANIFESTED_ADDITION_UNDETECTED",
                "NO_DIRECTORY_INVENTORY_COMPLETENESS_SWEEP",
                "PACKET_STILL_VERIFIES_WITH_INJECTED_EVIDENCE",
            ]
        elif control_ok and not injection_undetected:
            outcome_codes = ["UNMANIFESTED_ADDITION_DETECTED_GAP_MAY_BE_CLOSED"]
        else:
            outcome_codes = ["CONTROL_DID_NOT_PASS_REINSPECT_HARNESS"]

        payload = {
            "case_id": "LRT_DAY0_ADV_003_UNMANIFESTED_ADDITION_v0_1",
            "filed_by": "Mac McFall / M87 (exterior observer)",
            "reviewed_packet": PACKET_REL,
            "day0_checker": DAY0_CHECKER_REL,
            "mutation": {"target": INJECTED_REL,
                         "summary": "one unmanifested JSON file added to packet evidence directory; "
                                    "manifest, sidecar, and outer receipt unchanged"},
            "control": control_s,
            "mutation_result": mutated_s,
            "limitation_reproduced": reproduced,
            "outcome_codes": outcome_codes,
            "non_authority_statement": (
                "This adversarial case records Day-0 checker coverage scope only. It does not "
                "establish truth, compliance, legal sufficiency, safety, authorization, approval, "
                "certification, endorsement, validation, production readiness, procurement approval, "
                "or institutional authority."),
        }

        if args.json:
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            print(f"CASE {payload['case_id']}")
            print(f"  control:  passed={control_s.get('passed')} failed={control_s.get('failed')}")
            print(f"  mutation: passed={mutated_s.get('passed')} failed={mutated_s.get('failed')}")
            print(f"  limitation_reproduced: {reproduced}")
            for c in outcome_codes:
                print(f"  - {c}")
        return 0 if reproduced else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
