# CSH Prompt Artifacts

This directory contains the complete, still-unfrozen Step 5 prompt configuration:

- one shared receiver instruction;
- twelve paired JSON prompt packets;
- one pair manifest with SHA-256 digests;
- one fixed 108-unit run order.

For each scenario, the control and instrumented prompt packets are identical except for `handoff_state_artifact`: `null` for `control_h0`, and the exact scenario-specific handoff object for `instrumented_h1`.

These files are freeze candidates, not evidence of execution. No result-informed tuning is permitted during v0.1.
