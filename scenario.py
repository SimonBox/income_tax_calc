from grant import Grant
from tax import Tax

import json
import datetime

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
                "ltcg": 0},
            "cal": {
                "income": 0,
                "amt": 0,
                "amt_tot": 0,
                "ltcg": 0},
            "tax" : 0,
            "me": {
                "held": 0,
                "outstanding": 0
            }
        }
        total_exercise_income = 0
        total_sale_income = 0
        other_income = self.other_income[str(year)]
        for name,grant in self.grants.items():
            detail[name] = {}
            exercise_income = grant.exercise_income(year)
            total_exercise_income += exercise_income
            sale_income = grant.sale_income(year)
            total_sale_income += sale_income
        
        tax = Tax(year)
        
        tax_data["irs"]["amt_tot"] = tax.amt_tax(
           total_exercise_income,
           total_sale_income + other_income) 
        tax_data["irs"]["income"] = tax.inc_tax(
           total_sale_income + other_income) 
        tax_data["irs"]["amt"] = max(
            0, 
            tax_data["irs"]["amt_tot"] - tax_data["irs"]["income"])
        
        tax_data["cal"]["amt_tot"] = tax.cal_amt_tax(
           total_exercise_income,
           total_sale_income + other_income) 
        tax_data["cal"]["income"] = tax.cal_inc_tax(
           total_sale_income + other_income) 
        tax_data["cal"]["amt"] = max(
            0, 
            tax_data["irs"]["amt_tot"] - tax_data["irs"]["income"])

        tax_data["tax"] = (
            tax_data["irs"]["amt"] +
            tax_data["irs"]["income"] +    
            tax_data["cal"]["amt"] +
            tax_data["cal"]["income"])

        tax_data["me"]["held"] = total_sale_income - tax_data["tax"]

        return tax_data
