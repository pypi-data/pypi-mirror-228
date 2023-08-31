import unittest
import parameterized
from bewe.backtest import holder
from bewe.alpha_seeker import base_strategy


class BankTest(unittest.TestCase):

    def setUp(self) -> None:
        self.bank = holder.Bank(1000000)

    def test_create_bank(self):
        bank = holder.Bank(50000)
        self.assertEqual(bank.budget, 50000)

    @parameterized.parameterized.expand([
        (0.4, 2.0, 10000, 1000.0),
        (0.5, 1.2, 50000, 4167.0),
        (0.2, 1.2, 10000, 0.0)
    ])
    def test_kelly_formula(self, conf, gain, budget, expected):
        actual = self.bank._kelly_formula(confidence=conf, gain=gain, budget=budget)
        self.assertEqual(expected, actual)

    @parameterized.parameterized.expand([
        (0.5, 1.5, 50, 3000, 850000),
        (0.2, 1.5, 50, 0, 1000000)
    ])
    def test_act(self, conf, gain, target_price, expected_volume, expected_budget):
        asset_name = 'mock'
        execution = base_strategy.Execution(
            action=base_strategy.Action.BUY,
            confidence=conf,
            gain=gain
        )

        self.bank.act(execution, asset_name, target_price)

        self.assertTrue(asset_name in self.bank.asset)
        self.assertEqual(self.bank.asset[asset_name].volume, expected_volume)
        self.assertEqual(self.bank.budget, expected_budget)


if __name__ == '__main__':
    unittest.main()
