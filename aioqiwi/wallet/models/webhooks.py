from dataclasses import dataclass

from ...models.base_api_model import BaseModel


@dataclass(init=False)
class Hooks(BaseModel):
    hook_id: str

    @dataclass(init=False)
    class HookParameters(BaseModel):
        url: str

    hook_type: str
    txn_type: str
