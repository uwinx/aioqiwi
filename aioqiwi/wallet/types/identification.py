from typing import Optional

from aioqiwi.types import BaseModel


class Identification(BaseModel):
    id: int
    """Номер кошелька пользователя"""

    birthDate: Optional[str] = None
    """Дата рождения пользователя (в формате "ГГГГ-ММ-ДД")"""

    firstName: Optional[str] = None
    """Имя пользователя"""

    inn: Optional[str] = None
    """ИНН пользователя"""

    lastName: Optional[str] = None
    """Фамилия пользователя"""

    middleName: Optional[str] = None
    """Отчество пользователя"""

    oms: Optional[str] = None
    """Номер полиса ОМС пользователя"""

    passport: Optional[str] = None
    """Серия и номер паспорта пользователя (только цифры)"""

    snils: Optional[str] = None
    """Номер СНИЛС пользователя"""

    type: Optional[str] = None
    """
    Текущий уровень идентификации кошелька:
    SIMPLE - без идентификации.
    VERIFIED - упрощенная идентификация (данные для идентификации успешно прошли проверку).
    FULL – если кошелек уже ранее получал полную идентификацию по данным ФИО, номеру паспорта и дате рождения.
    """
