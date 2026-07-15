#!/usr/bin/env python3
from csh_evidence_common_v0_1 import check_reviewer_receipt, run_cli

if __name__ == "__main__":
    raise SystemExit(run_cli(
        "check_csh_reviewer_receipt_v0_1.py",
        check_reviewer_receipt,
        "Validate a CSH reviewer receipt v0.1.",
    ))