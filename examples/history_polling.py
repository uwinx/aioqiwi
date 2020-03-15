import asyncio
import logging
import datetime

from aioqiwi.contrib import history_polling
from aioqiwi.wallet import Wallet, types

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

loop = asyncio.get_event_loop()
wallet = Wallet(api_hash="...", loop=loop, phone_number="+...")
poller = history_polling.HistoryPoll(
    wallet,
    timeout=10,
    from_date=datetime.datetime.now() - datetime.timedelta(days=30),
    limit=5,
    process_old_to_new=True,
)


@wallet.hm()
async def my_handler(event: types.PaymentData):
    print(event)


async def main():
    async def on_error(exception: asyncio.TimeoutError):
        logger.info(f"... hI {exception!s} Hi ...")
        print("Oops. Just got timeout error. Shall we sleep for a bit?")
        await asyncio.sleep(14.44)

    try:
        await poller.run_polling(
            asyncio.TimeoutError,
            on_exception=on_error,
        )
    finally:
        await wallet.close()

loop.run_until_complete(main())
