from dataclasses import dataclass

from .base_api_model import BaseModel


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

        @dataclass(init=False)
        class Sum(BaseModel):
            amount: float
            currency: int
            commission: int

        @dataclass(init=False)
        class Total(BaseModel):
            amount: float
            currency: int
            sign_fields: str

    hash: str
    version: str
    test: bool
