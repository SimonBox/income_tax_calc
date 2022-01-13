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
                
