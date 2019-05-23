import asyncio


class Handler:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.loop = loop or asyncio.get_event_loop()
        self._handlers = []  # [(callback, *funcs, **kwarg-filters)]

    def update(
        self, *func_filters, **kwargs
    ):
        filters = func_filters

        def decorator(event_handler):
            self._handlers.append((event_handler, filters, kwargs))

        return decorator