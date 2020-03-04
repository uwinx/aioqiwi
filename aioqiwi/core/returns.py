from enum import Enum, auto


class ReturnType(Enum):
    """
    4 Return policies.

    READ_DATA - raw return once stream is read

    JSON - raw return once read data was deserialized

    MODEL - complex return once json deserialized and new model instantiated

    LIST_OF_MODELS - complex return once json deserialized as an iterable list with new instantiated models
                                                                                            of json objects
    """

    READ_DATA = auto()
    """raw return once stream is read"""

    JSON = auto()
    """raw return once read data was deserialized"""

    MODEL = auto()
    """complex return once json deserialized and new model instantiated"""

    LIST_OF_MODELS = auto()
    """complex return once json deserialized as an iterable list with new instantiated models of json objects"""
