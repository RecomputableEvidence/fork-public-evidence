from csh_test_support import *

class TestPairComparison(FixtureContractMixin, unittest.TestCase):
    checker = staticmethod(check_pair_comparison)
    valid_dir = FIXTURES / "pair-comparison" / "valid"
    invalid_dir = FIXTURES / "pair-comparison" / "invalid"

if __name__ == "__main__":
    unittest.main()