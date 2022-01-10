from amt import AMT
import datetime
import unittest

class TestAMT(unittest.TestCase):
    def setUp(self):
        self.amt = AMT(2020)

    def test_initialization(self):
        #self.assertEqual(self.amt.amt_rates[0]['pc_rate'], 26)
        self.assertEqual(self.amt.inc_rates[3]['bracket_l'], 178151)

    def test_toy_amt(self):
        amt_income = 1000000 * (10.1 - 0.1)
        income = 0
        amt_tax = self.amt.amt_tax(amt_income, income)
        print("AMT tax: {}".format(amt_tax))

if __name__ == "__main__":
    unittest.main()
