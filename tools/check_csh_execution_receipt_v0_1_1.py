#!/usr/bin/env python3
from csh_evidence_common_v0_1 import check_execution_receipt, run_cli

if __name__ == "__main__":
    raise SystemExit(run_cli(
        "check_csh_execution_receipt_v0_1_1.py",
        check_execution_receipt,
        "Validate a CSH execution receipt v0.1.1.",
    ))