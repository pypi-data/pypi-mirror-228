from bewe.alpha_seeker import base_strategy
from bewe.alpha_seeker import base_data
from bewe.backtest import holder


class BackTester:
    def __init__(self, bank: holder.Bank):
        self.bank = bank

    def backtest(self, strategy: base_strategy.Strategy, container: base_data.DataContainer):
        for unit in container:
            execution_plan = strategy.predict(unit)
            self.bank.act(execution_plan, container.asset_name, unit.actional_price)
