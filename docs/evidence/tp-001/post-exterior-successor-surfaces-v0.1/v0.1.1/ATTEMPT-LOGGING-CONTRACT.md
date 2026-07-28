# Attempt logging contract

Every invocation creates a new directory:

`RETURN/ATTEMPTS/<attempt-id>/`

Each directory contains its own preflight record, completed disclosure copy, receipt, and raw stdout/stderr. Existing attempt directories are never reused. `RETURN/ATTEMPT-INDEX.json` appends one digest-bound entry per attempt.

A later attempt must not overwrite earlier negative evidence.
