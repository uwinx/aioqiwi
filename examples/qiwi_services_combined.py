from aiohttp.web import Application

from aioqiwi.kassa import QiwiKassa, BillUpdate
from aioqiwi.wallet import Wallet, QiwiUpdate
from aioqiwi.utils import BeautifulSum


qiwi = Wallet("api_hash from qiwi.com/api")
kassa = QiwiKassa("secret_key from p2p.qiwi.com")


@qiwi.on_update()
async def payment_handler(payment: QiwiUpdate):
    print(BeautifulSum(payment.Payment.Sum).pretty)


@kassa.on_update()
async def kassa_update(bill: BillUpdate):
    print(BeautifulSum(bill.Bill.Amount).pretty)


async def caren():
    lifetime = 30  # days

    await qiwi.transaction(14.88, "alex@morti.ttl")

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

    for o in history.reversed:  # .reverse is reversed(history.data)
        print(o.type, o.status, BeautifulSum(o.Sum).pretty, sep="|")


async def before_idle():
    await caren()
    await show_my_history_by_the_way(25)


app = Application()
kassa.configure_listener(app)
qiwi.idle(on_startup=before_idle(), app=app)
