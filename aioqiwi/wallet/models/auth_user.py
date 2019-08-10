from dataclasses import dataclass
from typing import List

from ...models.utils import to_lower_camel_case
from ...models.base_api_model import BaseModel


@dataclass(init=False)
class Feature(BaseModel):
    feature_id: int
    feature_value: str
    start_date: str
    end_date: str


@dataclass(init=False)
class AuthUser(BaseModel):
    @dataclass(init=False)
    class AuthInfo(BaseModel):
        person_id: int
        bound_email: str
        ip: str
        registration_date: str
        last_login_date: str = None

        @dataclass(init=False)
        class EmailSettings(BaseModel):
            use_for_security: str
            use_for_promo: str

        @dataclass(init=False)
        class MobilePinInfo(BaseModel):
            last_mobile_pin_change: str
            mobile_pin_used: bool
            next_mobile_pin_change: str

        @dataclass(init=False)
        class PassInfo(BaseModel):
            last_pass_change: str
            next_pass_change: str
            password_used: bool
            person_id: int

        @dataclass(init=False)
        class PinInfo(BaseModel):
            pin_used: bool
            registration_date: str

    @dataclass(init=False)
    class ContractInfo(BaseModel):
        blocked: bool
        contract_id: int
        creation_date: str
        features: List[Feature]
        identification_info: list

        @dataclass(init=False)
        class Nickname(BaseModel):
            can_change: bool
            can_use: bool
            description: str
            nickname: str = None

        @dataclass(init=False)
        class SmsNotification(BaseModel):
            @dataclass(init=False)
            class Price:
                amount: float
                currency: int

            enabled: bool
            active: bool
            end_date: str

        @dataclass(init=False)
        class PriorityPackage(BaseModel):
            @dataclass(init=False)
            class Price:
                amount: float
                currency: int

            auto_renewal_active: bool
            enabled: bool
            active: bool
            end_date: str

    @dataclass(init=False)
    class UserInfo(BaseModel):
        default_pay_currency: int
        default_pay_source: int
        default_pay_account_alias: str
        email: str
        first_txn_id: int
        language: str
        operator: str
        phone_hash: str
        promo_enabled: bool

        @dataclass(init=False)
        class IntegrationHashes(BaseModel):
            _field_free_aioqiwi_model = True


class Me(BaseModel):
    def __init__(
        self,
        auth_info_enabled: bool = True,
        contact_info_enabled: bool = True,
        user_info_enabled: bool = True,
    ):
        self.auth_info_enabled = auth_info_enabled
        self.contract_info_enabled = contact_info_enabled
        self.user_info_enabled = user_info_enabled

    def as_params(self):
        return {to_lower_camel_case(k): v for k, v in self.dict_params.items()}
