#!/usr/bin/env python3
from csh_evidence_common_v0_1 import check_integrated_manifest, run_cli

if __name__ == "__main__":
    raise SystemExit(run_cli(
        "check_csh_integrated_evidence_chain_v0_1.py",
        check_integrated_manifest,
        "Validate an integrated CSH evidence-chain manifest v0.1.",
    ))