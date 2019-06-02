"""
Before running install aiogram, cool telegram bot-api wrapper
"""
from aioqiwi.wallet import Wallet, QiwiUpdate
from aioqiwi.utils import BeautifulSum

from aiogram import Bot, Dispatcher, types
from aiogram.utils import markdown

ME = 124191486  # your telegram user id

qiwi = Wallet("qiwiToken")
bot = Bot("telegramBotToken", parse_mode="markdown")
disp = Dispatcher(bot)


@qiwi.on_update(incoming=True)
async def new_payment(event: QiwiUpdate):
    payment = event.Payment
    text = f":D Woop-woop! {payment.account} sent you {BeautifulSum(payment.Sum).humanize}\n"
    text += f"Commentary: {payment.comment}" if payment.comment else ""

    await bot.send_message(ME, text)


@disp.message_handler(commands=["send"], prefix="./!")
@disp.message_handler(regexp=r"^.send \d*\.?\d* (\(?\+?[0-9]*\)?)?[0-9_\- \(\)] .*")
async def send_money(event: types.Message):
    # process text with pattern: .send amount_float receiver_phone_number comments
    cmd, amount, peer, comment = event.text.split(maxsplit=3)

    info = await qiwi.transaction(amount, peer)

    await event.reply(
        f"`{BeautifulSum(info.Sum).humanize}` was sent to **{info.Fields.account}** "
        f"<__{markdown.escape_md(info.comment)}__>"
    )


qiwi.idle((disp.start_polling, {"fast": True}), port=1488)
