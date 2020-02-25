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


@qiwi.on_update(filters.PaymentComment == "xyz")
async def special_payments_handler(event: QiwiUpdate):
    payment = event.Payment
    text = f":D Woop-woop! {payment.account} sent you {BeautifulSum(payment.Sum).humanize}\n"

    await bot.send_message(chat_id=ME, text=text)


async def on_startup():
    # change hooks if you want
    # info = await qiwi.new_hooks("http://myNewWebHooksUrl.com", 2)
    info = await qiwi.hooks()

    await bot.send_message(
        chat_id=ME,
        text=f"Bot is starting\nQiwi will send hooks to {info.HookParameters.url}",
    )


qiwi.idle(on_startup=on_startup(), port=5577)
