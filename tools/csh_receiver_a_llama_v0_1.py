#!/usr/bin/env python3
"""CSH v0.1 hosted Receiver A: Meta Llama 4 Scout via GitHub Models."""

from pathlib import Path

from csh_receiver_github_models_v0_1 import ReceiverSpec, run_cli

RECEIVER_SPEC = ReceiverSpec(
    receiver_class_id="llm_receiver_a",
    provider="Meta",
    serving_platform="GitHub Models",
    displayed_model_name="Llama 4 Scout 17B 16E Instruct",
    requested_model_id="meta/Llama-4-Scout-17B-16E-Instruct",
    expected_returned_model="Llama-4-Scout-17B-16E-Instruct",
)


if __name__ == "__main__":
    raise SystemExit(
        run_cli(RECEIVER_SPEC, entrypoint_path=Path(__file__).resolve())
    )
