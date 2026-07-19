# Fork Independent Verification Surface v0.1

**Control ID:** `FORK_INDEPENDENT_VERIFICATION_SURFACE_v0_1`

**Status:** proposed for review; no merge or experiment authority.

## Purpose

The Independent Verification Surface provides a repository-controlled location from which a contribution can be examined without inheriting the contribution's claims, code, hooks, dependency declarations, workflows, or authority. It recomputes bounded assertions against exact Git objects and returns one of three results:

- `VERIFIED_WITHIN_DECLARED_SCOPE`: every bound assertion is supported and the trusted claim-admission result is exactly the result declared by the plan;
- `INVALIDATED_BY_RECOMPUTATION`: an exact subject binding, expected gate result, or declared assertion is contradicted by observable evidence;
- `INCONCLUSIVE_EVIDENCE_GAP`: the plan, policy, schema, Git object, or required evidence cannot be resolved safely.

These are surface results, not personal or institutional endorsements. A supported machine result does not approve a merge, grant repository standing, certify security, establish universal semantic correctness, or authorize an experiment.

## Separation from the contribution

The verification plan and engine execute from a trusted verifier tree. Candidate commits are addressed only by full commit SHA and read as Git object data. In the trusted lane:

- candidate checkout is prohibited;
- candidate code, tests, hooks, actions, and dependency declarations are not executed;
- no candidate-requested command exists in the plan schema;
- no secret is available;
- tags, submodules, mutable refs, and file-protocol fetches are prohibited;
- plans and asserted blobs are size bounded;
- JSON plans reject duplicate keys and unknown properties;
- repository paths reject absolute paths, traversal, backslashes, control characters, and NUL bytes.

The candidate tree cannot change the verifier plan that judges it. This is surface independence. Independent human review remains a separate, attributable act: the contribution author cannot manufacture it, and this control cannot claim it when no different reviewer is recorded.

## Evidence layers

### 1. Exact subject binding

The plan binds the repository, base commit and tree, candidate commit and tree, and expected merge base. This prevents a successful result for one tree from being represented as a result for another.

### 2. Trusted claim-admission recomputation

The surface executes the trusted-base claim-admission checker against candidate Git objects. The plan must declare the exact expected result kind and exact finding code/path set. Unexpected success and unexpected failure both invalidate the plan result.

This permits bounded transition review without silently weakening a prior gate. For example, a plan may record that an earlier exact-digest policy is expected to reject a provenance-bound successor. The independent assertions must then establish the successor's archived predecessor identity, static workflow hardening, fail-closed state, and unchanged scientific inputs. The old gate finding remains visible in the receipt.

### 3. Declarative assertions

v0.1 supports only non-executable assertions:

- exact changed-path set;
- path present or absent;
- candidate SHA-256 equality;
- candidate path unchanged from the base;
- candidate archive byte-equal to a base path;
- strict-JSON pointer equality;
- workflow hardening evaluated by trusted static parser logic.

No shell, Python, action, test, URL, package, or plugin command can be supplied by a plan.

### 4. External observations

Pull-request state, review records, and GitHub Actions runs may be preserved as external observations. They have `OBSERVATION_ONLY` authority and cannot substitute for a trusted assertion. A later reviewer may recompute or reject them.

## Code-execution boundary

Some contributions include executable behavior whose semantics cannot be established by static Git-object inspection. The trusted lane returns only the result supported by its declared assertions. Independent execution, when needed, belongs in a separate disposable environment with no credentials, secrets, repository write token, persistent state, or authority-bearing network access. Its exact environment, commands, inputs, outputs, and digests must be preserved in a separately attributable receipt.

Candidate execution must never be added to the privileged `pull_request_target` lane.

## PR #63 verification plan

`verification/plans/PR_63_CSH_AMENDMENT_v0_1.json` is the first bounded plan. It evaluates PR #63 from the admitted PR #62 preservation tree. It binds the exact commits and trees, preserves the old gate's three expected transition findings, verifies the complete changed-path set, statically checks both hardened workflow successors, proves each archived predecessor is byte-equal to its base workflow, confirms the scientific freeze remains unchanged, and verifies that execution authority remains false.

The resulting receipt may support the content within that scope. It cannot provide the missing independent human identity, admit PR #63, publish the release anchor, validate provider credentials, close the experiment gate, or execute a receiver call.

## Reviewer workflow

1. Begin from the exact trusted verifier commit.
2. Fetch only the plan's full base and candidate SHAs.
3. Run the self-check.
4. Run the bound verification plan.
5. Compare the generated receipt byte-for-byte with the committed receipt.
6. Inspect every contradicted or inconclusive assertion before considering review.
7. Record reviewer identity and review separately; never edit the machine receipt to imply attribution.
8. Treat any new candidate commit as a new subject requiring a new plan and receipt.

Example:

```text
python tools/check_independent_verification_surface_v0_1.py --self-check
python tools/check_independent_verification_surface_v0_1.py \
  --plan verification/plans/PR_63_CSH_AMENDMENT_v0_1.json
```

## Preservation and experiment boundary

The surface appends evidence; it does not rewrite incident records, remove residual conditions, reinterpret preserved attempts, modify the frozen hypothesis or design, or count execution availability as an experimental outcome. `VERIFIED_WITHIN_DECLARED_SCOPE` has no experiment-execution effect.

## Non-claims

This surface does not establish intent, truth beyond its exact assertions, compliance, legal sufficiency, institutional authority, security certification, production readiness, merge approval, endorsement, or experiment authorization.
