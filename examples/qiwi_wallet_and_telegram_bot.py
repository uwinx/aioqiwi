"""
Install aiogram, cool telegram bot-api wrapper
"""
from aioqiwi.wallet import Wallet, QiwiUpdate
from aioqiwi.utils import BeautifulSum

from aiogram import Bot, Dispatcher

ME = 124191486  # telegram_id

qiwi = Wallet('qiwiToken')
bot = Bot('telegramBotToken')
disp = Dispatcher(bot)


@qiwi.on.payment_event(incoming=True)
async def new_payment(event: QiwiUpdate):
    payment = event.Payment
    text = f':D Woop-woop! {payment.account} sent you {BeautifulSum(payment.Sum).humanize}\n'
    text += f'Commentary: {payment.comment}' if payment.comment else ''

    await bot.send_message(ME, text)

qiwi.idle((disp.start_polling, {'fast': True}), port=1488)
