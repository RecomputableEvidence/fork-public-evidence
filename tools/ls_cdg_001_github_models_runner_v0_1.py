#!/usr/bin/env python3
"""Bounded GitHub Models runner for LS-CDG-001 v0.1.1 preflight.

Exactly one non-streaming request per invocation. No retries, tools, retrieval,
or conversation history. Exact request/response bytes and execution metadata are
preserved. This runner is used only after a frozen caller selects model and
max_tokens.
"""
from __future__ import annotations

import argparse, hashlib, json, os, urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path

ENDPOINT = "https://models.github.ai/inference/chat/completions"
API_VERSION = "2022-11-28"
MODELS = {
    "llama": {
        "requested": "meta/Llama-4-Scout-17B-16E-Instruct",
        "expected": "Llama-4-Scout-17B-16E-Instruct",
        "provider": "Meta",
    },
    "deepseek": {
        "requested": "deepseek/DeepSeek-V3-0324",
        "expected": "DeepSeek-V3-0324",
        "provider": "DeepSeek",
    },
}

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical(value) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--model", choices=sorted(MODELS), required=True)
    p.add_argument("--system", type=Path, required=True)
    p.add_argument("--prompt", type=Path, required=True)
    p.add_argument("--max-tokens", type=int, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    args = p.parse_args()
    if args.max_tokens < 1 or args.max_tokens > 2048:
        raise SystemExit("max-tokens outside frozen preflight range")
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token.strip():
        raise SystemExit("GITHUB_TOKEN unavailable")
    spec = MODELS[args.model]
    system_raw = args.system.read_bytes(); prompt_raw = args.prompt.read_bytes()
    system = system_raw.decode("utf-8"); prompt = prompt_raw.decode("utf-8")
    payload = {
        "frequency_penalty": 0,
        "max_tokens": args.max_tokens,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "model": spec["requested"],
        "presence_penalty": 0,
        "stream": False,
        "temperature": 0,
        "top_p": 1,
    }
    request_body = canonical(payload)
    args.out_dir.mkdir(parents=True, exist_ok=False)
    (args.out_dir / "request.json").write_bytes(request_body)
    request = urllib.request.Request(
        ENDPOINT, data=request_body, method="POST",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": API_VERSION,
        },
    )
    started = now(); status = None; headers = {}; body = b""; transport_error = None
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            status = int(response.status); headers = dict(response.headers); body = response.read()
    except urllib.error.HTTPError as exc:
        status = int(exc.code); headers = dict(exc.headers); body = exc.read()
    except Exception as exc:
        transport_error = {"type": type(exc).__name__, "message": str(exc)}
    completed = now()
    metadata = {
        "runner_version": "0.1.0",
        "started_at_utc": started,
        "completed_at_utc": completed,
        "endpoint": ENDPOINT,
        "provider": spec["provider"],
        "requested_model": spec["requested"],
        "expected_returned_model": spec["expected"],
        "parameters": {"max_tokens": args.max_tokens, "temperature": 0, "top_p": 1, "stream": False, "frequency_penalty": 0, "presence_penalty": 0},
        "tools_enabled": False,
        "retrieval_enabled": False,
        "conversation_history": "NONE",
        "retry_count": 0,
        "silent_retries_permitted": False,
        "request_sha256": sha256(request_body),
        "system_prompt_sha256": sha256(system_raw),
        "prompt_sha256": sha256(prompt_raw),
        "http_status": status,
        "transport_error": transport_error,
    }
    if transport_error is not None:
        metadata["execution_status"] = "transport_error"
        (args.out_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        return 5
    (args.out_dir / "response.json").write_bytes(body)
    metadata["response_sha256"] = sha256(body)
    if status is None or not (200 <= status < 300):
        metadata["execution_status"] = "http_error"
        (args.out_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        return 3
    try:
        parsed = json.loads(body.decode("utf-8"))
        returned = parsed["model"]
        text = parsed["choices"][0]["message"]["content"]
        usage = parsed.get("usage")
    except Exception as exc:
        metadata["execution_status"] = "invalid_provider_response"
        metadata["validation_error"] = str(exc)
        (args.out_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        return 4
    metadata["returned_model"] = returned
    metadata["usage"] = usage
    metadata["response_text_sha256"] = sha256(text.encode("utf-8"))
    (args.out_dir / "response_text.txt").write_text(text, encoding="utf-8")
    if returned != spec["expected"]:
        metadata["execution_status"] = "returned_model_mismatch"
        (args.out_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        return 4
    metadata["execution_status"] = "success"
    (args.out_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
