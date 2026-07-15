#!/usr/bin/env python3
from csh_evidence_common_v0_1 import check_run_classification, run_cli

if __name__ == "__main__":
    raise SystemExit(run_cli(
        "check_csh_run_classification_v0_1.py",
        check_run_classification,
        "Validate a CSH run-classification record v0.1.",
    ))