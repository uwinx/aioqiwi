"""
Main model: History
"""
from typing import List, Union

from pydantic import Field

from aioqiwi.types import BaseModel

NoneType = type(None)


class Provider(BaseModel):
    """Object: provider"""

    id: int = Field(..., alias="id")
    short_name: str = Field(..., alias="shortName")
    long_name: str = Field(..., alias="longName")
    logo_url: str = Field(..., alias="logoUrl")
    description: str = Field(..., alias="description")
    keys: str = Field(..., alias="keys")
    site_url: Union[str, bool, int, NoneType] = Field(NoneType, alias="siteUrl")


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

    amount: int = Field(..., alias="amount")
    currency: str = Field(..., alias="currency")


class Data(BaseModel):
    """Object: data"""

    txn_id: int = Field(..., alias="txnId")
    person_id: int = Field(..., alias="personId")
    date: str = Field(..., alias="date")
    error_code: int = Field(..., alias="errorCode")
    error: Union[str, bool, int, NoneType] = Field(NoneType, alias="error")
    status: str = Field(..., alias="status")
    type: str = Field(..., alias="type")
    status_text: str = Field(..., alias="statusText")
    trm_txn_id: str = Field(..., alias="trmTxnId")
    account: str = Field(..., alias="account")
    comment: Union[str, bool, int, NoneType] = Field(NoneType, alias="comment")
    currency_rate: int = Field(..., alias="currencyRate")
    extras: Union[str, bool, int, NoneType] = Field(NoneType, alias="extras")
    cheque_ready: bool = Field(..., alias="chequeReady")
    bank_document_available: bool = Field(..., alias="bankDocumentAvailable")
    bank_document_ready: bool = Field(..., alias="bankDocumentReady")
    repeat_payment_enabled: bool = Field(..., alias="repeatPaymentEnabled")
    sum: Sum = Field(..., alias="sum")
    commission: Commission = Field(..., alias="commission")
    total: Total = Field(..., alias="total")
    provider: Provider = Field(..., alias="provider")


class History(BaseModel):
    """Object: History"""

    data: List[Data] = Field(..., alias="data")
    next_txn_id: int = Field(..., alias="nextTxnId")
    next_txn_date: str = Field(..., alias="nextTxnDate")
