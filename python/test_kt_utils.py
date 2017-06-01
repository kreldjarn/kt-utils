import unittest
import time

import kt_utils


class TestKtUtils(unittest.TestCase):
    def test_is_invalid(self):
        # Too short
        self.assertFalse(kt_utils.is_valid('111111'))
        # Non-integer string
        self.assertFalse(kt_utils.is_valid('1A2B3C4D5E'))
        # Fails checksum
        self.assertFalse(kt_utils.is_valid('1101115040'))

if __name__ == '__main__':
    unittest.main()
