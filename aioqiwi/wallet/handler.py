import asyncio
import re


class Handler:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.loop = loop or asyncio.get_event_loop()
        self._handlers = []  # [(callback, *funcs, **kwarg-filters)]

    def payment_event(
        self, *func_filters, comment_regex=None, incoming=None, outgoing=None, **kwargs
    ):
        filters = func_filters
        txn_types = ["IN", "OUT"]

        if incoming and not outgoing or not outgoing and incoming is None:
            txn_types.remove("OUT")

        elif outgoing and not incoming or not incoming and outgoing is None:
            txn_types.remove("IN")

        elif all(not x and x is not None for x in (outgoing, incoming)):
            raise ValueError(f"Why the fuck do you need this handler")

        def decorator(event_handler):
            ffilters = list(filters)

            if isinstance(comment_regex, str):
                ffilters.append(
                    lambda update: re.compile(comment_regex).match(
                        update.payment.comment
                    )
                )

            if txn_types:
                ffilters.append(lambda update: update.payment.type in txn_types)

            self._handlers.append((event_handler, ffilters, kwargs))

        return decorator
