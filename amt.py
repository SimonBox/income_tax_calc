import datetime

class AMT:
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

        self.cal_amt_rates = tax_constants["cal"]["amt_rates"]
        self.cal_inc_rates = tax_constants["cal"]["inc_rates"]


    def amt_tax(self, exercise_income, income):
        amt_income = exercise_income + income
        exemption = (
            self.amt_exemption if amt_income <= self.amt_phaseout else
            max(0, self.amt_exemption - 0.25*(amt_income - self.amt_phaseout)))
        amt_income -= exemption  
        
        
        irs_amt = self._tax_from_rates(amt_income, self.amt_rates()
        cal_amt = self._tax_from_rates(amt_income, self.cal_amt_rates()
        return {"irs_amt" : irs_amt, "cal_amt" : cal_amt}

    def inc_tax(self, income):
        irs_inc = self._tax_from_rates(income, self.inc_rates()
        cal_inc = self._tax_from_rates(income, self.cal_inc_rates()
        return {"irs_inc" : irs_inc, "cal_inc" : cal_inc}
        

    def _tax_from_rates(self, income, rates):
        tax = 0
        for bracket in reversed(rates):
            if income > bracket['bracket_l']:
                exess = amt_income - bracket['bracket_l']
                income -= exess
                tax += exess * (bracket['pc_rate']/100.0)

        return tax

