from grant import Grant
from tax import Tax

import json
import datetime

TAX_SUMMARY = """
TAX YEAR                            | {year}
------------------------------------
IRS
    Ordinary income tax             | {irs_inc}
    AMT                             | {irs_amt}
    Long term capital gains         | {irs_ltcg}
    Total                           | {irs_tot}
------------------------------------
CAL
    Ordinary income tax             | {cal_inc}
    AMT                             | {cal_amt}
    Long term capital gains         | {cal_ltcg}
    Total                           | {cal_tot}
------------------------------------
TOTAL TAX                           | {tax_tot}
------------------------------------
After Tax assets.
Net income from sales               | {me_inc}
Unsold (untaxed) assets             | {me_stock}
"""

class Scenario:
    def __init__(self, scenario_file_path):
        # load scenario
        scenario_data = { } 
        with open(scenario_file_path) as scenario_file:
            scenario_data = json.load(scenario_file)
        
        # Create grants
        self.grants = {}
        grant_data = scenario_data["initial_grants"]
        for grant in grant_data:
            self.grants[grant["name"]] = Grant(
                datetime.date.fromisoformat(grant["date"]),
                grant["amount"],
                grant["strike"])

        # Process transactions
        last_transaction_date = False
        for transaction in scenario_data["transactions"]:
            transaction_date = datetime.date.fromisoformat(transaction["date"])
            if last_transaction_date:
                if transaction_date < last_transaction_date:
                    raise ValueError("Transactions must be sequential")
            if transaction["type"] == "exercise":
                self.grants[transaction["grant"]].exercise(
                    transaction_date,
                    transaction["amount"],
                    transaction["share_price"])
            elif transaction["type"] == "sell":
                self.grants[transaction["grant"]].sell(
                    transaction_date,
                    transaction["amount"],
                    transaction["share_price"])
            last_transaction_date = transaction_date

        # Store other income
        self.other_income = scenario_data["other_income"]

    def calculate_tax(self, year):
        tax_data = {
            "irs": {
                "income": 0,
                "amt": 0,
                "amt_tot": 0,
                "ltcg": 0,
                "total": 0},
            "cal": {
                "income": 0,
                "amt": 0,
                "amt_tot": 0,
                "ltcg": 0,
                "total": 0},
            "tax" : 0,
            "me": {
                "held": 0,
                "outstanding": 0
            }
        }
        total_exercise_income = 0
        total_sale_income = 0
        total_ordinary_income = 0
        total_ltcg_income = 0
        other_income = self.other_income[str(year)]
        for name,grant in self.grants.items():
            total_exercise_income += grant.exercise_income(year)
            total_sale_income += grant.sale_income(year)
            total_ordinary_income += grant.ordinary_income(year)
            total_ltcg_income += grant.ltcg_income(year)
        
        #TODO hack  
        tax = Tax(2020)#Tax(year)
        
        tax_data["irs"]["amt_tot"] = tax.amt_tax(
           total_exercise_income,
           total_sale_income + other_income) 
        tax_data["irs"]["income"] = tax.inc_tax(
           total_ordinary_income + other_income) 
        tax_data["irs"]["ltcg"] = tax.ltcg_tax(
            total_ltcg_income,
            total_ordinary_income + other_income)
        tax_data["irs"]["amt"] = max(
            0, 
            ( tax_data["irs"]["amt_tot"]
            - tax_data["irs"]["income"]
            - tax_data["irs"]["ltcg"]))
        tax_data["irs"]["total"] = (
            tax_data["irs"]["amt"] + 
            tax_data["irs"]["income"] +
            tax_data["irs"]["ltcg"])
        
        tax_data["cal"]["amt_tot"] = tax.cal_amt_tax(
           total_exercise_income,
           total_sale_income + other_income) 
        tax_data["cal"]["income"] = tax.cal_inc_tax(
           total_ordinary_income + other_income) 
        tax_data["cal"]["ltcg"] = tax.cal_ltcg_tax(
            total_ltcg_income,
            total_ordinary_income + other_income)
        tax_data["cal"]["amt"] = max(
            0, 
            ( tax_data["cal"]["amt_tot"] 
            - tax_data["cal"]["income"]
            - tax_data["cal"]["ltcg"]))
        tax_data["cal"]["total"] = (
            tax_data["cal"]["amt"] + 
            tax_data["cal"]["income"] +
            tax_data["cal"]["income"]) 
        tax_data["tax"] = (
            tax_data["irs"]["total"] +
            tax_data["cal"]["total"])

        tax_data["me"]["held"] = total_sale_income - tax_data["tax"]

        return tax_data

    def display_tax_data(self, year):
        tax_data = self.calculate_tax(year)
        tax_str = TAX_SUMMARY.format(
            year = year,
            irs_inc = tax_data["irs"]["income"],
            irs_amt = tax_data["irs"]["amt"],
            irs_ltcg = tax_data["irs"]["ltcg"],
            irs_tot = tax_data["irs"]["total"],
            cal_inc = tax_data["cal"]["income"],
            cal_amt = tax_data["cal"]["amt"],
            cal_ltcg = tax_data["cal"]["ltcg"],
            cal_tot = tax_data["cal"]["total"],
            tax_tot = tax_data["tax"],
            me_inc = tax_data["me"]["held"],
            me_stock = tax_data["me"]["outstanding"])
        print(tax_str)


