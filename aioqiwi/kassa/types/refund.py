"""Main model: Refund"""
from pydantic import Field

from aioqiwi.types import BaseModel


class Amount(BaseModel):
    """Object: amount"""

    value: float = Field(..., alias="value")
    currency: str = Field(..., alias="currency")


class Refund(BaseModel):
    """Object: Refund"""

    datetime: str = Field(..., alias="datetime")
    refund_id: str = Field(..., alias="refundId")
    status: str = Field(..., alias="status")
    amount: Amount = Field(..., alias="amount")


__all__ = ("Refund",)
