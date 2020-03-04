class AioqiwiError(Exception):
    """
    Base exception for all exceptions produced by library.
    """


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
