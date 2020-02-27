"""Main model: Invoice"""
from typing import Any, Dict, Optional

from pydantic import Field

from aioqiwi.types import BaseModel


class Customer(BaseModel):
    """Object: customer"""

    email: str = Field(..., alias="email")
    phone: str = Field(..., alias="phone")
    account: str = Field(..., alias="account")


class Status(BaseModel):
    """Object: status"""

    value: str = Field(..., alias="value")
    datetime: str = Field(..., alias="datetime")


class Amount(BaseModel):
    """Object: amount"""

    value: float = Field(..., alias="value")
    currency: str = Field(..., alias="currency")


class Invoice(BaseModel):
    """Object: Invoice"""

    site_id: str = Field(..., alias="siteId")
    bill_id: str = Field(..., alias="billId")
    comment: str = Field(..., alias="comment")
    creation_date_time: str = Field(..., alias="creationDateTime")
    expiration_date_time: str = Field(..., alias="expirationDateTime")
    pay_url: str = Field(..., alias="payUrl")
    amount: Amount = Field(..., alias="amount")
    status: Status = Field(..., alias="status")
    customer: Customer = Field(..., alias="customer")
    custom_fields: Optional[Dict[str, Any]] = Field(type(None), alias="customFields")


__all__ = ("Invoice",)
