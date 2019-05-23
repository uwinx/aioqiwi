from enum import Enum


class BillStatuses(Enum):
    WAITING = 'WAITING'
    PAID = 'PAID'
    REJECTED = 'REJECTED'
    EXPIRED = 'EXPIRED'


class RefundStatuses(Enum):
    PARTIAL = 'PARTIAL'
    FULL = 'FULL'
