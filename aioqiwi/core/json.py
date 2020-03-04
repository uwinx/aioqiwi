import importlib


class JsonModule:
    """
    JsonModule - class for managing json deserializer/serializer module

    It basically has two function attributes: deserialize/serialize

    >>> j = JsonModule("json")
    >>> j.deserialize(b"{'a': 'b'}"); j.serialize({'a': 'b'})
    """

    def __init__(self, module: str = "json"):
        """
        :param module: any importable python module with appropriate loads and dumps functions
                       (for json! deserialization and serialization) in namespace.
        """
        try:
            self.serialize = importlib.import_module(module).dumps  # type: ignore
            self.deserialize = importlib.import_module(module).loads  # type: ignore
        except ImportError:
            raise ImportError(f"{module!s} is not a module or was not yet installed.")
        except AttributeError:
            raise AttributeError(f"{module!s} has no dumps|loads in its namespace")
