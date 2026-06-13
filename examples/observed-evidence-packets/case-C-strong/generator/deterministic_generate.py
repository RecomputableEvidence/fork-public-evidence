#!/usr/bin/env python3
from pathlib import Path
import hashlib
import sys

if len(sys.argv) != 3:
    raise SystemExit("usage: deterministic_generate.py <prompt-path> <output-path>")

prompt_path = Path(sys.argv[1])
output_path = Path(sys.argv[2])
prompt = prompt_path.read_text(encoding="utf-8")
prompt_digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]

brief = (
    "Case C deterministic brief\n"
    f"Prompt digest: {prompt_digest}\n"
    "Finding: AI workflow evidence must preserve observed facts, recomputability class, "
    "and claim boundaries without inheriting correctness, authority, or legal sufficiency.\n"
)

output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(brief, encoding="utf-8", newline="\n")
