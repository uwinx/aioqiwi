from aiohttp.web import Application

from aioqiwi.kassa import QiwiKassa, BillUpdate
from aioqiwi.wallet import QiwiAccount, QiwiUpdate
from aioqiwi.utils import BeautifulSum, TimeRange


qiwi = QiwiAccount("api_hash from qiwi.com/api")
kassa = QiwiKassa("secret_key from p2p.qiwi.com")
app = Application()


@qiwi.on.payment_event()
async def payment_handler(payment: QiwiUpdate):
    print(BeautifulSum(payment.Payment.Sum).pretty)


@kassa.on_update()
async def kassa_update(bill: BillUpdate):
    print(BeautifulSum(bill.Bill.Amount).pretty)


async def caren():
    lifetime = TimeRange(30)

    bill = await kassa.new_bill(
        14.88,
        "7787787787",
        "kevin@kids.com",
        lifetime=lifetime,
        comment="Yes. I took your kids! Pay that bill in a month to see them again :P",
    )

    print(bill.pay_url)


async def show_my_history_by_the_way(rows: int = 1):
    month_ago = TimeRange(-30)

    history = await qiwi.history(rows, timerange=month_ago)

    for o in history.reversed:  # .reverse is reversed(history.data)
        print(o.type, o.status, BeautifulSum(o.Sum).pretty, sep="|")


# coroutines and functions passed as a first arguments in lists will be executed in the background and forgotten
kassa.configure_listener(app)
qiwi.idle([caren], [show_my_history_by_the_way, 25], app=app)
