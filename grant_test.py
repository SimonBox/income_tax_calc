from grant import Grant
import datetime
import unittest

class TestGrant(unittest.TestCase):
    def setUp(self):
        self.cmn_grant = Grant(initial_shares=3000, strike_price=0)
        self.iso_grant_1 = Grant(initial_shares=6000, strike_price=0.05)
        self.iso_grant_2 = Grant(initial_shares=1000, strike_price=3.26)

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
        self.iso_grant_1.exercise(T1_AMOUNT, T1_DATE, T1_SALE_PRICE)

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

    def test_sale_transaction(self):
        S1_AMOUNT = 1000
        S1_DATE = datetime.date(2022, 2, 1)
        S1_SALE_PRICE = 10.0
        
        self.iso_grant_1.exercise(S1_AMOUNT, S1_DATE, S1_SALE_PRICE)
        self.iso_grant_1.sell(S1_AMOUNT, S1_DATE, S1_SALE_PRICE)
        self.assertEqual(len(self.iso_grant_1.sale_transaction_history), 1)
        sale_transaction = self.iso_grant_1.sale_transaction_history[0]
        self.assertEqual(sale_transaction.amount, S1_AMOUNT)
        self.assertEqual(sale_transaction.transaction_date, S1_DATE)
        self.assertEqual(sale_transaction.sale_price, S1_SALE_PRICE)
        self.assertEqual(
            self.iso_grant_1.remaining_shares,
            (self.iso_grant_1.initial_share_count - S1_AMOUNT))


if __name__ == "__main__":
    unittest.main()
