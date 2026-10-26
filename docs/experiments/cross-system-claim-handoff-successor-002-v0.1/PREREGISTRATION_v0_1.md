# CSH-S002: Perplexity handoff pilot v0.1

Status: CANDIDATE_NOT_FROZEN. Preparation and neutral qualification only.
Predecessor: CROSS-SYSTEM-CLAIM-HANDOFF-SUCCESSOR-001-v0.1 (preserved).

## Question and design

Does explicit handoff-state information change unsupported-inheritance findings
for the six S001 scenario meanings under two model families served by Perplexity?
Use all six scenarios, both H0/H1 conditions, two receivers, one replicate:
24 hosted units (12 within-model/scenario pairs). This is a descriptive pilot,
not completion of the predecessor's 72-unit study. There is no replication-based
variance estimate and no claim of independent hosting platforms. Differences
cannot isolate structure from added information/salience.

Candidate receivers are openai/gpt-6-luna and anthropic/claude-haiku-5-5 through
Perplexity Agent API. Model aliases are requested identities, not immutable
weight attestations. Access, exact returned identities, and settings remain
unqualified until the new neutral preflight passes. No fallback models.

## Inputs, order, and isolation

CANDIDATE_v0_1.json binds the inherited corpus builder, byte checker, measurement
specification, classifier, analysis program and predecessor freeze records by
SHA-256. The preparation tool recomputes all S001 packets and verifies actual
bytes against the preserved binding. Packet contents retain their original
S001 identities as reused source material; S002 unit IDs identify new requests.
The caller instruction is fixed, shared across conditions, and adds no scoring
rules. Each exact request is included in the candidate PLAN.json.

Pairs are sorted by SHA-256 of the declared seed, scenario and receiver ID.
Within-pair condition order alternates H0/H1 and H1/H0. This reproducible order
is fixed before results, not randomized sampling. One independent conversation
per unit, no previous_response_id. Explicit tools=[], tool_choice=none,
max_steps=1, store=false, no preset/effort/profile/skills/connectors, no retrieval.
No temperature or reasoning override is assumed portable; provider defaults
apply and are a limitation. max_output_tokens=2048 for both receivers.

## Measurements and interpretation

Adopt the bound S001 U/P/A/T definitions and coding procedure by reference.
Preserve raw output before normalization. Label new coding and analysis records
with S002 identities; validate compatibility before corpus execution. Human
coding, disagreements and adjudications remain separate from deterministic
classification. Do not treat model-written labels as independently verified
coding. No numeric score for missing, incomplete or unclassifiable responses.
No selective reruns, prompt tuning, model substitution, or exclusion based on
results. Any modification after freeze requires a successor or an explicit
instrumentation repair with prior attempts preserved.

The 12-unit deterministic reference may be prepared as a separate engineering
check; it is not generated or executed by this candidate tool and is excluded
from the 24 hosted units and nominal cost calculation.

## Budget proposal

Use existing Perplexity credit only. Proposed campaign request-admission budget:
$1.00. Reserve $0.03 per neutral/corpus request: $0.06 for two neutral requests,
$0.72 for 24 pilot requests, $0.22 unallocated. No automatic retries or concurrency.
These are planning reservations, not guaranteed prices or provider billing caps.

The offline estimate uses input UTF-8 byte counts plus an assumed 2048-token
per-request overhead and the output allowance at published low-context rates.
It does not prove actual token counts, cache charges or hidden platform costs.
Candidate rates were read from Perplexity's model catalog on 2026-10-26:
https://docs.perplexity.ai/docs/agent-api/models
Both candidate models: $0.10/1M input and $0.50/1M output in the applicable
low-context tier (Haiku below 100k; Luna below 272k). Live access remains unknown.

The neutral tool reserves before sending, preserves exact HTTP request/response
bodies, rejects returned tool activity and mismatched identity/content/completion,
and stops on missing/invalid USD usage or cost above $0.03. A failed first call
prevents the second. An unknown outcome retains its reservation. Fresh output
directories prevent overwriting evidence, not repeated billing: do not rerun
batches without accounting for earlier reservations and observed cost.

A corpus runner must enforce campaign-wide admission and durable reservations,
stop on uncertain outcomes/costs, reconcile returned cost, and verify frozen
requests before sending. An in-flight request can exceed its reservation.
No such enforcement is claimed from this preparation tool.

## Gates before corpus execution

1. Two successful neutral receipts with exact model, content, completion,
   no returned tool activity, exact byte hashes and finite USD costs.
2. Review costs and adopt a concrete campaign budget based on those receipts.
3. Bind receiver settings, source bytes, measurement/coding procedure, adapter
   implementation, budget and exact order in a successor freeze record.
4. Implement and test the corpus execution adapter, durable budget admission,
   output capture, terminal-state recording and normalization handoff.
5. Verify the frozen package before the first corpus request.

None of these gates is satisfied by the earlier web-grounded Perplexity demo.
No corpus execution command is exposed by this preparation tool. A neutral
PASS is access/configuration evidence only, not a CSH result or freeze.
