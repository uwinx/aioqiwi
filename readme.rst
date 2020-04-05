===========
🥝 aioqiwi
===========

.. image:: https://img.shields.io/badge/Python%203.7-blue.svg
    :target: https://www.python.org/
    :alt: Python-version

**Qiwi payments for humans(for healthy humans)**

Supports most of `qiwi <https://qiwi.com>`_ apis: `qiwi-maps <https://github.com/QIWI-API/qiwi-map>`_, `bills <https://developer.qiwi.com/en/bill-payments/>`_, `wallet <https://developer.qiwi.com/en/qiwi-wallet-personal/>`_

------------
Installation
------------

::

    pip install aioqiwi

---------------
🔸 Dependencies
---------------

+------------+----------------------------+
| Library    | Description                |
+============+============================+
|  aiohttp   | default http server        |
+------------+----------------------------+
|  pydantic  | schema validation          |
+------------+----------------------------+


**However aioqiwi is highly customizable. Example of switching json modules:**

::

    pip install orjson

.. code-block:: python

    from aioqiwi import Wallet
    from aioqiwi.core.tooling import json

    wallet = Wallet()
    wallet.tools.json_module = json.JSONModule("orjson")

--------------------
🔹 Dive-in Examples
--------------------

.. code:: python

    import asyncio

    from aioqiwi import Wallet

    async def qiwi():
        async with Wallet("TOKEN from https://qiwi.com/api") as w:
            w.phone_number = '+7878787878'  # phone number is not required by default, but some methods need it
            balance = await w.balance()
            print("ACCOUNTS:")
            for acc in balance.accounts:
                print(acc.alias, acc.balance)

    asyncio.run(qiwi())


--------------------
📣 Handling updates
--------------------

**aioqiwi** provides user-friendly web-hooks handler


.. code:: python

    import asyncio
    from aioqiwi.wallet import WebHook, Wallet

    wallet = Wallet("...")

    @wallet.hm(lambda event: ...)
    async def payments_handler(hook: WebHook):
        print(f"{hook.payment.account} sent you {event.payment}")

    @wallet.hm()
    async def secret_payments_handler(event: WebHook):
        await something(event.payment.commission.amount)

    wallet.idle(port=8090)

When you do `Wallet::idle`, aioqiwi adds connector closing to `aiohttp.web.Application::on_shutdown` to make sure connector closes, however if you want to avoid this behaviour pass `close_connector_ate=False` to `Wallet::idle`

****************
Handler manager
****************

Handler manager `QiwiClient.handler_manager` or `qiwi_client.hm` is responsible for event-handlers registering and filtering/delivering updates to them.
There're currently two event processing strategies:
1. `core.handler.EventProcessStrategy.ORDERED` - sequential filter-check. has O(n) amplitude
2. `core.handler.EventProcessStrategy.MILKSHAKE` - as receives update, will shuffle existing handlers list. has O(n) amplitude

.. note::
    Filters results are not currently cached.

.. note::
    Some users don't want mess with web-hooks, for those fellas aioqiwi has `history_polling` [wip] in `aioqiwi.contrib`. Different approach for dealing with payment events.
    Find usage example in `examples/` directory.

---------------------------------------------------
🔥 Qiwi API p2p transactions(bills)
---------------------------------------------------

.. code:: python

    import asyncio
    from aioqiwi import QiwiKassa

    async def test_kassa():
        async with QiwiKassa("SECRET KEY from p2p.qiwi.com or kassa.qiwi.com") as kassa:
            sent_invoice = await kassa.new_bill(14.88, lifetime=44)
            # setting lifetime to 44 ahead today [default is 10] 45 - is max
            print("Url to pay:", sent_invoice.pay_url)
            await kassa.close()

    asyncio.run(test_kassa())


``sent_invoice.pay_url`` will redirect us to something like:

.. image:: https://imbt.ga/gO8EzaFItB


---------------------------
💳 Handling bill payments
---------------------------


.. code:: python


    from aioqiwi.kassa import QiwiKassa, Notification

    kassa = QiwiKassa('PRIVATE_KEY')

    @kassa.hm(lambda bill: bill.bill.amount.currency == 'RUB')
    async def my_shiny_rubles_handler(bill_update: Notification):
        # do something
        pass

    kassa.idle()


--------------------
🗺 QIWI terminals
--------------------

**aioqiwi** covers qiwi's `MAPS
<https://developer.qiwi.com/ru/qiwi-map>`_ api in aioqiwi.terminals module

---------------
Connectors
---------------

QiwiClient.connector is responsible for making http requests. Current available request managers are located in `aioqiwi.core.connectors`

Default connector is `aioqiwi.core.connectors.asyncio`, but if it's no suit for you, you can easily switch to another

Example:

.. code:: python3

    from aioqiwi import Wallet
    from aioqiwi.core.connectors.aiohttp import AiohttpConnector

    wallet = Wallet("auth")
    # switch with read-to-use connector-like instance implementing
    wallet.connector = AiohttpConnector(timeout, {"user-agent": "opeka/02"})
    # or switch with aioqiwi.core.connectors.abstract.Connector compatible class
    wallet.connector = AiohttpConnector

*******************
Hacking connector
*******************

You can easily implement your own http client(connector), subclassing from `aioqiwi.core.connectors.abstract.AbstractConnector`. Take a look at "out of the box" `aiohttp` or `asyncio` sessions for the start.

-----------------------
👾 Handling errors
-----------------------

******************
API request error
******************

Consider we have a `aioqiwi.wallet.Wallet` instance with a named reference `wallet` to it.
Known error when we cannot ask server for more than 50 rows in `wallet.history`. To handle that error, we simply:

.. code:: python

    from aioqiwi.exceptions import AioqiwiError
    from aioqiwi.errors import ErrorInfo

    try:
        await wallet.history(2 ** 6)  # pass rows=64, whilst constraint is 0<rows<51
    except AioqiwiError as exc:
        if exc.err:  # this feature is experimental
            exc.err: ErrorInfo = exc.err  # cast to aioqiwi.Wallet's error info
            print(exc.err.error_message)

***************
TimeoutError
***************

This is slight different error and aioqiwi should not be really responsible for it. It's usually server-side error
which makes exception that should be raised connector-specific. `asyncio.TimeoutError` is exception that is produced
by `asyncio` connector. In `aiohttp` or other connectors it may differ.

-----------------------------
⛏ return policies (types)
-----------------------------

aioqiwi's server.BaseWebHookView and requests.Requests support "return policy", it means you can get response/update in the form that suits your needs.
There're currently 5 return policies.

- NOTHING - returns nothing(note: None is python's implicit return), :note: returning nothing does not mean doing nothing, validation is done anyway
- READ_DATA - raw return once stream is read
- JSON - raw return once read data was deserialized
- MODEL - complex return once json deserialized and new model instantiated
- LIST_OF_MODELS - complex return once json deserialized as an iterable list with new instantiated models of json objects

-------------------
❓ HOW-TOs
-------------------

You can find examples in ``examples/`` directory in github repository. For start examples above should be enough.


---------------------------
🔧 TODOs
---------------------------

- **Tests/CI/CD**
- **Implement all qiwi wallet API methods**

-----------------
Work in progress
-----------------

- history_polling needs to be tested
- implement wallet web-hook payment verification

------------------------------------------
🐦 Community
------------------------------------------

**My group**
`✈️ Telegram
<https://t.me/joinchat/B2cC_hSIAiYXxqKghdguCA>`_
