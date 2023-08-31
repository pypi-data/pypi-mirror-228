import unittest
from bewe.backtest import holder
from bewe.backtest import backtester as bt


class TestBacktester(unittest.TestCase):

    def test_create(self):
        bank = holder.Bank(1000000)
        trader = bt.BackTester(bank)
        self.assertIsInstance(trader, bt.BackTester)


if __name__ == '__main__':
    unittest.main()
