"""
Main model: AuthUser
"""
from typing import Any, List, Optional, Union

from pydantic import Field

from aioqiwi.types import BaseModel


class UserInfo(BaseModel):
    """Object: userInfo"""

    default_pay_currency: int = Field(..., alias="defaultPayCurrency")
    default_pay_source: int = Field(..., alias="defaultPaySource")
    email: Optional[Any] = Field(None, alias="email")
    first_txn_id: int = Field(..., alias="firstTxnId")
    language: str = Field(..., alias="language")
    operator: str = Field(..., alias="operator")
    phone_hash: str = Field(..., alias="phoneHash")
    promo_enabled: Optional[Any] = Field(None, alias="promoEnabled")


class IdentificationInfo(BaseModel):
    """Object: identificationInfo"""

    bank_alias: str = Field(..., alias="bankAlias")
    identification_level: str = Field(..., alias="identificationLevel")


class ContractInfo(BaseModel):
    """Object: contractInfo"""

    blocked: bool = Field(..., alias="blocked")
    contract_id: int = Field(..., alias="contractId")
    creation_date: str = Field(..., alias="creationDate")
    features: List[Any] = Field(..., alias="features")
    identification_info: List[IdentificationInfo] = Field(
        ..., alias="identificationInfo"
    )


class PinInfo(BaseModel):
    """Object: pinInfo"""

    pin_used: bool = Field(..., alias="pinUsed")


class PassInfo(BaseModel):
    """Object: passInfo"""

    last_pass_change: str = Field(..., alias="lastPassChange")
    next_pass_change: str = Field(..., alias="nextPassChange")
    password_used: bool = Field(..., alias="passwordUsed")


class MobilePinInfo(BaseModel):
    """Object: mobilePinInfo"""

    last_mobile_pin_change: str = Field(..., alias="lastMobilePinChange")
    mobile_pin_used: bool = Field(..., alias="mobilePinUsed")
    next_mobile_pin_change: str = Field(..., alias="nextMobilePinChange")


class AuthInfo(BaseModel):
    """Object: authInfo"""

    bound_email: Optional[str] = Field(None, alias="boundEmail")
    ip: Optional[str] = Field(None, alias="ip")
    last_login_date: Optional[str] = Field(None, alias="lastLoginDate")
    person_id: int = Field(..., alias="personId")
    registration_date: str = Field(..., alias="registrationDate")
    mobile_pin_info: MobilePinInfo = Field(..., alias="mobilePinInfo")
    pass_info: PassInfo = Field(..., alias="passInfo")
    pin_info: PinInfo = Field(..., alias="pinInfo")


class AuthUser(BaseModel):
    """Object: AuthUser"""

    auth_info: AuthInfo = Field(..., alias="authInfo")
    contract_info: ContractInfo = Field(..., alias="contractInfo")
    user_info: UserInfo = Field(..., alias="userInfo")
