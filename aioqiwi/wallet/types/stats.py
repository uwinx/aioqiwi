"""
Main model: Stats
"""
from typing import List

from pydantic import Field

from aioqiwi.types import BaseModel


class OutgoingTotal(BaseModel):
    """Object: outgoingTotal"""

    amount: float = Field(..., alias="amount")
    currency: str = Field(..., alias="currency")


class IncomingTotal(BaseModel):
    """Object: incomingTotal"""

    amount: float = Field(..., alias="amount")
    currency: str = Field(..., alias="currency")


class Stats(BaseModel):
    """Object: Stats"""

    incoming_total: List[IncomingTotal] = Field(..., alias="incomingTotal")
    outgoing_total: List[OutgoingTotal] = Field(..., alias="outgoingTotal")
