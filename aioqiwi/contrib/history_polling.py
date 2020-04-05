import asyncio
import datetime
import logging
from typing import Awaitable, Callable, ClassVar, Optional, Type, TypeVar, Union

from aioqiwi.core.returns import ReturnType
from aioqiwi.core.tooling.datetime import DatetimeModule
from aioqiwi.wallet import Wallet, enums

EX = TypeVar("EX", bound=BaseException)  # continue Exception type

# defaults
DEFAULT_LIMIT = 50
DEFAULT_TIMEOUT = 0.5

logger = logging.getLogger(__name__)


class StopPolling(Exception):
    pass


class ContinuePolling(Exception):
    pass


class HistoryPoll:
    """
    This implementation assumes:
    1. Wallet is using MODEL return policy
    2. QIWI-API transactions are ordered from new -> old in history.data list
    """

    datetime_module: ClassVar[DatetimeModule] = DatetimeModule()

    def __init__(
        self,
        client: Wallet,
        from_date: Union[str, datetime.datetime] = datetime.datetime.now(),
        timeout: float = DEFAULT_TIMEOUT,
        limit: int = DEFAULT_LIMIT,
        process_old_to_new: bool = True,
    ):
        if client.tools.return_type is not ReturnType.MODEL:
            raise ValueError("Wallet::return_type must be `MODEL` for history polling")

        self._client = client

        self.timeout = timeout
        self.limit_per_request = limit

        self.payment_sources = [
            enums.PaymentSources.CARD,
            enums.PaymentSources.MK,
            enums.PaymentSources.QW_EUR,
            enums.PaymentSources.QW_RUB,
            enums.PaymentSources.QW_USD,
        ]
        self.payment_type = enums.PaymentTypes.ALL
        self.process_old_to_new = process_old_to_new

        self._last_txn_id: Optional[int] = None

        if isinstance(from_date, str):
            self._left_date = self.datetime_module.parse_date_string(from_date)
        elif isinstance(from_date, datetime.datetime):
            self._left_date = from_date
        else:
            raise TypeError(
                "`from_date` argument should be either `datetime.datetime` or `str` instance"
            )
        self._right_date: Optional[datetime.datetime] = None  # initializes in poll

        logger.debug(
            f"Initial date range: from {self._left_date!s} till {self._right_date!s}"
        )

    async def poll(self):
        self._right_date = datetime.datetime.now()

        history = await self._client.history(
            self.limit_per_request,
            operation=self.payment_type,
            sources=self.payment_sources,
            date_range=(self._left_date, self._right_date),
        )

        last_payment = history.data[0]
        last_txn_id = last_payment.txn_id

        if self._last_txn_id is None:
            first_payment = history.data[-1]
            self._last_txn_id = first_payment.txn_id

        elif self._last_txn_id == last_txn_id:
            logger.debug("No new transaction found")
            return

        if self.process_old_to_new is True:
            history.data.reverse()  # reverse to (older -> newer)

        history_iterator = iter(history.data)

        while self._last_txn_id < last_txn_id:
            try:
                payment = next(history_iterator)
                logger.debug(f"Processing {payment.txn_id} from {payment.date}")
                await self._client.handler_manager.process_event(payment)
            except StopIteration:  # handle exhausted iterator
                break

            self._last_txn_id = payment.txn_id
            self._left_date = self.datetime_module.parse_date_string(payment.date)

    async def run_polling(
        self,
        *exceptions: Type[EX],
        on_exception: Optional[Callable[[EX], Awaitable[None]]] = None,
    ):
        if self._client.handler_manager is None:
            raise ValueError("Wallet has to have handler manager")

        while True:
            try:
                await self.poll()
                logger.debug(f"Going to sleep {self.timeout} after polling")
                await asyncio.sleep(self.timeout)

            except exceptions as exc:
                if on_exception is not None:
                    await on_exception(exc)
