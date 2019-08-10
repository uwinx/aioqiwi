# todo implement filters stack for common filters

import typing
import re

from ..models.base_api_model import BaseModel

CallableFilter = typing.Callable[[typing.Any], bool]
redundant_repr_chars_table = {ord(i): None for i in "\"'>"}


# private region
def __base_field_chain(update):
    return hasattr(update, "Payment") and update.Payment is not None


def _rec_getattr(obj, attr_path, default=None):
    """
    Usage:
    >>> class A:
    ...     class B:
    ...         class C:
    ...             abc = "abc"
    ...
    >>> assert _rec_getattr(A, "B.C.abc") == "abc"
    """
    try:
        main, child = attr_path.split('.', maxsplit=1)
    except ValueError:
        return getattr(obj, attr_path, default)
    return _rec_getattr(getattr(obj, child), main, default)


def _rec_hasattr(obj, attr_path) -> bool:
    """
    Usage:
    >>> class X:
    ...     class Y:
    ...         class Z:
    ...             xyz = "xyz"
    ...
    >>> _rec_hasattr(X, "Y.Z.xyz")
    :return:
    :type: bool
    """
    try:
        main, child = attr_path.split(".", maxsplit=1)
    except ValueError:
        return hasattr(obj, attr_path)
    return _rec_hasattr(getattr(obj, child), main)


def _ensure_field(field: typing.Union[str, BaseModel]):
    if isinstance(field, BaseModel):
        *_, field = str(field).translate(redundant_repr_chars_table).split(".", 2)

    return field


# public region
def equal(field: typing.Union[str, BaseModel], value: typing.Any) -> CallableFilter:
    """
    Check values equality
    :param field: update.{FIELD} can be X.Y.Z
    :param value: value to compare with
    :return callable(update)
    """
    field = _ensure_field(field)

    return lambda update: _rec_getattr(update, field) == value


def in_sequence(
    field: typing.Union[str, BaseModel], sequence: typing.Any
) -> CallableFilter:
    """
    Check if fields value in sequence
    :param field: update.{FIELD} can be X.Y.Z
    :param sequence: sequence of values that contains(or does not) field.(value)
    :return callable(update)
    """
    field = _ensure_field(field)

    return lambda update: _rec_getattr(update, field) in sequence


def startswith(field: typing.Union[str, BaseModel], prefix: str) -> CallableFilter:
    _field = _ensure_field(field)

    def _startswith(update):
        value = _rec_getattr(update, _field)
        if not isinstance(value, str):
            raise UserWarning(
                f"{field} expected to be type str got {type(value).__name__}"
            )

        return value.startswith(prefix)

    return _startswith


class PaymentComment:
    @classmethod
    def startswith(cls, prefix: str) -> CallableFilter:
        return lambda update: __base_field_chain(update) and (
            update.Payment.comment or ""
        ).startswith(prefix)

    @classmethod
    def match(cls, expression: str) -> CallableFilter:
        return lambda update: __base_field_chain(update) and re.compile(
            expression
        ).match(update.Payment.comment)

    @classmethod
    def __eq__(cls, comment: str) -> CallableFilter:
        return equal(field="Payment.comment", value=comment)


class PaymentAmount:
    @classmethod
    def __eq__(cls, amount: int) -> CallableFilter:
        return equal(field="Payment.amount", value=amount)


__all__ = ["PaymentComment", "PaymentAmount", "CallableFilter", "equal", "in_sequence"]
