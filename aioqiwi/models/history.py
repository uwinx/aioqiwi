from dataclasses import dataclass
from typing import List

from .base_api_model import BaseModel


@dataclass(init=False)
class History(BaseModel):
    account: str
    comment: str

    @dataclass(init=False)
    class Commission(BaseModel):
        amount: int
        currency: int

    currencyRate: int
    date: str
    error: str
    errorCode: int

    @dataclass(init=False)
    class Features(BaseModel):
        bank_document_available: bool
        bank_document_ready: bool
        chat_available: bool
        cheque_ready: bool
        favorite_payment_enabled: bool
        greeting_card_attached: bool
        regular_payment_enabled: bool
        repeat_payment_enabled: bool

    payment_extras: list
    person_id: int

    @dataclass(init=False)
    class Provider(BaseModel):
        description: str
        extras: list
        id: int
        keys: str
        logo_url: str
        long_name: str
        short_name: str
        site_url: str

    @dataclass(init=False)
    class ServiceExtras(BaseModel):
        ...

    @dataclass(init=False)
    class Source(BaseModel):
        description: str
        extras: list
        id: int
        keys: str
        logo_url: str
        long_name: str
        short_name: str
        site_url: str

    status: str
    status_text: str

    @dataclass(init=False)
    class Sum(BaseModel):
        amount: int
        currency: int

    @dataclass(init=False)
    class Total(BaseModel):
        amount: int
        currency: int

    trm_txn_id: str
    txn_id: int
    type: str

    @dataclass(init=False)
    class View(BaseModel):
        account: str
        title: str


@dataclass(init=False)
class HistoryList(BaseModel):
    data: List[History]
    next_txn_id: int
    next_txn_date: str

    @property
    def reversed(self):
        return reversed(self.data)
