from dataclasses import dataclass

from ...models.base_api_model import BaseModel


@dataclass(init=False)
class Offer(BaseModel):
    alias: str
    currency: int
