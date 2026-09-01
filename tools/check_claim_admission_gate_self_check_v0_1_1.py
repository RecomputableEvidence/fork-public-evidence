#!/usr/bin/env python3
"""Emit a scoped successor to the v0.1 claim-admission local self-check receipt.

The predecessor checker remains authoritative for claim-admission semantics. This
successor changes only the committed self-check receipt boundary: repository-wide
tree cardinality is an observation about the surrounding repository, not a
control-surface invariant. Unrelated additive files therefore cannot invalidate
the scoped receipt merely by increasing the global entry count.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

PREDECESSOR = "tools/check_claim_admission_gate_v0_1.py"
CHECKER_ID = "FORK_CLAIM_ADMISSION_GATE_SCOPED_SELF_CHECK_v0_1_1"
SCOPE_ID = "FORK_CLAIM_ADMISSION_CONTROL_SURFACE_SCOPE_v0_1_1"


def load_predecessor(root: Path) -> Any:
    path = root / PREDECESSOR
    spec = importlib.util.spec_from_file_location("fork_claim_admission_gate_v0_1", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load predecessor checker: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def evaluate(root: Path) -> dict[str, Any]:
    root = root.resolve()
    predecessor = load_predecessor(root)
    output = predecessor.build_output(
        root,
        predecessor.WorktreeView(root),
        base_sha=None,
        candidate_sha=None,
        changed=[],
        initial_errors=[],
    )
    verification = dict(output.get("verification", {}))
    observed_tree_entry_count = verification.pop("tree_entry_count", None)
    verification.update(
        {
            "self_check_scope_id": SCOPE_ID,
            "scope_semantics": "CLAIM_ADMISSION_CONTROL_SURFACE_ONLY",
            "unrelated_repository_additions_affect_receipt": False,
            "global_tree_entry_count": {
                "binding": "OBSERVED_NOT_RECEIPT_BOUND",
                "observed": observed_tree_entry_count,
            },
        }
    )
    # The global count is deliberately not part of equality semantics. Retain
    # an explicit observation without its value so the exclusion is visible.
    verification["global_tree_entry_count"].pop("observed", None)
    output["checker_id"] = CHECKER_ID
    output["predecessor_checker_id"] = predecessor.CHECKER_ID
    output["verification"] = verification
    output["execution_boundary"] = dict(output.get("execution_boundary", {}))
    output["execution_boundary"]["mode"] = "LOCAL_SCOPED_SELF_CHECK"
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--write-receipt", type=Path)
    args = parser.parse_args()
    output = evaluate(args.repo_root)
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    if args.write_receipt:
        target = args.write_receipt
        if not target.is_absolute():
            target = args.repo_root.resolve() / target
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    return 0 if output.get("result", {}).get("ok") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
