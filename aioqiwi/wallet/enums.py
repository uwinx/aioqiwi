"""
aioqiwi.wallet enums, constants and constraints
"""

from aioqiwi.types import NamedEnum, name

from .types.payment import PaymentMethod as _PaymentMethod


PaymentMethodConst = _PaymentMethod(
    type="Account",
    accountId="643"
)


class PaymentTypes(NamedEnum):
    IN = name()
    OUT = name()
    QIWI_CARD = name()
    ALL = name()


class PaymentSources(NamedEnum):
    QW_RUB = name()
    QW_USD = name()
    QW_EUR = name()
    CARD = name()
    MK = name()


class Provider:
    """
    99 - Перевод на QIWI Wallet

    1963 - Перевод на карту Visa (карты российских банков)
    21013 - Перевод на карту MasterCard (карты российских банков)
    Для карт, выпущенных банками стран Азербайджан, Армения, Белоруссия, Грузия, Казахстан, Киргизия, Молдавия,
    Таджикистан, Туркменистан, Украина, Узбекистан:
        1960 – Перевод на карту Visa
        21012 – Перевод на карту MasterCard

    31652 - Перевод на карту национальной платежной системы МИР
    466 - Тинькофф Банк
    464 - Альфа-Банк
    821 - Промсвязьбанк
    815 - Русский Стандарт
    Идентификаторы операторов мобильной связи
    Идентификаторы других провайдеров
    1717 - платеж по банковским реквизитам"""

    QIWI_WALLET = 99

    VISA_RU = 1963
    VISA_FOREIGN = 1960

    MASTERCARD_RU = 21013
    MASTERCARD_FOREIGN = 21012

    MIR_CARD = 31652

    TINKOFF_BANK = 466
    ALPHA_BANK = 464
    PROSVYAZ_BANK = 821
    RUSSKIY_STANDART = 815

    CUSTOM = 1717


class ChequeTypes(NamedEnum):
    """
    Check [Cheque]'s output type
    """

    JPEG = name()
    PDF = name()
