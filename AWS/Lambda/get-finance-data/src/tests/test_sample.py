import unittest

from main import handler

class Test_Sample(unittest.TestCase):
    def test_sample(self):
        result = handler(None, None)
        self.assertEqual('S&P 500 data printed and uploaded to S3 successfully.', result)