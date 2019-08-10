import typing
import asyncio

from .filters import CallableFilter

EventHandler = typing.Type[typing.Callable[[typing.Any], typing.Awaitable[typing.Any]]]


class Handler:
    """
    Handler class entry point
    """

    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.loop = loop or asyncio.get_event_loop()
        self.handlers: typing.List[
            typing.Tuple[EventHandler, typing.Sequence[CallableFilter]]
        ] = list()

    def payment_event(self, *filters: CallableFilter):
        def decorator(event_handler: EventHandler):
            self.handlers.append((event_handler, filters))

        return decorator
