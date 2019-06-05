from dataclasses import dataclass

from ...models.base_api_model import BaseModel


@dataclass(init=False)
class Commission(BaseModel):
    provider_id: int

    @dataclass(init=False)
    class WithdrawSum(BaseModel):
        amount: float
        currency: str

    @dataclass(init=False)
    class EnrollmentSum(BaseModel):
        amount: int
        currency: str

    @dataclass(init=False)
    class QwCommission(BaseModel):
        # true and real payment commission
        amount: float
        currency: str

    @dataclass(init=False)
    class FundingSourceCommission(BaseModel):
        amount: int
        currency: str

    withdraw_to_enrollment_rate: int
