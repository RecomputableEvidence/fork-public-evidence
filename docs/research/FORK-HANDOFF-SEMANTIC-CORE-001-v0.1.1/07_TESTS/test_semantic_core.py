import importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('validator',ROOT/'06_REFERENCE_VALIDATOR.py')
v=importlib.util.module_from_spec(spec); spec.loader.exec_module(v)

class SemanticCoreTests(unittest.TestCase):
    def test_all_valid_fixtures_pass(self):
        for p in sorted((ROOT/'04_VALID_FIXTURES').glob('*.json')):
            with self.subTest(p=p.name):
                self.assertEqual(v.validate_obj(json.loads(p.read_text(encoding='utf-8')))['result'],'PASS')

    def test_all_adversarial_fixtures_fail(self):
        for p in sorted((ROOT/'05_ADVERSARIAL_FIXTURES').glob('*.json')):
            with self.subTest(p=p.name):
                self.assertEqual(v.validate_obj(json.loads(p.read_text(encoding='utf-8')))['result'],'FAIL')

    def test_fixture_corpus_expected_count(self):
        self.assertEqual(len(list((ROOT/'04_VALID_FIXTURES').glob('*.json'))),4)
        self.assertEqual(len(list((ROOT/'05_ADVERSARIAL_FIXTURES').glob('*.json'))),15)

    def test_witness_claim_forbidden(self):
        p=ROOT/'05_ADVERSARIAL_FIXTURES/ADV_009_PREMATURE_WITNESS_CLAIM.json'
        codes={e['code'] for e in v.validate_obj(json.loads(p.read_text(encoding='utf-8')))['semantic_errors']}
        self.assertIn('CRYPTOGRAPHIC_LAYER_PREMATURE',codes)

    def test_reseal_target_not_claimed_solved(self):
        txt=(ROOT/'10_SUCCESSOR_QUALIFICATION_TARGET.md').read_text(encoding='utf-8')
        self.assertIn('NOT_SOLVED_BY_THIS_OBJECT',txt)
        self.assertIn('FORK-EXTERNAL-WITNESS-BINDING-001',txt)

    def test_all_declared_invariants_have_direct_fixture_coverage(self):
        inv=json.loads((ROOT/'03_SEMANTIC_INVARIANTS.json').read_text(encoding='utf-8'))['invariants']
        cov=json.loads((ROOT/'16_INVARIANT_FIXTURE_COVERAGE.json').read_text(encoding='utf-8'))['coverage']
        self.assertEqual({x['id'] for x in inv},{x['invariant_id'] for x in cov})
        for row in cov:
            p=ROOT/row['fixture']
            rep=v.validate_obj(json.loads(p.read_text(encoding='utf-8')))
            codes={e['code'] for e in rep['semantic_errors']+rep['schema_errors']}
            with self.subTest(invariant=row['invariant_id']):
                self.assertEqual(rep['result'],'FAIL')
                self.assertIn(row['expected_failure_code'],codes)

    def test_declared_truth_boundary_passes_without_truth_promotion(self):
        p=ROOT/'04_VALID_FIXTURES/VALID_004_DECLARED_TRUTH_BOUNDARY.json'
        obj=json.loads(p.read_text(encoding='utf-8'))
        rep=v.validate_obj(obj)
        self.assertEqual(rep['result'],'PASS')
        self.assertEqual(obj['claims'][0]['claim_dimension'],'TRUTH')
        self.assertEqual(obj['claims'][0]['claim_basis'],'DECLARED')
        self.assertEqual(obj['claims'][0]['evidence_refs'],[])
        pp=json.loads((ROOT/'04_PROHIBITED_PROMOTIONS.json').read_text(encoding='utf-8'))['promotions']
        self.assertIn({'id':'PP-015','from':'VALIDATOR_PASS','to':'TRUTH_ESTABLISHED'},pp)

    def test_no_runtime_bytecode_is_packaged(self):
        bad=[p for p in ROOT.rglob('*') if p.is_file() and (p.suffix=='.pyc' or '__pycache__' in p.parts)]
        self.assertEqual(bad,[])

if __name__=='__main__': unittest.main()
