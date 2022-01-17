from grant import Grant
import datetime
import unittest

class TestGrant(unittest.TestCase):
    def setUp(self):
        grant_date = datetime.date(2015,1,1)
        self.cmn_grant = Grant(grant_date, initial_shares=3000, strike_price=0)
        self.iso_grant_1 = Grant(
            grant_date, 
            initial_shares=6000, 
            strike_price=0.05)
        self.iso_grant_2 = Grant(
            grant_date, 
            initial_shares=1000, 
            strike_price=3.26)

    def test_initialization(self):
        self.assertEqual(self.cmn_grant.remaining_shares, 3000)
        self.assertEqual(self.iso_grant_1.remaining_shares, 6000)
        self.assertEqual(self.iso_grant_2.remaining_shares, 1000)
        self.assertEqual(self.cmn_grant.sold_shares(), 0)
        self.assertEqual(self.iso_grant_1.sold_shares(), 0)
        self.assertEqual(self.iso_grant_2.sold_shares(), 0)
        self.assertEqual(self.cmn_grant.unexercised_shares(), 0)
        self.assertEqual(self.iso_grant_1.unexercised_shares(), 6000)
        self.assertEqual(self.iso_grant_2.unexercised_shares(), 1000)

    def test_exercise_transaction(self): 
        T1_AMOUNT = 1000
        T1_DATE = datetime.date(2022, 2, 1)
        T1_SALE_PRICE = 10.0
        self.iso_grant_1.exercise(T1_DATE, T1_AMOUNT, T1_SALE_PRICE)

        self.assertEqual(len(self.iso_grant_1.exercise_transaction_history), 1)
        exercise_transaction = self.iso_grant_1.exercise_transaction_history[0]
        self.assertEqual(exercise_transaction.amount, T1_AMOUNT)
        self.assertEqual(exercise_transaction.transaction_date, T1_DATE)
        self.assertEqual(
            exercise_transaction.price_spread,
            (T1_SALE_PRICE - self.iso_grant_1.strike_price))
        self.assertEqual(self.iso_grant_1.exercised_shares, T1_AMOUNT)
        self.assertEqual(
            self.iso_grant_1.unexercised_shares(),
            (self.iso_grant_1.initial_share_count - T1_AMOUNT))
        YEAR = T1_DATE.year
        self.assertTrue(self.iso_grant_1._transaction_in_year(
            exercise_transaction, 
            YEAR))
        self.assertFalse(self.iso_grant_1._transaction_in_year(
            exercise_transaction, 
            YEAR + 1))
        INCOME = exercise_transaction.price_spread * T1_AMOUNT
        self.assertEqual(self.iso_grant_1.exercise_income(YEAR), INCOME)
        self.assertEqual(self.iso_grant_1.exercise_income(YEAR + 1), 0)


    def test_sale_transaction(self):
        S1_AMOUNT = 1000
        S1_DATE = datetime.date(2022, 2, 1)
        S1_SALE_PRICE = 10.0
        
        self.iso_grant_1.exercise(S1_DATE, S1_AMOUNT, S1_SALE_PRICE)
        self.assertEqual(self.iso_grant_1.sellable_amount(), S1_AMOUNT)
        self.iso_grant_1.sell(S1_DATE, S1_AMOUNT, S1_SALE_PRICE)
        self.assertEqual(len(self.iso_grant_1.sale_transaction_history), 1)
        self.assertEqual(self.iso_grant_1.sellable_amount(), 0)
        sale_transaction = self.iso_grant_1.sale_transaction_history[0]
        self.assertEqual(sale_transaction.amount, S1_AMOUNT)
        self.assertEqual(sale_transaction.transaction_date, S1_DATE)
        self.assertEqual(
            sale_transaction.price_spread, 
            S1_SALE_PRICE - self.iso_grant_1.strike_price)
        self.assertEqual(self.iso_grant_1.sold_shares(), S1_AMOUNT)
        self.assertEqual(
            self.iso_grant_1.remaining_shares,
            (self.iso_grant_1.initial_share_count - S1_AMOUNT))
        YEAR = S1_DATE.year
        INCOME = S1_AMOUNT * (S1_SALE_PRICE - self.iso_grant_1.strike_price)
        self.assertEqual(self.iso_grant_1.sale_income(YEAR), INCOME)
        self.assertEqual(self.iso_grant_1.sale_income(YEAR + 1), 0)
        self.assertEqual(self.iso_grant_1.amount_sold(YEAR), S1_AMOUNT)
        self.assertEqual(self.iso_grant_1.amount_sold(YEAR + 1), 0)


if __name__ == "__main__":
    unittest.main()
