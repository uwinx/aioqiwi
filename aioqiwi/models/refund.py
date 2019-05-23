from dataclasses import dataclass

from .base_api_model import BaseModel


@dataclass(init=False)
class Refund(BaseModel):
    @dataclass(init=False)
    class Amount(BaseModel):
        value: float
        currency: str

    datetime: str
    refund_id: str
    status: str
