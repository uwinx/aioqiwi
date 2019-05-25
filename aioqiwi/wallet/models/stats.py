from dataclasses import dataclass

from typing import List

from ...models.base_api_model import BaseModel


@dataclass(init=False)
class Payment(BaseModel):
    amount: float
    currency: str


@dataclass(init=False)
class Stats(BaseModel):
    incoming_total: List[Payment]
    outgoing_total: List[Payment]

    @property
    def profit(self):
        return sum(
            out.amount - inc.amount
            for inc, out in zip(self.incoming_total, self.outgoing_total)
        )
