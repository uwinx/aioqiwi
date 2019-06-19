"""

Before running install aiogram, cool telegram bot-api wrapper
    ::

        pip install aiogram

"""
from aiogram import Bot

from aioqiwi.utils import BeautifulSum
from aioqiwi.wallet import Wallet, QiwiUpdate

ME = 124191486  # your telegram user id

qiwi = Wallet("token from qiwi")
bot = Bot("telegram bot token", parse_mode="markdown")


@qiwi.on_update(incoming=True)
async def new_payment(event: QiwiUpdate):
    payment = event.Payment
    text = f":D Woop-woop! {payment.account} sent you {BeautifulSum(payment.Sum).humanize}\n"
    text += f"Commentary: {payment.comment}" if payment.comment else ""

    await bot.send_message(ME, text)


async def on_startup():
    await bot.send_message(ME, "Bot is starting")


qiwi.idle(on_startup(), port=1488)
