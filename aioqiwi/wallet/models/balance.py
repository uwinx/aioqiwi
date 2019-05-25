from dataclasses import dataclass
from typing import List

from ...models.base_api_model import BaseModel


@dataclass(init=False)
class Account(BaseModel):
    alias: str
    fs_alias: str
    bank_alias: str
    title: str

    @dataclass(init=False)
    class Type(BaseModel):
        id: str
        title: str

    has_balance: bool

    @dataclass(init=False)
    class Balance:
        amount: int
        currency: int


@dataclass(init=False)
class Balance(BaseModel):
    accounts: List[Account]
