from __future__ import annotations

import asyncio
import random
from enum import Enum, auto
from typing import Any, Awaitable, Callable, List, Optional, Tuple, TypeVar

from .filter import Filter

E = TypeVar("E")
EventFilter = Callable[[E], bool]
EventHandlerFunctor = Callable[[E], Awaitable[Any]]


class EventProcessStrategy(Enum):
    ORDERED = auto()
    """When processing new event manager will go through all event processors till filters of one them succeeded"""

    MILKSHAKE = auto()
    """When processing new event manager will apply random.shuffle to event handlers.
    No order of execution guaranteed"""


class EventHandler:
    def __init__(self, functor: EventHandlerFunctor, *filter_: Filter):
        self._fn = functor
        self._filters = filter_

    async def check_then_execute(self, event: E):
        for filter_ in self._filters:
            if filter_.awaitable:
                if not await filter_.function(event):
                    break
            else:
                if not filter_.function(event):
                    break
        else:
            return await self._fn(event)


class HandlerManager:
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        event_process_strategy: Optional[EventProcessStrategy] = None,
    ):
        if not isinstance(loop, asyncio.AbstractEventLoop):
            raise ValueError(
                f"Listener must have its event loop implemented with {asyncio.AbstractEventLoop!r}"
            )

        self.loop = loop
        self.process_strategy = EventProcessStrategy(
            event_process_strategy or EventProcessStrategy.ORDERED
        )
        self._event_handlers: List[EventHandler] = []

    def add_event_handler(
        self, event_handler: EventHandlerFunctor, filters: Tuple[Filter, ...]
    ) -> HandlerManager:
        """
        Add new event handler.
        (!) Allows chain addition.
        :param event_handler: event handler, low order function which works with events
        :param filters: filter for low order function execution
        :return: this handler manager
        """
        if filters:  # Initially filters are in tuple
            filters_list = list(filters)

            for index, filter_ in enumerate(filters):
                if not isinstance(filter_, Filter):
                    filters_list[index] = Filter(filter_)

            filters = tuple(filters_list)

        self._event_handlers.append(EventHandler(event_handler, *filters))

        return self

    def __call__(self, *filter_: Filter):
        """
        Listener is callable for registering new event handlers
        :param filter_: Filter objects unpacked
        """

        def decorator(event_handler: EventHandlerFunctor):
            self.add_event_handler(event_handler, filter_)

        return decorator

    async def process_event(self, event: E):
        """
        Feed handlers with event.
        :param event: any object that will be translated to handlers
        """
        if self.process_strategy is EventProcessStrategy.MILKSHAKE:
            random.shuffle(self._event_handlers)

        for handler in self._event_handlers:
            await handler.check_then_execute(event)
