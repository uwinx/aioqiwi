from dataclasses import dataclass

from ...models.base_api_model import BaseModel


@dataclass(init=False)
class BillUpdate(BaseModel):
    @dataclass(init=False)
    class Bill(BaseModel):
        site_id: str
        bill_id: str

        @dataclass(init=False)
        class Amount(BaseModel):
            value: str
            currency: str

        @dataclass(init=False)
        class Status(BaseModel):
            value: str
            datetime: str

        @dataclass(init=False)
        class Customer(BaseModel):
            phone: str = None
            account: str = None
            email: str = None

        @dataclass(init=False)
        class CustomFields(BaseModel):
            def __setattr__(self, key, value):
                setattr(self, key, value)

        creation_date_time: str
        expiration_date_time: str

    version: str
