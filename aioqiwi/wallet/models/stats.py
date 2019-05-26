from dataclasses import dataclass

from typing import List

from ...models.base_api_model import BaseModel
from ...utils.currency_utils import Currency


@dataclass(init=False)
class Payment(BaseModel):
    amount: float
    currency: str


@dataclass(init=False)
class Stats(BaseModel):
    incoming_total: List[Payment]
    outgoing_total: List[Payment]

    def profit(self, currency: int or str = Currency['RUB'].isoformat):
        return sum(
            out.amount - inc.amount
            for inc, out in zip(self.incoming_total, self.outgoing_total)
            if inc.currency == out.currency == currency
        )
