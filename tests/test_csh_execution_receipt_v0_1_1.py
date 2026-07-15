from csh_test_support import *

class TestExecutionReceipt(FixtureContractMixin, unittest.TestCase):
    checker = staticmethod(check_execution_receipt)
    valid_dir = FIXTURES / "execution" / "valid"
    invalid_dir = FIXTURES / "execution" / "invalid"

if __name__ == "__main__":
    unittest.main()