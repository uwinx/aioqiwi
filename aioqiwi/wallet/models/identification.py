from dataclasses import dataclass

from ...models.base_api_model import BaseModel


@dataclass(init=False)
class Identification(BaseModel):
    id: int
    birth_date: str
    first_name: str
    inn: str
    last_name: str
    middle_name: str
    oms: str
    passport: str
    snils: str
    type: str

    def __repr__(self):
        return (
            f"{self.first_name} {self.last_name}({self.middle_name})"
            f"\n|PASS: {self.passport}\n|BIRTH-DATE: {self.birth_date}"
            f"\n|SNILS: {self.snils}\n|INN: {self.inn}"
        )
