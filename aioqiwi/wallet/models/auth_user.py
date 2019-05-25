from dataclasses import dataclass

from ...models.utils import to_lower_camel_case
from ...models.base_api_model import BaseModel


@dataclass(init=False)
class AuthUser(BaseModel):
    @dataclass(init=False)
    class AuthInfo(BaseModel):
        bound_email: str
        ip: str
        last_login_date: str

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
        features: list
        identification_info: list

    @dataclass(init=False)
    class UserInfo(BaseModel):
        default_pay_currency: int
        default_pay_source: int
        email: str
        first_txn_id: int
        language: str
        operator: str
        phone_hash: str
        promo_enabled: bool


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

    def dict_params(self):
        return {to_lower_camel_case(k): v for k, v in self.dict_params().items()}
