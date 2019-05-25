from dataclasses import dataclass

from ...models.base_api_model import BaseModel


@dataclass(init=False)
class Partner(BaseModel):
    title: str
    id: int

    maps: list = None
