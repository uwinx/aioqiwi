"""
Main model: Commission
"""
from pydantic import Field

from aioqiwi.types import BaseModel


class FundingSourceCommission(BaseModel):
    """Object: fundingSourceCommission"""

    amount: float = Field(..., alias="amount")
    currency: str = Field(..., alias="currency")


class QwCommission(BaseModel):
    """Object: qwCommission"""

    amount: float = Field(..., alias="amount")
    currency: str = Field(..., alias="currency")


class EnrollmentSum(BaseModel):
    """Object: enrollmentSum"""

    amount: float = Field(..., alias="amount")
    currency: str = Field(..., alias="currency")


class WithdrawSum(BaseModel):
    """Object: withdrawSum"""

    amount: float = Field(..., alias="amount")
    currency: str = Field(..., alias="currency")


class Commission(BaseModel):
    """Object: Commission"""

    provider_id: int = Field(..., alias="providerId")
    withdraw_to_enrollment_rate: int = Field(..., alias="withdrawToEnrollmentRate")
    withdraw_sum: WithdrawSum = Field(..., alias="withdrawSum")
    enrollment_sum: EnrollmentSum = Field(..., alias="enrollmentSum")
    qw_commission: QwCommission = Field(..., alias="qwCommission")
    funding_source_commission: FundingSourceCommission = Field(
        ..., alias="fundingSourceCommission"
    )
