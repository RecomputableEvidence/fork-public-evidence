from csh_test_support import *

class TestIntegratedEvidenceChain(unittest.TestCase):
    def test_valid_integrated_fixtures(self):
        manifests = sorted((FIXTURES / "integrated" / "valid").glob("*/manifest.json"))
        self.assertTrue(manifests)
        for path in manifests:
            with self.subTest(path=path):
                errors = check_integrated_manifest(path, ROOT)
                self.assertEqual([], errors, "\n".join(errors))

    def test_invalid_integrated_fixtures(self):
        manifests = sorted((FIXTURES / "integrated" / "invalid").glob("*/manifest.json"))
        self.assertTrue(manifests)
        for path in manifests:
            with self.subTest(path=path):
                errors = check_integrated_manifest(path, ROOT)
                self.assertTrue(errors, f"Expected rejection for {path}")

if __name__ == "__main__":
    unittest.main()