from dataclasses import dataclass

from ...models.base_api_model import BaseModel


@dataclass(init=False)
class Provider(BaseModel):
    @dataclass(init=False)
    class Code:
        value: str
        _name = str

    message: str
    data: str = None
    messages = None
