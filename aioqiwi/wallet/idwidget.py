from ..models.utils import to_lower_camel_case


class IdentificationWidget:
    """birth_date 	Дата рождения пользователя (в формате “ГГГГ-ММ-ДД”)
    first_name 	Имя пользователя
    middle_name 	Отчество пользователя
    last_name 	Фамилия пользователя
    passport 	Серия и номер паспорта пользователя (только цифры)
    inn 	ИНН пользователя
    snils 	Номер СНИЛС пользователя
    oms 	Номер полиса ОМС пользователя
    """
    birth_date: str
    first_name: str
    inn: str
    last_name: str
    middle_name: str
    oms: str
    passport: str
    snils: str

    def as_dict(self):
        return {
            to_lower_camel_case(k): getattr(self, k)
            for k in vars(self).keys()
            if k[0] != "_"
        }
