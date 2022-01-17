from grant import Grant
from amt import AMT

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
        total_amt_income = 0
        total_sale_income = 0
        other_income = self.other_income[str(year)]
        detail = {}
        for name,grant in self.grants.items():
            detail[name] = {}
            amt_income = grant.amt_income(year)
            total_amt_income += amt_income
            detail[name]["amt_income"] = amt_income
            sale_income = grant.sale_income(year)
            total_sale_income += sale_income
            detail[name]["sale_income"] = sale_income
        tax = AMT(year)
        amt_tax = tax.amt_tax(
            total_amt_income, 
            (total_sale_income + other_income))
        inc_tax = tax.inc_tax(total_sale_income+other_income)
        
        print("AMT tax: {}".format(amt_tax))
        print("ordinary tax: {}".format(inc_tax))
        
                
