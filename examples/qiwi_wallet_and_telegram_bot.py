"""
Before running install aiogram, cool telegram bot-api wrapper
    ::

        pip install aiogram

"""
import asyncio

from aiogram import Bot
from aioqiwi.wallet import Wallet, WebHook

ME = 124191486  # your telegram user id

loop = asyncio.get_event_loop()

qiwi = Wallet("MyQiwiToken", loop=loop)
bot = Bot("MyBotToken", validate_token=False)


@qiwi.hm()
async def special_payments_handler(event: WebHook):
    payment = event.payment
    text = f":D Woop-woop! {payment.account} sent you {payment.sum.amount}\n"

    await bot.send_message(chat_id=ME, text=text)


async def on_startup():
    # change hooks if you want
    # info = await qiwi.new_hooks("http://myNewWebHooksUrl.com", 2)
    info = await qiwi.hooks()

    await bot.send_message(
        chat_id=ME,
        text=f"Bot is starting\nQiwi will send hooks to {info.hook_parameters.url}",
    )


if __name__ == '__main__':
    loop.run_until_complete(on_startup())
    qiwi.idle(port=5577)
