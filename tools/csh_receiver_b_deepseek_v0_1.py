#!/usr/bin/env python3
"""CSH v0.1 hosted Receiver B: DeepSeek V3 0324 via GitHub Models."""

from pathlib import Path

from csh_receiver_github_models_v0_1 import ReceiverSpec, run_cli

RECEIVER_SPEC = ReceiverSpec(
    receiver_class_id="llm_receiver_b",
    provider="DeepSeek",
    serving_platform="GitHub Models",
    displayed_model_name="DeepSeek-V3-0324",
    requested_model_id="deepseek/DeepSeek-V3-0324",
    expected_returned_model="DeepSeek-V3-0324",
)


if __name__ == "__main__":
    raise SystemExit(
        run_cli(RECEIVER_SPEC, entrypoint_path=Path(__file__).resolve())
    )
