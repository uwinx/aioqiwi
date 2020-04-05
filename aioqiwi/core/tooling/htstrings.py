"""experimental"""
from typing import ClassVar

_SC = "{-]"


class HeadTailString(str):
    """
    HeadTailString helper string inheriting type.

    __head__ default head
    __tail__ default tail
    __skip_constraint__ passed as an argument sets this argument to its default.

    NOTE: __skip__constraint__ must never be changed, any change is ignored.

    cls.__skip_constraint__ as an argument sets this argument to its default.
    by default, arguments are cls.__skip_constraint__
    """

    __head__: ClassVar[str] = ""
    __tail__: ClassVar[str] = ""
    __skip_constraint__: ClassVar[str] = _SC

    def __new__(cls, tail: str = _SC, head: str = _SC):
        if tail is None or tail == _SC:
            tail = cls.__tail__

        if head is None or head == _SC:
            head = cls.__head__

        return str.__new__(cls, head + tail)
