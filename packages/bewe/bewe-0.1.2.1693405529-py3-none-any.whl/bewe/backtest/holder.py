import dataclasses
from bewe.alpha_seeker import base_strategy
from typing import Any, Dict, Optional, Sequence, Tuple

_MIN_GAIN_RATE = 0.1
_MIN_WIN_RATE = 0.05


@dataclasses.dataclass
class Holder:
    name: Any
    hold_volumes: Sequence[float] = dataclasses.field(default_factory=list)
    hold_prices: Sequence[float] = dataclasses.field(default_factory=list)

    @property
    def volume(self) -> float:
        return sum(self.hold_volumes)

    @property
    def total_cost(self) -> float:
        total = 0.0
        for price, volume in zip(self.hold_prices, self.hold_volumes):
            total += price * volume
        return abs(total)
            
    @property
    def avg_cost(self) -> float:
        if self.volume == 0:
            return 0.0
        return self.total_cost / self.volume
        
    def current_profit(self, current_price: float):
        return self.volume * current_price - self.total_cost
        
    def current_value(self, current_price: float):
        return self.cost + self.current_profit(current_price)
    
    def execute(self, price: float, volume: float, lever: float = 1.0):
        self.hold_volumes.append(volume)
        self.hold_prices.append(price)


class Bank:
    def __init__(self, budget: float, win_rate: float = 0.3, gain_rate: float = 0.2):
        self.budget = budget
        self.init_value = budget
        self.asset: Dict[str, Holder] = {}
        self.history: Sequence[Tuple[base_strategy.Execution, float]] = []
        self.win_rate = win_rate
        self.gain_rate = gain_rate
        self.sell_record = [win_rate]
        self.profit_record = [gain_rate]

    def _kelly_formula(
            self,
            confidence: Optional[float] = None, 
            budget: Optional[float] = None,
            gain: Optional[float] = None) -> float:

        c = self.win_rate if not confidence else confidence
        b = self.budget if not budget else budget
        g = self.gain_rate if not gain else gain

        if g < 1.0:
            raise ValueError(f'Gain rate {g} is lower than 1.0.')
        kelly_value = round(b * (g * c + c - 1) / g)
        return max(kelly_value, 0.0)

    def review(self) -> None:
        self.win_rate = max(sum(self.sell_record) / len(self.sell_record), _MIN_WIN_RATE)
        self.gain_rate = max(sum(self.profit_record) / len(self.profit_record), _MIN_GAIN_RATE)

    def act(self, execution: base_strategy.Execution, asset_name: str, target: float, volume: float = 0) -> None:

        if asset_name not in self.asset:
            self.asset[asset_name] = Holder(asset_name)
        
        asset: Holder = self.asset[asset_name]
        
        if execution.action == base_strategy.Action.BUY:
            default_units = self._kelly_formula(confidence=execution.confidence, gain=execution.gain) // target
            possible_units = default_units if not volume else volume

        elif execution.action == base_strategy.Action.SELL:
            asset_current_value = asset.current_value
            default_units = self._kelly_formula(
                confidence=execution.confidence,
                budget=asset_current_value,
                gain=execution.gain) // target
            possible_units = - default_units if not volume else volume

            review_record = 1 if target > asset.avg_cost else 0
            profit_ratio = target / asset.avg_cost - 1

            self.sell_record.append(review_record)
            self.profit_record.append(profit_ratio)
            
        else:
            possible_units = 0.0

        possible_units = (possible_units//1000) * 1000

        if possible_units < 0.0 and execution.action != base_strategy.Action.SELL:
            raise ValueError('Action should be Buy but the target is negative.')

        self.budget -= possible_units * target
        self.history.append((execution, possible_units))
        asset.execute(target, possible_units)
        self.review()
        