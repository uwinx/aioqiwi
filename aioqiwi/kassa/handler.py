import asyncio


class Handler:
    """
    Kassa handler same implementation as in payments.handler
    """

    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.loop = loop or asyncio.get_event_loop()
        self.handlers = []  # [(callback, *funcs, **kwarg-filters)]

    def update(self, *func_filters, **kwargs):
        filters = func_filters

        def decorator(event_handler):
            self._handlers.append((event_handler, filters, kwargs))

        return decorator

    @property
    def registered_handlers(self):
        return [
            f'{filters}(where {"".join(f"{k}={v}" for k, v in kfilter.items())})->will execute callback: <{callback.__name__}>'
            for callback, filters, kfilter in self.handlers
        ]
