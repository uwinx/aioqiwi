from aioqiwi.types.base import NamedEnum, name


class BillStatuses(NamedEnum):
    WAITING = name()
    PAID = name()
    REJECTED = name()
    EXPIRED = name()


class RefundStatuses(NamedEnum):
    PARTIAL = name()
    FULL = name()
