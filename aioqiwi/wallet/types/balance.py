"""
Main model: Balance
"""
from typing import List, Optional

from pydantic import Field

from aioqiwi.types import BaseModel


class AccountBalance(BaseModel):
    """Object: balance"""

    amount: float = Field(..., alias="amount")
    currency: int = Field(..., alias="currency")


class Type(BaseModel):
    """Object: type"""

    id: str = Field(..., alias="id")
    title: str = Field(..., alias="title")


class Accounts(BaseModel):
    """Object: accounts"""

    alias: str = Field(..., alias="alias")
    fs_alias: str = Field(..., alias="fsAlias")
    title: str = Field(..., alias="title")
    has_balance: bool = Field(..., alias="hasBalance")
    currency: int = Field(..., alias="currency")
    type: Type = Field(..., alias="type")
    balance: Optional[AccountBalance] = None


class Balance(BaseModel):
    """Object: Balance"""

    accounts: List[Accounts] = Field(..., alias="accounts")
