"""Main model: Notification"""
from typing import Any, Dict, Optional

from pydantic import Field

from aioqiwi.types import BaseModel


class Customer(BaseModel):
    """Object: customer"""

    phone: Optional[str] = None
    account: Optional[str] = None
    email: Optional[str] = None


class Status(BaseModel):
    """Object: status"""

    value: str = Field(..., alias="value")
    datetime: str = Field(..., alias="datetime")


class Amount(BaseModel):
    """Object: amount"""

    value: str = Field(..., alias="value")
    currency: str = Field(..., alias="currency")


class Bill(BaseModel):
    """Object: bill"""

    site_id: str = Field(..., alias="siteId")
    bill_id: str = Field(..., alias="billId")
    creation_date_time: str = Field(..., alias="creationDateTime")
    expiration_date_time: str = Field(..., alias="expirationDateTime")
    amount: Amount = Field(..., alias="amount")
    status: Status = Field(..., alias="status")
    customer: Customer = Field(type(None), alias="customer")
    custom_fields: Optional[Dict[str, Any]] = Field(type(None), alias="customFields")


class Notification(BaseModel):
    """Object: Notification"""

    version: str = Field(..., alias="version")
    bill: Bill = Field(..., alias="bill")


__all__ = ("Notification",)
