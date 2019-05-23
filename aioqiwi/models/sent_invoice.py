from dataclasses import dataclass

from .base_api_model import BaseModel


@dataclass(init=False)
class _CustomFields(BaseModel):
    def __setattr__(self, key, value):
        setattr(self, key, value)


@dataclass(init=False)
class Invoice(BaseModel):
    site_id: str
    bill_id: str

    @dataclass(init=False)
    class Amount(BaseModel):
        currency: str
        value: str

    @dataclass(init=False)
    class Status(BaseModel):
        value: str
        changed_date_time: str

    @dataclass(init=False)
    class Customer(BaseModel):
        phone: str
        account: str

    comment: str
    creation_date_time: str
    expiration_date_time: str
    pay_url: str

    CustomFields = _CustomFields
