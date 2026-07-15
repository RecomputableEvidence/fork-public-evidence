from csh_test_support import *

class TestReviewerReceipt(FixtureContractMixin, unittest.TestCase):
    checker = staticmethod(check_reviewer_receipt)
    valid_dir = FIXTURES / "reviewer-receipt" / "valid"
    invalid_dir = FIXTURES / "reviewer-receipt" / "invalid"

if __name__ == "__main__":
    unittest.main()