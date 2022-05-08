import datetime

class ExerciseTransaction:
    def __init__(self, transaction_date, amount, price_spread):
        self.transaction_date = transaction_date
        self.amount = amount
        self.price_spread = price_spread
        self.sold = 0
        self.income_eligible_amount = amount;

class SaleTransaction:
    def __init__(self, transaction_date, amount, price_spread, lt_amount):
        self.transaction_date = transaction_date
        self.amount = amount
        self.long_term_amount = lt_amount
        self.price_spread = price_spread

class Grant:
    def __init__(self, grant_date, initial_shares, strike_price):
        self.grant_date = grant_date
        self.initial_share_count = initial_shares
        self.strike_price = strike_price
        self.remaining_shares = self.initial_share_count
        self.exercised_shares = (
            0 if strike_price else self.initial_share_count)
        self.exercise_transaction_history = []
        self.sale_transaction_history = []

    def exercise(self, date, amount, share_price):
        if (amount > self.unexercised_shares()):
            raise ValueError("Cannot exercise more shares than are remaining")
        self.exercised_shares += amount
        self.exercise_transaction_history.append(
            ExerciseTransaction(date, amount, share_price-self.strike_price))
    
    def sell(self, date, amount, share_price):
        if (amount > self.remaining_shares):
            raise ValueError("Cannot sell more shares than are remaining")
        if (amount > self.sellable_amount()):
            raise ValueError(
            "Cannot sell unexercised shares please exercise first")
        # Assume we sell the oldest first, which is reasonable given
        # that we only care about this for LTCG.
        remain_to_sell = amount;
        long_term_amount = 0
        for ex in self.exercise_transaction_history:
            available = ex.amount - ex.sold
            selling = min(available, remain_to_sell)
            ex.sold += selling
            remain_to_sell -= selling
            if self.long_term_eligible(date, ex):
                long_term_amount += selling
            if date.year == ex.date:
                ex.income_eligible_amount -= selling
            if not remain_to_sell:
                break
        
        self.remaining_shares -= amount
        self.sale_transaction_history.append(
            SaleTransaction(
                date, 
                amount, 
                share_price - self.strike_price, 
                long_term_amount))

    def sold_shares(self):
        return self.initial_share_count - self.remaining_shares
    
    def unexercised_shares(self):
        return self.initial_share_count - self.exercised_shares

    def sellable_amount(self):
        return self.exercised_shares - self.sold_shares()

    def long_term_eligible(self, date, exercise_transaction):
        if (date - exercise_transaction.transaction_date) 
                > datetime.timedelta(days=365):        
            return True
        return False

    def sale_income(self, year):
        income = 0
        for sale in self.sale_transaction_history:
            if self._transaction_in_year(sale, year):        
                income += sale.price_spread * sale.amount
        return income

    def amount_sold(self, year):
        amount = 0
        for sale in self.sale_transaction_history:
            if self._transaction_in_year(sale, year):        
                amount += sale.amount
        return amount 
    
    def exercise_income(self, year):
        ex_income = 0
        for ex in self.exercise_transaction_history:
            if self._transaction_in_year(ex, year):        
                ex_income += ex.price_spread * ex.income_eligible_amount

        return ex_income

    def ordinary_income(self, year):
        ordinary_income = 0
        for sale in self.sale_transaction_history:
            if self._transaction_in_year(sale, year):
                ordinary_income += (
                    sale.amount 
                    - sale.long_term_amount) * sale.price_spread

        return ordinary_income

    def ltcg_income(self, year):
        ltcg_income = 0
        for sale in self.sale_transaction_history:
            if self._transaction_in_year(sale, year):
                ltcg_income += sale.long_term_amount * sale.price_spread

        return ltcg_income


    def _transaction_in_year(self, transaction, year):
       return (
        transaction.transaction_date >= datetime.date(year, 1, 1) and
        transaction.transaction_date < datetime.date(year + 1, 1, 1))
                
