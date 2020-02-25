from ..utils.autoenum import NamedEnum, auto


class BillStatuses(NamedEnum):
    WAITING = auto()
    PAID = auto()
    REJECTED = auto()
    EXPIRED = auto()


class RefundStatuses(NamedEnum):
    PARTIAL = auto()
    FULL = auto()
