# AI-Assisted Surface

## Purpose

This file identifies where AI assistance enters the workflow.

## AI function

- [ ] generation
- [x] summarization
- [x] classification
- [ ] ranking
- [x] recommendation
- [ ] routing
- [ ] drafting
- [x] review support
- [x] extraction
- [x] triage
- [x] scoring
- [ ] comparison
- [ ] other: Not used
- [ ] unknown

## AI system

- AI system or vendor: ExampleAIReview
- Internal or vendor-provided: VENDOR
- Model identifier retained? YES
- Prompt retained? PARTIAL
- Output retained? YES
- Retrieval context retained? PARTIAL
- Tool calls retained? NO
- Vendor invocation IDs retained? YES
- System messages or policy prompts retained? PARTIAL

## Human review

- Is there human review before action? YES
- Human reviewer role: Vendor risk analyst
- Review notes retained? YES
- Approval retained? YES
- Denial retained? YES
- Modification retained? YES
- Escalation retained? YES

## AI-to-action relationship

The AI system summarizes vendor questionnaire responses, extracts risk indicators, and proposes a risk classification. A vendor-risk analyst reviews the AI output and records the actual disposition in ExampleGRC.

## Unavailable AI artifacts

Full vendor backend routing logic and complete hidden system prompt history are unavailable.

## AI non-claims acknowledged

- [x] Fork does not prove AI output correctness.
- [x] Fork does not prove decision correctness.
- [x] Fork does not claim full replayability of AI behavior.
- [x] Fork does not claim hidden vendor behavior can be reconstructed.
- [x] Fork does not claim source completeness unless explicitly supported by the client evidence boundary.