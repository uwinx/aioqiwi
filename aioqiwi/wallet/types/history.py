"""
Main model: History
"""
from typing import Any, List, Optional, Union

from pydantic import Field

from aioqiwi.types import BaseModel


class Provider(BaseModel):
    """Object: provider"""

    id: int = Field(..., alias="id")
    short_name: str = Field(..., alias="shortName")
    long_name: Optional[str] = Field(None, alias="longName")
    logo_url: Optional[str] = Field(None, alias="logoUrl")
    description: Optional[str] = Field(None, alias="description")
    keys: Optional[str] = Field(None, alias="keys")
    site_url: Optional[Any] = Field(None, alias="siteUrl")


class Total(BaseModel):
    """Object: total"""

    amount: int = Field(..., alias="amount")
    currency: str = Field(..., alias="currency")


class Commission(BaseModel):
    """Object: commission"""

    amount: int = Field(..., alias="amount")
    currency: str = Field(..., alias="currency")


class Sum(BaseModel):
    """Object: sum"""

    amount: float = Field(..., alias="amount")
    currency: str = Field(..., alias="currency")


class PaymentData(BaseModel):
    """Object: data"""

    txn_id: int = Field(..., alias="txnId")
    person_id: int = Field(..., alias="personId")
    date: str = Field(..., alias="date")
    error_code: int = Field(..., alias="errorCode")
    error: Optional[Any] = Field(None, alias="error")
    status: str = Field(..., alias="status")
    type: str = Field(..., alias="type")
    status_text: str = Field(..., alias="statusText")
    trm_txn_id: str = Field(..., alias="trmTxnId")
    account: str = Field(..., alias="account")
    comment: Optional[Any] = Field(None, alias="comment")
    currency_rate: int = Field(..., alias="currencyRate")
    extras: Optional[Any] = Field(None, alias="extras")
    cheque_ready: Optional[bool] = Field(None, alias="chequeReady")
    bank_document_available: Optional[bool] = Field(None, alias="bankDocumentAvailable")
    bank_document_ready: Optional[bool] = Field(None, alias="bankDocumentReady")
    repeat_payment_enabled: Optional[bool] = Field(None, alias="repeatPaymentEnabled")
    sum: Sum = Field(..., alias="sum")
    commission: Commission = Field(..., alias="commission")
    total: Total = Field(..., alias="total")
    provider: Provider = Field(..., alias="provider")


class History(BaseModel):
    """Object: History"""

    data: List[PaymentData] = Field(..., alias="data")
    next_txn_id: Optional[int] = Field(None, alias="nextTxnId")
    next_txn_date: Optional[str] = Field(None, alias="nextTxnDate")
