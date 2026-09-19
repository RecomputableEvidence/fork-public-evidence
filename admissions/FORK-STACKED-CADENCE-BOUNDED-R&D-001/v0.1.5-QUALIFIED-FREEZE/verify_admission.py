#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
SUBJECT_SHA='bde58e1f3389e179d91d26c17c05318e8815a8604e1c0e1d0494a127cd8a49c2'
PRED_SHA='f78c654cf2e30c2bfeba3962a80272cf9ddb804cc352a064fa7a23f5653eb289'
EVIDENCE_SHA='bdec62146a9aea1b601d1d43dac6f511bcebcde6beb24e76dc9e9bc55570a4a3'
FINAL_SHA='bfb1ab333e58097dbdfd1d75ac1ab6a6f16430f85b9598f8a8afff031b48c97e'
DISP='INDEPENDENT_QUALIFICATION_PASS__BOUNDED_STACKED_CADENCE_SEMANTICS_ADMITTED_WITHIN_TESTED_SURFACE'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fail(m):raise SystemExit('FAIL: '+m)
def main():
 for line in (HERE/'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
  if not line.strip():continue
  d,n=line.split('  ',1);p=HERE/n
  if not p.is_file() or sha(p)!=d:fail('admission byte closure: '+n)
 obj=json.loads((HERE/'SUBJECT/01_OBJECT_SPEC.json').read_text())
 if obj.get('object_id')!='FORK-STACKED-CADENCE-BOUNDED-R&D-001' or obj.get('version')!='v0.1.5':fail('subject identity')
 if obj.get('status')!='CANDIDATE_QUALIFICATION_REPAIR_SUCCESSOR':fail('subject authored status')
 if obj.get('predecessor_disposition')!='INDEPENDENT_QUALIFICATION_FAIL__SURVIVING_SEMANTIC_MUTATION_OBSERVED':fail('subject predecessor disposition')
 if obj.get('implementation_authority')!='NONE_BEYOND_BOUNDED_LOCAL_HARNESS':fail('subject implementation authority')
 contract=json.loads((HERE/'SUBJECT/19_NORMATIVE_SEMANTIC_CONTRACT.json').read_text())
 delta=json.loads((HERE/'SUBJECT/21_REPAIR_DELTA.json').read_text())
 ir=json.loads((HERE/'SUBJECT/22_INTERNAL_REPAIR_RECEIPT.json').read_text())
 if ir.get('live_epoch_authority')!='NONE' or ir.get('repair_scope_expansion') is not False:fail('internal repair authority/scope boundary')
 vis=ir.get('verified_internal_surface',{}); v08=vis.get('08_VERIFY.py',{})
 if v08.get('check_count')!=291 or v08.get('failure_count')!=0 or not v08.get('verified'):fail('291-check internal verification drift')
 if vis.get('20_V014_FAILURE_REGRESSION_TEST.py',{}).get('M01_through_M10')!='BLOCKED':fail('M01-M10 regression standing drift')
 if delta.get('negative_result_freeze_sha256')!=PRED_SHA or delta.get('new_capability_introduced') is not False:fail('repair delta predecessor/capability binding')
 pred=json.loads((HERE/'PREDECESSOR_NEGATIVE_RESULT/01_VERIFICATION_AND_FREEZE_RECEIPT.json').read_text())
 if pred.get('standing')!='NEGATIVE_EMPIRICAL_RESULT_FROZEN' or pred.get('reported_disposition')!='INDEPENDENT_QUALIFICATION_FAIL__SURVIVING_SEMANTIC_MUTATION_OBSERVED':fail('negative predecessor standing')
 ledger=json.loads((HERE/'PREDECESSOR_NEGATIVE_RESULT/02_SURVIVING_MUTATION_LEDGER.json').read_text())
 if len(ledger.get('mutations',[]))!=10:fail('negative mutation ledger count')
 ev=json.loads((HERE/'INDEPENDENT_EVIDENCE/01_FREEZE_RECEIPT.json').read_text())
 if ev.get('canonical_subject',{}).get('sha256')!=SUBJECT_SHA or ev.get('final_promotion_authority')!='NONE':fail('independent evidence boundary')
 if ev.get('local_recomputation',{}).get('independent_recompute',{}).get('check_count')!=182 or ev.get('local_recomputation',{}).get('independent_recompute',{}).get('failure_count')!=0 or not ev.get('local_recomputation',{}).get('independent_recompute',{}).get('passed'):fail('182-check independent recomputation receipt')
 fr=json.loads((HERE/'FINAL_ADJUDICATION/01_FINAL_VERIFICATION_RECEIPT.json').read_text())
 a=fr.get('adjudication',{})
 if a.get('final_disposition')!=DISP or a.get('criteria_count')!=9 or a.get('criteria_pass_count')!=9 or not a.get('all_criteria_pass'):fail('final adjudication receipt')
 if a.get('subject_modified') or a.get('repair_performed'):fail('subject modified during final gate')
 if fr.get('standing')!='QUALIFIED_BOUNDED_RESEARCH_SEMANTICS__NO_LIVE_RUNTIME_AUTHORITY':fail('final standing')
 bp=fr.get('bound_populations',{})
 if bp.get('canonical_subject_sha256')!=SUBJECT_SHA or bp.get('independent_evidence_freeze_sha256')!=EVIDENCE_SHA or bp.get('v0_1_4_negative_predecessor_sha256')!=PRED_SHA:fail('final bound populations')
 dec=json.loads((HERE/'FINAL_ADJUDICATION/05_ADJUDICATION_DECISION.json').read_text())
 if dec.get('final_disposition')!=DISP or len(dec.get('criteria',[]))!=9 or any(c.get('result')!='PASS' for c in dec['criteria']):fail('G01-G09 decision')
 if not dec.get('non_claims_confirmed') or dec.get('subject_modified') or dec.get('repair_performed'):fail('decision standing boundary')
 cand=json.loads((HERE/'FORK-STACKED-CADENCE-v0.1.5-REPOSITORY-ADMISSION-CANDIDATE-001.json').read_text())
 if cand.get('frozen_package_bindings')!={'subject':SUBJECT_SHA,'pred':PRED_SHA,'evidence':EVIDENCE_SHA,'final':FINAL_SHA}:fail('frozen package bindings')
 if cand.get('standing')!='QUALIFIED_BOUNDED_RESEARCH_SEMANTICS__NO_LIVE_RUNTIME_AUTHORITY' or cand.get('research_disposition')!=DISP:fail('admission standing/disposition')
 if cand.get('admission_state')!='CANDIDATE_PENDING_PR_CHECKS_AND_MAIN_MERGE':fail('admission candidate state')
 bind=json.loads((HERE/'FORK-STACKED-CADENCE-v0.1.5-REPOSITORY-BYTE-BINDINGS-001.json').read_text())
 if bind.get('hash_bound_not_byte_admitted',{}).get('INDEPENDENT_EVIDENCE/23_RECOMPUTE_RESULT.json')!='fe578331dd578c37fb7b34a7721e9f920af992746733c101130ea2473fe25e7e':fail('independent recompute result hash binding')
 print('PASS: Stacked Cadence v0.1.5 bounded repository admission verified')
 print('negative predecessor preserved; 291/291 internal + 182/182 independent + G01-G09 PASS preserved')
 print('repository admission adds no live runtime, production, external trust, governance, or commercial standing')
if __name__=='__main__':main()
