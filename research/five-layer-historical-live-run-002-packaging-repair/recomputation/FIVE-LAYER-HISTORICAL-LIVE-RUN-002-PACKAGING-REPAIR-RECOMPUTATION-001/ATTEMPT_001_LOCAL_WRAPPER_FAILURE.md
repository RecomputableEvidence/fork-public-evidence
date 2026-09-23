# ATTEMPT-001 — Local wrapper failure before substantive byte evaluation

**Classification:** `LOCAL_EXECUTION_WRAPPER_FAILURE_BEFORE_SUBSTANTIVE_BYTE_EVALUATION`

The first reconstruction attempt did not reach substantive parent-byte evaluation.

Observed local failures:

- output paths resolved outside the repository worktree (`C:\Users\Rwcal\research\...`) instead of under `C:\Users\Rwcal\fork-public-evidence\research\...`;
- the gzip source and output streams therefore were not created;
- follow-on `CopyTo` / `Dispose` calls operated on null values;
- the variable name `$input` collided with PowerShell's automatic `$input` variable, producing an `ArrayListEnumeratorSimple` object rather than the intended file stream.

Treatment:

- preserve the failed attempt as local execution evidence;
- do not attribute the failure to the repository subject;
- do not repair or alter the subject package;
- correct only the local wrapper by anchoring paths to `(Get-Location).Path` and using non-reserved stream variable names.

**Substantive evidence effect:** `NONE`
