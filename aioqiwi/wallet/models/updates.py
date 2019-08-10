from dataclasses import dataclass

from ...models.base_api_model import BaseModel


@dataclass(init=False)
class QiwiUpdate(BaseModel):
    message_id: str
    hook_id: str

    @dataclass(init=False)
    class Payment(BaseModel):
        txn_id: str
        date: str
        type: str
        status: str
        error_code: str
        person_id: int
        account: str
        comment: str
        provider: int
        sign_fields: str

        @dataclass(init=False)
        class Sum(BaseModel):
            amount: float
            currency: int

        @dataclass(init=False)
        class Commission(BaseModel):
            amount: float
            currency: int

        @dataclass(init=False)
        class Total(BaseModel):
            amount: float
            currency: int

    hash: str
    version: str
    test: bool
