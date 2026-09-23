#!/usr/bin/env python3
"""Neutral CSH-S001 hosted receiver access preflight. Sends no CSH corpus/treatment/scoring material."""
from __future__ import annotations
import argparse, json, os, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path

CONFIGS={
 "groq":{"env":"GROQ_API_KEY","endpoint":"https://api.groq.com/openai/v1/chat/completions","model":"openai/gpt-oss-120b",
         "payload":{"model":"openai/gpt-oss-120b","messages":[{"role":"user","content":'Return JSON only: {"preflight":"ok"}'}],
                    "temperature":0,"top_p":1,"max_completion_tokens":64,"stream":False,"response_format":{"type":"json_object"},
                    "reasoning_effort":"low","include_reasoning":False}},
 "deepseek":{"env":"DEEPSEEK_API_KEY","endpoint":"https://api.deepseek.com/chat/completions","model":"deepseek-flash",
         "payload":{"model":"deepseek-flash","messages":[{"role":"user","content":'Return JSON only: {"preflight":"ok"}'}],
                    "temperature":0,"top_p":1,"max_tokens":64,"stream":False,"response_format":{"type":"json_object"},
                    "reasoning_effort":"low"}}
}
def call(provider,timeout=45):
    cfg=CONFIGS[provider]; key=os.environ.get(cfg["env"]); started=datetime.now(timezone.utc).isoformat()
    base={"provider":provider,"endpoint":cfg["endpoint"],"requested_model":cfg["model"],"started_at_utc":started,
          "neutral_prompt":True,"contains_csh_corpus":False,"contains_treatment":False,"contains_classifier_material":False}
    if not key: return {**base,"status":"CREDENTIAL_UNAVAILABLE","credential_environment_variable":cfg["env"]}
    body=json.dumps(cfg["payload"],separators=(",",":")).encode("utf-8")
    req=urllib.request.Request(cfg["endpoint"],data=body,method="POST",
        headers={"Authorization":f"Bearer {key}","Content-Type":"application/json","User-Agent":"fork-csh-s001-neutral-preflight/0.1"})
    try:
        with urllib.request.urlopen(req,timeout=timeout) as response:
            rb=response.read(); status=response.status
    except urllib.error.HTTPError as exc:
        rb=exc.read(); return {**base,"status":"HTTP_ERROR","http_status":exc.code,
          "error_body_utf8":rb.decode("utf-8",errors="replace"),"completed_at_utc":datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        return {**base,"status":"EXECUTION_ERROR","error_type":type(exc).__name__,"error":str(exc),
                "completed_at_utc":datetime.now(timezone.utc).isoformat()}
    try: parsed=json.loads(rb.decode("utf-8"))
    except Exception as exc:
        return {**base,"status":"RESPONSE_NOT_JSON","http_status":status,"error":str(exc),
                "completed_at_utc":datetime.now(timezone.utc).isoformat()}
    choice=(parsed.get("choices") or [{}])[0]; msg=choice.get("message") or {}; content=msg.get("content"); json_ok=False
    if isinstance(content,str):
        try: json.loads(content); json_ok=True
        except Exception: json_ok=False
    returned=parsed.get("model"); identity=bool(returned) and (returned==cfg["model"] or cfg["model"].split("/")[-1].lower() in str(returned).lower())
    passed=status==200 and json_ok and identity
    return {**base,"status":"PASS" if passed else "RESPONSE_INCOMPATIBLE","http_status":status,"returned_model":returned,
            "model_identity_compatible":identity,"json_content_valid":json_ok,"finish_reason":choice.get("finish_reason"),
            "provider_response_id":parsed.get("id"),"system_fingerprint":parsed.get("system_fingerprint"),
            "completed_at_utc":datetime.now(timezone.utc).isoformat()}
def main():
    p=argparse.ArgumentParser(); p.add_argument("--provider",choices=sorted(CONFIGS),action="append"); p.add_argument("--output-dir",type=Path)
    p.add_argument("--json",action="store_true",dest="as_json"); p.add_argument("--allow-missing-credentials",action="store_true")
    a=p.parse_args(); providers=a.provider or sorted(CONFIGS); results=[call(p) for p in providers]
    if a.output_dir:
        a.output_dir.mkdir(parents=True,exist_ok=True)
        for r in results: (a.output_dir/f"{r['provider']}_preflight.json").write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    if a.as_json or not a.output_dir: print(json.dumps(results,indent=2,sort_keys=True))
    failures=[r for r in results if r["status"]!="PASS" and not (a.allow_missing_credentials and r["status"]=="CREDENTIAL_UNAVAILABLE")]
    return 1 if failures else 0
if __name__=="__main__": raise SystemExit(main())
