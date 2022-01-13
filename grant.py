from datetime import date

class ExerciseTransaction:
    def __init__(self, transaction_date, amount, price_spread):
        self.transaction_date = transaction_date
        self.amount = amount
        self.price_spread = price_spread

class SaleTransaction:
    def __init__(self, transaction_date, amount, sale_price):
        self.transaction_date = transaction_date
        self.amount = amount
        self.sale_price = sale_price

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
        self.sale_transaction_history.append(
            SaleTransaction(date, amount, share_price))

    def sold_shares(self):
        return self.initial_share_count - self.remaining_shares
    
    def unexercised_shares(self):
        return self.initial_share_count - self.exercised_shares

    def sellable_amount(self):
        return self.exercised_shares - self.sold_shares()


