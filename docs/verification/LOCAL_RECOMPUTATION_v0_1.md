# Fork Local Recomputation v0.1

## Status and purpose

This document defines the default local recomputation procedure for contributors and reviewers.

It does not replace package-specific, experiment-specific, checker-specific, or branch-specific verification instructions. The more specific governing verification artifact controls.

A successful local recomputation establishes only the declared result of the commands executed against the identified inputs. It does not establish truth, compliance, legality, safety, authority, endorsement, independent review, production readiness, or admission.

## Toolchain authority

Fork does not impose one repository-wide shell as the authoritative execution environment for every component.

The controlling local command for a component is the command declared by that component’s verification guide, package README, experiment procedure, or governing workflow documentation.

Contributors must not replace a declared command with a translated or alternative command and then describe the alternative result as identical execution unless equivalence is separately tested and documented.

At the current `main` baseline:

- `docs/VERIFICATION_COMMANDS_v0_1.md` provides the consolidated public/reviewer command path;
- the integrated proof-surface verifier explicitly declares Windows PowerShell 5.1;
- multiple Python component checks are documented as cross-platform commands;
- the public verifier documentation distinguishes execution of the named PowerShell artifact from manual cross-platform reconstruction.

This document therefore does not declare PowerShell 7+ as a repository-wide minimum and does not prohibit Bash, WSL, Linux, or macOS for components that support them.

## Execution categories

### Canonical verifier execution

Canonical verifier execution runs the exact named verifier artifact using its declared shell, interpreter, arguments, working directory, and required environment.

Example from the current public verification surface:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify_fork_proof_surface_v0_1.ps1
```

The applicable verification guide controls the expected output and interpretation.

### Component recomputation

Component recomputation runs the direct checker or test command governing a specific artifact.

Examples include:

```powershell
python .\tools\check_surface_interaction_v0_1.py `
  .\examples\surface-interaction\valid\valid_reliance_references_evidence_boundary_v0_1.json
```

```bash
python tools/check_fork_proof_surface_state_v0_1.py --json --check-summary
```

A component result must not be represented as a full-repository result unless the governing procedure says it is sufficient.

### Manual reconstruction

Manual reconstruction reproduces the steps or component checks of a named verifier without executing the named verifier artifact itself.

Manual reconstruction can provide useful evidence about component behavior and cross-platform accessibility. It is not identical to canonical verifier execution unless equivalence is explicitly established.

### Full repository test execution

The default broad test command documented on `main` is:

```powershell
python -m pytest
```

A full test pass remains test-relative. Each suite must be interpreted under its own contract. Full-suite success does not broaden the meaning of any individual checker result.

## Required local record

Before submitting a change that affects a verifiable surface, record:

- repository and branch;
- exact commit tested;
- operating system;
- shell and version where material;
- interpreter and version;
- dependency installation method or lock source;
- working directory;
- exact commands;
- exit status;
- observed output or stable summary;
- generated or modified files;
- known warnings, skips, failures, or untested conditions.

A pull-request description may contain a concise summary and link to a larger receipt when the output is extensive.

## Preparation procedure

### 1. Start from an identified tree

Fetch the intended base and candidate refs. Record the exact candidate commit before reporting final results.

Do not rely only on a moving branch name when exact candidate identity matters.

### 2. Inspect component instructions

Before executing a command, locate the most specific governing instructions for the affected artifact.

Check, as applicable:

- package README;
- verification guide;
- schema or contract document;
- experiment preregistration;
- workflow file;
- tool help output;
- dependency lock or requirements file.

Do not infer a command solely from a similarly named component.

### 3. Prepare dependencies without expanding scope

Install only the dependencies required by the governing procedure.

Record material dependency versions. When a lock file or hash-locked requirements file exists, use it as directed.

Do not modify dependencies, generated files, fixtures, or lock state merely to obtain a passing result without separately classifying and reviewing that change.

### 4. Run the narrowest controlling checks first

Run the checker or targeted tests that directly govern the modified surface.

This provides a bounded failure signal before broader suites introduce unrelated output.

### 5. Run required regression surfaces

