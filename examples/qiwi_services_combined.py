import asyncio

from aiohttp.web import Application

from aioqiwi.kassa import QiwiKassa, Notification
from aioqiwi.wallet import Wallet, WebHook, types, enums
from aioqiwi.utils import Currency


loop = asyncio.get_event_loop()
qiwi = Wallet("api_hash from qiwi.com/api", loop=loop)
kassa = QiwiKassa("secret_key from p2p.qiwi.com")


@qiwi.on_update()
async def payment_handler(payment: WebHook):
    print(payment.payment.sum)


@kassa.on_update()
async def kassa_update(bill: Notification):
    print(bill.bill.amount)


async def caren():
    lifetime = 30  # days

    await qiwi.transaction(
        provider_id=enums.Provider.QIWI_WALLET.value,
        payment_type=types.P2PPayment(
            id=None,
            sum=types.payment.Sum(
                amount=100.44,
                currency=Currency["RUB"].isoformat,
            ),
            fields=types.payment.Fields(
                account="!!!receiver's_account!!!"
            ),
            paymentMethod=enums.PaymentMethodConst()
        )
    )

    bill = await kassa.new_bill(
        14.88,
        "7787787787",
        "kevin@kids.com" "com",
        lifetime=lifetime,
        comment="Yes. I took your kids! Pay that bill in a month to see them again :P",
    )

    print(bill.pay_url)


async def show_my_history_by_the_way(rows: int = 1):
    history = await qiwi.history(rows)

    for o in reversed(history.data):
        print(o.type, o.status, o.sum, sep="|")


async def idle(app_: Application):
    await caren()
    await show_my_history_by_the_way(25)
    qiwi.idle(app=app_)


if __name__ == '__main__':
    app = Application()
    kassa.configure_listener(app)
    loop.run_until_complete(idle(app))
