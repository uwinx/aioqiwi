from dataclasses import dataclass

from ...models.base_api_model import BaseModel


@dataclass(init=False)
class Terminal(BaseModel):
    terminal_id: int
    ttp_id: int
    last_active: str
    count: int

    @dataclass(init=False)
    class Coordinate(BaseModel):
        latitude: float
        longitude: float
        precision: int

        @property
        def latlon(self):
            return self.latitude, self.longitude

    address: str
    verified: bool
    label: str
    description: str
    cash_allowed: bool
    card_allowed: bool
    identification_type: int
