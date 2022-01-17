import datetime

class ExerciseTransaction:
    def __init__(self, transaction_date, amount, price_spread):
        self.transaction_date = transaction_date
        self.amount = amount
        self.price_spread = price_spread

class SaleTransaction:
    def __init__(self, transaction_date, amount, price_spread, lt_amount):
        self.transaction_date = transaction_date
        self.amount = amount
        self.long_term_eligible_amount = lt_amount
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
        self.remaining_shares -= amount
        long_term_amount = min(amount, self.long_term_eligible_amount(date))
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

    def long_term_eligible_amount(self, date):
        lt_amount = 0
        for ex in self.exercise_transaction_history:
            if (date - ex.transaction_date) > datetime.timedelta(days=365):        
                lt_amount += ex.amount
            else:
                break
        # TODO this is a worst-case should calculate properly
        lt_amount -= self.sold_shares()
        return max(0, lt_amount)

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
    
    def amt_income(self, year):
        ex_income = 0
        ex_amount = 0
        for ex in self.exercise_transaction_history:
            if self._transaction_in_year(ex, year):        
                ex_amount += ex.amount
                ex_income += ex.price_spread * ex.amount

        amount_sold = self.amount_sold(year)

        if ex_amount and amount_sold:
            # TODO probably not the right way
            ex_income = max(
                0, 
                ex_income * ((ex_amount - amount_sold) / float(ex_amount)))
        return ex_income


    def _transaction_in_year(self, transaction, year):
       return (
        transaction.transaction_date >= datetime.date(year, 1, 1) and
        transaction.transaction_date < datetime.date(year + 1, 1, 1))
                
