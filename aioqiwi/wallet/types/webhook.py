"""
Main model: WebHook
"""
from pydantic import Field

from aioqiwi.types import BaseModel


class Total(BaseModel):
    """Object: total"""

    amount: float = Field(..., alias="amount")
    currency: int = Field(..., alias="currency")


class Sum(BaseModel):
    """Object: sum"""

    amount: float = Field(..., alias="amount")
    currency: int = Field(..., alias="currency")


class Commission(BaseModel):
    """Object: commission"""

    amount: float = Field(..., alias="amount")
    currency: int = Field(..., alias="currency")


class Payment(BaseModel):
    """Object: payment"""

    account: str = Field(..., alias="account")
    comment: str = Field(..., alias="comment")
    date: str = Field(..., alias="date")
    error_code: str = Field(..., alias="errorCode")
    person_id: int = Field(..., alias="personId")
    provider: int = Field(..., alias="provider")
    sign_fields: str = Field(..., alias="signFields")
    status: str = Field(..., alias="status")
    txn_id: str = Field(..., alias="txnId")
    type: str = Field(..., alias="type")
    commission: Commission = Field(..., alias="commission")
    sum: Sum = Field(..., alias="sum")
    total: Total = Field(..., alias="total")


class WebHook(BaseModel):
    """Object: WebHook"""

    hash: str = Field(..., alias="hash")
    hook_id: str = Field(..., alias="hookId")
    message_id: str = Field(..., alias="messageId")
    test: bool = Field(..., alias="test")
    version: str = Field(..., alias="version")
    payment: Payment = Field(..., alias="payment")


class HookParameters(BaseModel):
    """Object: hookParameters"""

    url: str = Field(..., alias="url")


class WebHookConfig(BaseModel):
    """Object: WebHookConfig"""

    hook_id: str = Field(..., alias="hookId")
    hook_type: str = Field(..., alias="hookType")
    txn_type: str = Field(..., alias="txnType")
    hook_parameters: HookParameters = Field(..., alias="hookParameters")
