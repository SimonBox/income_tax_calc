from tax import Tax
import datetime
import json
import unittest

class TestTax(unittest.TestCase):
    def setUp(self):
        YEAR = 2020
        self.tax = Tax(YEAR)
        self.tax_constants = {}
        with open('tax_constants.json') as tc_file:
            tc_data = json.load(tc_file)
            self.tax_constants = tc_data[str(YEAR)]

    def test_initialization(self):
        self.assertListEqual(
            self.tax.amt_rates, 
            self.tax_constants["irs"]["amt_rates"])
        self.assertListEqual(
            self.tax.inc_rates, 
            self.tax_constants["irs"]["inc_rates"])
        self.assertListEqual(
            self.tax.cal_amt_rates, 
            self.tax_constants["cal"]["amt_rates"])
        self.assertListEqual(
            self.tax.cal_inc_rates, 
            self.tax_constants["cal"]["inc_rates"])

    def test_tax_rate_calc(self):
        carried_over_income = 0
        carried_over_tax = 0
        skip_first = True
        test_rates = self.tax.cal_inc_rates
        test_rate = 0
        for rate in self.tax.cal_inc_rates:
            if skip_first:
                skip_first = False
                test_rate = rate["pc_rate"] / 100.
                continue
            income = rate["bracket_l"]
            tax = self.tax._tax_from_rates(income, test_rates)
            income_in_band = income - carried_over_income
            tax_in_band = tax - carried_over_tax
            self.assertAlmostEqual(tax_in_band, income_in_band * test_rate)
            carried_over_income = income
            carried_over_tax = tax
            test_rate = rate["pc_rate"] / 100.

    def test_offset_rates_calc(self):
        offset = 13000
        test_rates = self.tax.cal_ltcg_rates
        offset_rates = self.tax._offset_rates(test_rates, offset)
        self.assertNotEqual(test_rates, offset_rates)
        incomes = [ rate["bracket_l"] for rate in test_rates]
        for income in incomes:
            self.assertAlmostEqual(
                self.tax._tax_from_rates(income, test_rates),
                self.tax._tax_from_rates(income - offset, offset_rates))

    def test_ltcg_tax_calc(self):
        lt_income = 10.0 # just needs to be small in comparison to bands.
        for rate in self.tax.ltcg_rates:
            other_income = rate["bracket_l"]
            test_rate = rate["pc_rate"] / 100.
            test_tax = lt_income * test_rate
            calc_tax = self.tax.ltcg_tax(lt_income, other_income)
            self.assertAlmostEqual(test_tax, calc_tax)

    def test_amt_income(self):
        self.assertEqual(
            self.tax._amt_income(self.tax.amt_exemption, 0),
            0)
        self.assertEqual(
            self.tax._amt_income(self.tax.amt_phaseout, 0),
            self.tax.amt_phaseout - self.tax.amt_exemption)
        self.assertEqual(
            self.tax._amt_income(2.*self.tax.amt_phaseout, 0),
            2.*self.tax.amt_phaseout)
        
        
                


if __name__ == "__main__":
    unittest.main()
