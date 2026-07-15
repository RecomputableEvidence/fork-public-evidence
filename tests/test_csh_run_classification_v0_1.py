from csh_test_support import *

class TestRunClassification(FixtureContractMixin, unittest.TestCase):
    checker = staticmethod(check_run_classification)
    valid_dir = FIXTURES / "run-classification" / "valid"
    invalid_dir = FIXTURES / "run-classification" / "invalid"

if __name__ == "__main__":
    unittest.main()