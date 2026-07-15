#!/usr/bin/env python3
from csh_evidence_common_v0_1 import check_pair_comparison, run_cli

if __name__ == "__main__":
    raise SystemExit(run_cli(
        "check_csh_pair_comparison_v0_1.py",
        check_pair_comparison,
        "Validate a CSH pair-comparison record v0.1.",
    ))