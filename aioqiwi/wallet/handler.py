import asyncio
import re


class Handler:
    """
    Handler class entry point
    """

    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.loop = loop or asyncio.get_event_loop()
        self.handlers = []  # [(callback, *funcs, **kwarg-filters)]

    def payment_event(self, *func_filters, comment_regex=None, incoming=None, outgoing=None, **kwargs):
        """
        Payments handler
        :param func_filters: pass your one-argument function, that argument is QiwiUpdate
        :param comment_regex: filter commentary by regex
        :param incoming: set filter to incoming payments
        :param outgoing: set filter to outgoing payments
        :param kwargs: QiwiUpdate attribute equality
        """
        filters = func_filters
        txn_types = ["IN", "OUT"]

        if incoming and not outgoing or not outgoing and incoming is None:
            txn_types.remove("OUT")

        elif outgoing and not incoming or not incoming and outgoing is None:
            txn_types.remove("IN")

        elif all(not x and x is not None for x in (outgoing, incoming)):
            raise ValueError(
                f"Why do you need this handler? Nothing will be catched to this."
            )

        def decorator(event_handler):
            ffilters = list(filters)

            if isinstance(comment_regex, str):
                ffilters.append(
                    lambda update: re.compile(comment_regex).match(
                        update.payment.comment
                    )
                )

            if txn_types:
                ffilters.append(lambda update: update.Payment.type in txn_types)

            self.handlers.append((event_handler, ffilters, kwargs))

        return decorator

    @property
    def registered_handlers(self):
        """
        User-friendly representation of registered handlers
        :return:
        """
        return [
            f'{"".join(func.__name__ for func in filters)}(where {", ".join(f"{k}={v}" for k, v in kfilter.items())})'
            f"->will execute callback: <{callback.__name__}>"
            for callback, filters, kfilter in self.handlers
        ]
