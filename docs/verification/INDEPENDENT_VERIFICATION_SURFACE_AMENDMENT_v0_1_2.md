# Independent Verification Surface Amendment v0.1.2

Status: successor hardening proposed after exterior recomputation.  
Predecessor package: PR #64 head `d911ad5c33e0ec32037414effa7749326983d5ff`.  
Subject package: PR #63 head `82c34252d7b8d9e8957fb5a86500e12da6cf363a`.  
Execution effect: none. Pair-001 remains blocked.

## Preserved observations

Mac McFall / M87 recorded two bounded, non-blocking observations during exterior review:

1. `candidate_checkout` and `candidate_code_execution` were emitted as literal declarations even though the non-execution guarantee was supported by inspected control flow.
2. The CSH readiness checker recomputed the correct fail-closed state but did not report a contradiction when the binding's declared `status` disagreed with that recomputation.

This amendment preserves both observations and changes the current implementation without rewriting the reviewed commits or exterior artifacts.

## Successor behavior

The fresh-repository runner now records the actual worktree-add and process-execution operations performed by the runner. Candidate checkout and candidate code-execution fields are derived from that operation record. Regression tests prove that a candidate-sourced checkout or process is detected.

The CSH readiness checker now emits `declared_status_consistency`. A declared/recomputed mismatch is a failed structural check and produces `PRE_EXECUTION_BINDING_FAILED`; it cannot promote execution.

## Post-admission recomputation scope

During the ordered PR #64 then PR #63 merge rehearsal, the full suite exposed that the historical PR #64 receipt test was executing the v0.1.1 checker from the mutable current worktree after its claim-admission dependency changed. That is not the reviewed package environment.

The regression now recomputes the historical receipt from the exact reviewed package commit `d911ad5c33e0ec32037414effa7749326983d5ff`. Generic v0.1 fixture construction also includes the provenance-bound predecessor archives required by the successor claim-admission policy. Historical package evidence remains byte-exact; current-state dependencies are not silently substituted for reviewed package dependencies.

The dedicated GitHub workflow follows the same rule: it invokes the operation-record-derived fresh runner against the reviewed package commit, then runs the current v0.1 and v0.1.1 adversarial suites. It no longer substitutes the post-admission worktree claim checker into the historical receipt recomputation.

## Validation

- fresh recomputation at `d911ad5c33e0ec32037414effa7749326983d5ff`: `FRESH_RECOMPUTATION_PASS`, receipt byte-exact;
- candidate effects: `DERIVED_FROM_OPERATION_RECORD`;
- readiness: 13/13 checks pass, `STRUCTURALLY_READY_EXECUTION_BLOCKED`, executable false, provider calls zero;
- focused successor tests: 25 passed;
- full repository suite after the PR #64/PR #63 merge rehearsal: 705 passed.

## Non-claims

This amendment does not authorize Pair-001 execution, publish the instrumentation release anchor, validate provider credentials or quota, grant merge or repository authority, certify security or compliance, establish semantic truth, or convert exterior review into endorsement.
