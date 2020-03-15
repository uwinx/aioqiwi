from typing import Optional, Dict, Type, TypeVar

from pydantic import ValidationError

from aioqiwi.types import BaseModel


class BaseErrorModel(BaseModel):
    @property
    def error_message(self) -> str:
        return "..."


E = TypeVar("E", bound=BaseErrorModel)


class AioqiwiError(Exception):
    """
    Base exception for all exceptions produced by library.
    """
    raw_err: Optional[Dict[str, Optional[str]]] = None
    err: Optional[E] = None

    @classmethod
    def with_error_model(cls, m: Type[E], err: Dict[str, Optional[str]]):
        msg = err
        prep_err = None

        if m is not None:
            try:
                prep_err = m(**err)
                msg = prep_err.error_message
            except ValidationError:
                pass

        exc = cls(msg)
        exc.raw_err = err
        exc.err = prep_err
        raise cls(msg)


class ReadDataProcessError(AioqiwiError):
    """
    Error while reading data from aiohttp response
    """


class JSONDeserializeError(AioqiwiError):
    """
    Error while deserialization of JSON response
    """


class ModelValidationError(AioqiwiError):
    """
    Error while validating model's scheme
    """