Execute the broader suite, package verifier, integration gate, or tamper/adversarial corpus required by the component’s governing procedure.

Do not state that a matrix or suite passed unless that exact matrix or suite was executed against the reported candidate commit.

### 6. Inspect generated changes

After verification, inspect the working tree.

Determine whether the commands changed:

- receipts;
- manifests;
- checksums;
- snapshots;
- caches;
- lock files;
- line endings;
- timestamps;
- other generated outputs.

Unexpected changes are evidence of nondeterminism, write-mode behavior, environment drift, or incomplete instructions and must be investigated before submission.

### 7. Re-run from a clean state where required

For changes involving deterministic generation, receipts, release packages, experiment packets, canonical fixtures, or admission anchors, use a clean checkout or fresh scratch directory when the governing procedure requires independent recomputation.

A rerun in the same mutated working tree may not detect hidden dependencies on prior output.

## Write-mode controls

Some tools support a write or regeneration mode.

Write mode and verification mode must remain distinguishable.

A contributor should normally:

1. execute intentional regeneration;
2. inspect the generated diff;
3. run the verifier without write mode;
4. confirm that verification makes no further changes.

Do not use a maintainer-only write option during independent review unless the purpose is explicitly to test regeneration and the resulting mutation is preserved as part of the review evidence.

## PowerShell considerations

Use the exact executable declared by the governing procedure:

- `powershell` normally identifies Windows PowerShell;
- `pwsh` identifies PowerShell 7+.

Do not treat them as interchangeable without testing the affected script.

When a script declares Windows PowerShell 5.1, execute it under Windows PowerShell 5.1 for canonical verifier execution. A successful PowerShell 7 run may be useful compatibility evidence but does not replace the declared execution unless the governing artifact is amended.

When complex evidence blocks, here-strings, path escaping, line endings, or encoding are material, preserve the declared shell and file bytes. Record any environment-specific difference rather than generalizing it into a repository-wide prohibition.

## Bash, WSL, Linux, and macOS considerations

Bash, WSL, Linux, and macOS may be used for components whose instructions support them.

A translated shell command is a separate execution path until equivalence is demonstrated.

When reporting cross-platform results, distinguish:

- same checker and same inputs under a different platform;
- manually reconstructed component commands;
- translated wrapper logic;
- canonical execution of the named artifact.

Line-ending normalization, executable-bit changes, path case, locale, filesystem ordering, and shell interpolation can affect results. Preserve these as observed conditions rather than assuming equivalence or failure in advance.

## Failure handling

A failed recomputation should be preserved accurately.

Record:

- exact command;
- exit status;
- relevant output;
- candidate commit;
- environment;
- first observed failing condition;
- whether the failure is expected, unrelated, intermittent, or unresolved;
- any subsequent corrective change as a separate lineage event.

Do not edit the reported output, fixture, checker, or expected result solely to convert a failure into a pass.

A known pre-existing failure should be identified separately from a regression introduced by the candidate.

## Expected-result discipline

The expected result must be declared before interpreting the observed result whenever the governing procedure requires predetermined outcomes.

Report the observed result even when it differs from expectation.

Do not collapse:

- expected-invalid fixture success;
- checker failure;
- infrastructure failure;
- missing dependency;
- evidence gap;
- unresolved state;
- substantive disagreement

into one generic pass/fail statement.

## Pull-request verification statement

A pull request should include a verification statement with this minimum form:

```text
Candidate commit: <full SHA>
Environment: <OS, shell/version, interpreter/version>
Governing verification guide: <path and version>
Commands executed:
  <exact command 1>
  <exact command 2>
Observed result:
  <exit status, test counts, stable tokens, or receipt paths>
Generated changes:
  <none or identified files>
Untested or unresolved conditions:
  <none or explicit conditions>
```

## Interpretation boundary

Local recomputation does not by itself establish:

- source truth or completeness;
- semantic correctness of upstream claims;
- legal admissibility;
- compliance satisfaction;
- safety or security certification;
- institutional authority;
- reviewer independence;
- merge or admission authority;
- production deployment readiness;
- experiment execution authority;
- endorsement.