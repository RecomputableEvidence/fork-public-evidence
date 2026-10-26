# CSH-S002 stopped attempt preservation and parser successor v0.2

The user requested preservation and a versioned parser repair after the first
corpus attempt stopped. This is an offline instrumentation repair, not a new
campaign, continuation, or retrospective change to the original ledger.

## Preserved execution

CSH_S002_STOPPED_ATTEMPT_20261026 contains all nine members of the uploaded
csh-s002-corpus-20261026-105606.zip, byte-for-byte, with Windows path separators
normalized. PRESERVATION_MANIFEST.json records every member hash and the source
archive hash. The original STOPPED ledger, FAIL receipt, response.bin, output.txt,
freeze and analysis handoff are unchanged.

Unit S002-SIM_F_POINTER_UNRESOLVED-B-H0-R1 returned HTTP 200, completed, exact
anthropic/claude-haiku-5-5 model string, and reported cost USD 0.00059. The first
frozen wire request and three recorded body/output hashes were verified. The
response used a single enclosing JSON code fence; the v0.1 bare-object parser
rejected it with transfer_json_object. Twenty-three units were not attempted.
Combined neutral plus corpus reported cost: USD 0.00062. Gross committed
reservation remains USD 0.09. No billing ceiling or semantic result is inferred.

## Separately versioned repair

New tools/parse_csh_s002_response_v0_2.py accepts a bare strict JSON object or one
whole-response enclosing ```json fence. Opening and closing markers occupy
separate lines; LF and CRLF are accepted. Only surrounding JSON whitespace is
ignored. The lowercase json tag is required. No untagged/other-language fences,
prose extraction, nested or multiple fenced blocks, concatenated values, duplicate
keys, nonfinite numbers, arrays, or silent JSON repairs are accepted. Literal
backticks inside a valid JSON string remain data.

The successor calls the unchanged v0.1 assessor and replaces only its
transfer_json_object result. Model identity, completion, response structure,
returned tool activity, history, and finite USD cost checks remain effective.
Offline parsing evaluates response bodies; original HTTP status and provenance
must still be established from preserved execution receipts.

CSH_S002_PARSER_REVIEW_20261026 contains a separately generated parser receipt,
parsed_transfer.json, and exact copies of response.bin and extracted output.txt.
The raw source hash and derived hashes connect these artifacts. Successor body
acceptance is PASS / single_json_fence / PENDING_HUMAN_CODING. The original
campaign remains STOPPED and its first receipt remains FAIL. No human coding,
semantic judgment, continuation record, or paid request was produced.

The existing tools/run_csh_s002_v0_1.py, frozen 24-request package, requests,
parser tests for the predecessor, and campaign marker are unchanged. This module
has no network or resume command. Any future execution continuation must bind
this repair, the observed first response, remaining order and existing budget;
it must not silently retry the first unit or delete the original marker.

## Offline invocation

```powershell
.\.venv\Scripts\python.exe tools/parse_csh_s002_response_v0_2.py `
  --response docs/current-standing/CSH_S002_STOPPED_ATTEMPT_20261026/S002-SIM_F_POINTER_UNRESOLVED-B-H0-R1/response.bin `
  --expected-model anthropic/claude-haiku-5-5 `
  --output-dir C:\N\csh-s002-parser-v02-review
```

The output directory must be new. The command preserves input bytes before
parsing and performs no API calls. Regression fixtures cover the actual uploaded
response, original failure reproduction, accepted/rejected wrappers, duplicate
keys, malformed JSON, preserved acceptance gates and no-overwrite behavior.
