"""
Before running install aiogram, cool telegram bot-api wrapper
    ::

        pip install aiogram

"""
from aiogram import Bot

from aioqiwi.utils import BeautifulSum
from aioqiwi.wallet import Wallet, QiwiUpdate, filters

ME = 124191486  # your telegram user id

qiwi = Wallet("MyQiwiToken")
bot = Bot("MyBotToken")

# different variations that can do the same        # ---------------------
filters.equal("Payment.comment", "xyz")  # for cons             |
filters.PaymentComment == "xyz"  # more elegant         |
filters.PaymentComment.match(r"^xyz+$")  # scalable             |
filters.in_sequence("Payment.comment", ["xyz"])  # also kinda scalable  |


# we'll use elegant one or choose one from below
@qiwi.on_update(filters.PaymentComment == "xyz")
async def special_payments_handler(event: QiwiUpdate):
    payment = event.Payment
    text = f":D Woop-woop! {payment.account} sent you {BeautifulSum(payment.Sum).humanize}\n"

    await bot.send_message(chat_id=ME, text=text)


async def on_startup():
    # change hooks if yyo want
    # info = await qiwi.new_hooks("http://myNewWebHooksUrl.com", 2)
    info = await qiwi.hooks()

    await bot.send_message(
        chat_id=ME,
        text=f"Bot is starting\nQiwi will send hooks to {info.HookParameters.url}",
    )


# I recommend using reverse-proxies
# like nginx running .py locally for convenience
qiwi.idle(on_startup=on_startup(), port=5577)
