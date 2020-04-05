from typing import Optional, Callable, Dict, Any, AnyStr, Union, List
from types import ModuleType

import importlib

JSON = Optional[Union[Dict[str, Any], List[Any]]]


class JsonModule:
    """
    JsonModule - class for managing json deserializer/serializer module

    It basically has two function attributes: deserialize/serialize

    >>> j = JsonModule("json")
    >>> j.deserialize(b"{'a': 'b'}"); j.serialize({'a': 'b'})
    """
    imported: ModuleType

    deserialize: Callable[[AnyStr], JSON]
    serialize: Callable[[JSON], AnyStr]

    def __init__(self, module: str = "json"):
        """
        :param module: any importable python module with appropriate loads and dumps functions
                       (for json! deserialization and serialization) in namespace.
        """
        try:
            self.imported = imported = importlib.import_module(module)
            self.serialize = imported.dumps  # type: ignore
            self.deserialize = imported.loads  # type: ignore
        except ImportError:
            raise ImportError(f"{module!s} is not a module or was not yet installed.")
        except AttributeError:
            raise AttributeError(f"{module!s} has no dumps|loads in its namespace")
