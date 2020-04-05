"""
Main model: Payment
"""
from typing import Generic, Optional, TypeVar, Union

from pydantic import Field

from aioqiwi.types import BaseModel

P = TypeVar("P")


class State(BaseModel):
    """Object: state"""

    code: str = Field(..., alias="code")


class Transaction(BaseModel):
    """Object: transaction"""

    id: str = Field(..., alias="id")
    state: State = Field(..., alias="state")


class Sum(BaseModel):
    """Object: sum"""

    amount: float = Field(..., alias="amount")
    currency: str = Field(..., alias="currency")


class PaymentMethod(BaseModel):
    """Object: paymentMethod"""

    type: str = Field(..., alias="type")
    account_id: str = Field(..., alias="accountId")


# ===================
# FIELDS REGION START
# ===================
class Fields(BaseModel):
    """Object: fields"""

    account: str = Field(..., alias="account")


class CardFields(BaseModel):
    """Object: fields"""

    account: str = Field(..., alias="account")
    rec_address: str = Field(..., alias="rec_address")
    rec_city: str = Field(..., alias="rec_city")
    rec_country: str = Field(..., alias="rec_country")
    reg_name: str = Field(..., alias="reg_name")
    reg_name_f: str = Field(..., alias="reg_name_f")
    rem_name: str = Field(..., alias="rem_name")
    rem_name_f: str = Field(..., alias="rem_name_f")


class BankFields(BaseModel):
    """Object: fields"""

    account_type: str = Field(..., alias="account_type")
    urgent: str = Field(..., alias="urgent")
    lname: str = Field(..., alias="lname")
    fname: str = Field(..., alias="fname")
    mname: str = Field(..., alias="mname")
    mfo: str = Field(..., alias="mfo")
    account: str = Field(..., alias="account")


# =================
# FIELDS REGION END
# =================


class P2PPayment(BaseModel):
    """Object: P2PPayment"""

    id: Optional[str] = Field(None, alias="id")
    sum: Sum = Field(..., alias="sum")
    payment_method: PaymentMethod = Field(..., alias="paymentMethod")
    comment: Optional[str] = Field(None, alias="comment")
    payment_fields: Fields = Field(..., alias="fields")


class CellTopUp(P2PPayment):
    """Object: CellTopUp"""


class CardPayment(BaseModel):
    """Object: CardPayment"""

    id: Optional[str] = Field(type(None), alias="id")
    sum: Sum = Field(..., alias="sum")
    payment_method: PaymentMethod = Field(..., alias="paymentMethod")
    comment: Optional[str] = Field(None, alias="comment")
    payment_fields: CardFields = Field(..., alias="fields")


class BankPayment(BaseModel):
    """Object: BankPayment"""

    id: Optional[str] = Field(type(None), alias="id")
    sum: Sum = Field(..., alias="sum")
    payment_method: PaymentMethod = Field(..., alias="paymentMethod")
    comment: Optional[str] = Field(None, alias="comment")
    payment_fields: BankFields = Field(..., alias="fields")


class Payment(BaseModel):
    """Object: P2PPayment"""

    id: str = Field(..., alias="id")
    source: str = Field(..., alias="source")
    payment_fields: Union[Fields, CardFields, BankFields] = Field(..., alias="fields")
    sum: Sum = Field(..., alias="sum")
    transaction: Transaction = Field(..., alias="transaction")
