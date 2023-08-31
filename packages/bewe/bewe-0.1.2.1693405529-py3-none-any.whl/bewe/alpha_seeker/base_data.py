import dataclasses
import pandas as pd
from typing import Any, Mapping, Optional, Sequence


@dataclasses.dataclass(frozen=True)
class DataFormat:
    required_field: Sequence[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class DataUnit:
    format: DataFormat
    data: Mapping[Any, Any]
    actionable_price: float

    def __post_init__(self):
        for col in self.format.required_field:
            if col not in self.data:
                raise KeyError(f'{col} is required for the target unit.')
            self.__setattr__(col, self.data[col])


class DataContainer:
    name = 'BaseContainer'

    def __init__(self, asset_name: str, data: Optional[Sequence[DataUnit]] = None):
        self.asset_name = asset_name
        self.data: Optional[Sequence[DataUnit]] = data
        self.index = 0
        self.size = 0 if not self.data else len(self.data)
        self.format = None

    def __iter__(self) -> 'DataContainer':
        return self

    def __next__(self) -> DataUnit:
        if self.index == self.size:
            raise StopIteration

        if not self.data:
            raise StopIteration

        unit = self.data[self.index]
        self.index += 1
        return unit

    def __len__(self):
        return 0 if not self.data else len(self.data)
    
    def transform(self, data: pd.DataFrame):
        raise NotImplementedError
    
    def get_format(self) -> DataFormat:
        if not self.format:
            raise ValueError
        return self.format
