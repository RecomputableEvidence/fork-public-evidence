#!/usr/bin/env python3
import argparse, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "docs/exterior-observations/reviews"
MANIFEST = PKG / "REVIEW_PACKAGE_MANIFEST_v0_1.json"
RECEIPT = PKG / "EXTERIOR_REVIEW_PR89_PR90_RECEIPT_v0_1.json"

def sha256(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--json",action="store_true"); args=ap.parse_args()
    findings=[]
    m=json.loads(MANIFEST.read_text(encoding="utf-8"))
    for e in m["entries"]:
        p=ROOT/e["path"]
        if not p.is_file(): findings.append({"code":"MISSING_FILE","path":e["path"]}); continue
        if p.stat().st_size!=e["size_bytes"]: findings.append({"code":"SIZE_MISMATCH","path":e["path"]})
        if sha256(p)!=e["sha256"]: findings.append({"code":"DIGEST_MISMATCH","path":e["path"]})
    r=json.loads(RECEIPT.read_text(encoding="utf-8"))
    declared=r["integrity"]["receipt_payload_sha256"]
    del r["integrity"]["receipt_payload_sha256"]
    canonical=json.dumps(r,sort_keys=True,ensure_ascii=False,separators=(",",":")).encode("utf-8")
    if hashlib.sha256(canonical).hexdigest()!=declared: findings.append({"code":"RECEIPT_PAYLOAD_DIGEST_MISMATCH"})
    required=["REPRODUCED_WITHIN_DECLARED_SCOPE","ATTRIBUTION_UNRESOLVED_NOT_AUTHENTICATED","PRIOR_EXPOSURE_DISCLOSED","REPOSITORY_WIDE_REVIEW_NOT_PERFORMED","CLAIM_LEDGER_NOT_VERIFIED_CLAIM_BY_CLAIM","NO_ADMISSION_OR_EXECUTION_EFFECT"]
    text=RECEIPT.read_text(encoding="utf-8")
    for token in required:
        if token not in text: findings.append({"code":"REQUIRED_STANDING_TOKEN_MISSING","token":token})
    result={"result":"EXTERIOR_REVIEW_PACKAGE_CONFORMS" if not findings else "EXTERIOR_REVIEW_PACKAGE_NONCONFORMING","finding_count":len(findings),"findings":findings,"does_not_prove":["review attribution","repository-wide correctness","claim-ledger correctness","admission","publication","merge authorization","authority transfer","execution permission"]}
    print(json.dumps(result,indent=2) if args.json else result["result"]); return 0 if not findings else 1
if __name__=="__main__": sys.exit(main())
