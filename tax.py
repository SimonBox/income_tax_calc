import datetime
import json
import copy

class Tax:
    def __init__(self, year, mfj=True):
        y_str = str(year)
        tax_constants = {}
        with open('tax_constants.json') as tc_file:
            tc_data = json.load(tc_file)
            tax_constants = tc_data[y_str]

        self.year = year
                
        self.amt_exemption = tax_constants["irs"]["amt_exemption"]
        self.amt_phaseout = tax_constants["irs"]["amt_phaseout"]
        self.amt_rates = tax_constants["irs"]["amt_rates"]
        self.inc_rates = tax_constants["irs"]["inc_rates"]
        self.ltcg_rates = tax_constants["irs"]["ltcg_rates"]
        self.standard_deduction = tax_constants["irs"]["standard_deduction"]

        self.cal_amt_rates = tax_constants["cal"]["amt_rates"]
        self.cal_inc_rates = tax_constants["cal"]["inc_rates"]
        self.cal_ltcg_rates = tax_constants["cal"]["ltcg_rates"]


    def amt_tax(self, exercise_income, income):
        amt_income = self._amt_income(exercise_income, income) 
        return self._tax_from_rates(amt_income, self.amt_rates)
    
    def cal_amt_tax(self, exercise_income, income):
        amt_income = self._amt_income(exercise_income, income) 
        return self._tax_from_rates(amt_income, self.cal_amt_rates)

    def _amt_income(self, exercise_income, income):
        amt_income = exercise_income + income
        exemption = (
            self.amt_exemption if amt_income <= self.amt_phaseout else
            max(0, self.amt_exemption - 0.25*(amt_income - self.amt_phaseout)))
        amt_income -= exemption
        return amt_income

    def inc_tax(self, income):
        income = max(0, income - self.standard_deduction)
        return self._tax_from_rates(income, self.inc_rates)
    
    def cal_inc_tax(self, income):
        income = max(0, income - self.standard_deduction)
        return self._tax_from_rates(income, self.cal_inc_rates)

    def ltcg_tax(self, lt_income, other_income):
        rates = self._offset_rates(self.ltcg_rates, other_income)
        return self._tax_from_rates(lt_income, rates)
    
    def cal_ltcg_tax(self, lt_income, other_income):
        rates = self._offset_rates(self.cal_ltcg_rates, other_income)
        return self._tax_from_rates(lt_income, rates)

    def _tax_from_rates(self, income, rates):
        tax = 0
        for bracket in reversed(rates):
            if income > bracket['bracket_l'] and income > 0:
                exess = income - bracket['bracket_l']
                income -= exess
                tax += exess * (bracket['pc_rate']/100.0)

        return tax

    def _offset_rates(self, rates, offset):
        offset_rates = copy.deepcopy(rates)
        for rate in offset_rates:
            rate["bracket_l"] -= offset
        return offset_rates

