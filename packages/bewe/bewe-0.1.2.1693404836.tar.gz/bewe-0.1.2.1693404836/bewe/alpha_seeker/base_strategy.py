import dataclasses
import enum
from bewe.alpha_seeker import base_data
from typing import Optional


class Action(enum.Enum):
    BUY = 1
    SELL = 2
    HOLD = 3


@dataclasses.dataclass
class Execution:
    action: Action
    confidence: Optional[float] = None
    gain: Optional[float] = None

    def __post_init__(self):
        if self.gain < 1.0:
            raise ValueError(f'gain value should be greater than 1.0, {self.gain} found.')
        if self.confidence < 0.0:
            raise ValueError(f'confidence should be greater than 0.0, {self.confidence} found.')


class Strategy:
    strategy_name = 'Base Strategy'
    required_format = None

    def __post_init__(self):
        if not self.required_format:
            raise ValueError('required_format should be defined.')

    def predict(self, data: base_data.DataUnit) -> Execution:
        raise NotImplementedError
    
    def validate_data(self, data: base_data.DataUnit) -> bool:
        raise NotImplementedError
