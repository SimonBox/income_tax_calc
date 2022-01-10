from datetime import date

class ExerciseTransaction:
    def __init__(self, amount, transaction_date, price_spread):
        self.amount = amount
        self.transaction_date = transaction_date
        self.price_spread = price_spread

class SaleTransaction:
    def __init__(self, amount, transaction_date, sale_price):
        self.amount = amount
        self.transaction_date = transaction_date
        self.sale_price = sale_price

class Grant:
    def __init__(self, initial_shares=0, strike_price=0):
        self.initial_share_count = initial_shares
        self.strike_price = strike_price
        self.remaining_shares = self.initial_share_count
        self.exercised_shares = (
            0 if strike_price else self.initial_share_count)
        self.exercise_transaction_history = []
        self.sale_transaction_history = []

    def exercise(self, amount, date, share_price):
        if (amount > self.unexercised_shares()):
            raise ValueError("Cannot exercise more shares than are remaining")
        self.exercised_shares += amount
        self.exercise_transaction_history.append(
            ExerciseTransaction(amount,date, share_price-self.strike_price))
    
    def sell(self, amount, date, share_price):
        if (amount > self.remaining_shares):
            raise ValueError("Cannot sell more shares than are remaining")
        if (amount > self.sellable_amount()):
            raise ValueError(
            "Cannot sell unexercised shares please exercise first")
        self.remaining_shares -= amount
        self.sale_transaction_history.append(
            SaleTransaction(amount,date,share_price))

    def sold_shares(self):
        return self.initial_share_count - self.remaining_shares
    
    def unexercised_shares(self):
        return self.initial_share_count - self.exercised_shares

    def sellable_amount(self):
        return self.exercised_shares - self.sold_shares()


