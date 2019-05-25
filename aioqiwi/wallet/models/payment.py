from dataclasses import dataclass

from ...models.base_api_model import BaseModel


@dataclass(init=False)
class Payment(BaseModel):
    id: str
    terms: str

    @dataclass(init=False)
    class Fields(BaseModel):
        account: str

    @dataclass(init=False)
    class Sum(BaseModel):
        amount: float or int
        currency: str

    @dataclass(init=False)
    class Transaction(BaseModel):
        id: str

        @dataclass(init=False)
        class State(BaseModel):
            code: str

    source: str
    comment: str = None


@dataclass(init=True)
class FieldsWidget(BaseModel):
    account: str

    # sender
    rem_name: str
    rem_name_f: str
    rec_address: str
    rec_city: str
    rec_count: str

    # receiver
    reg_name: str
    reg_name_f: str

    __doc__ = """fields 	Object 	Реквизиты платежа. Содержит параметры:
fields.account 	String 	Номер банковской карты получателя
fields.rem_name 	String 	Имя отправителя. Требуется только для ID (идентификатор провайдера в запросе) 1960, 21012
fields.rem_name_f 	String 	Фамилия отправителя. Требуется только для ID (идентификатор провайдера в запросе) 1960, 21012
fields.rec_address 	String 	Адрес отправителя (без почтового индекса, в произвольной форме). Требуется только для ID (идентификатор провайдера в запросе) 1960, 21012
fields.rec_city 	String 	Город отправителя. Требуется только для ID (идентификатор провайдера в запросе) 1960, 21012
fields.rec_country 	String 	Страна отправителя. Требуется только для ID (идентификатор провайдера в запросе) 1960, 21012
fields.reg_name 	String 	Имя получателя. Требуется только для ID (идентификатор провайдера в запросе) 1960, 21012
fields.reg_name_f 	String 	Фамилия получателя. Требуется только для ID (идентификатор провайдера в запросе) 1960, 21012"""
