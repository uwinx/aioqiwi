===========
🥝 aioqiwi
===========

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black
    :alt: aioqiwi-code-style

.. image:: https://img.shields.io/badge/Python%203.7-blue.svg
    :target: https://www.python.org/
    :alt: Python-version

.. image:: https://api.codacy.com/project/badge/Grade/f3c436d869d04a7095b980f71a78ad51
    :target: https://www.codacy.com/app/uwinx/aioqiwi?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=uwinx/aioqiwi&amp;utm_campaign=Badge_Grade
    :alt: codacy-rating


*(!) WARNING AT CURRENT STATE AIOQIWI IS NOT PRODUCTION-READY (!)*


**Qiwi payments for humans(for healthy humans)**

Supports most of `qiwi <https://qiwi.com>`_ apis: `qiwi-maps <https://github.com/QIWI-API/qiwi-map>`_, `bills <https://developer.qiwi.com/en/bill-payments/>`_, `wallet <https://developer.qiwi.com/en/qiwi-wallet-personal/>`_

------------
Installation
------------

::

    pip install "https://github.com/uwinx/aioqiwi/archive/master.zip"

---------------
🔸 Dependencies
---------------
**aioqiwi** uses only ``aiohttp`` and that's enough, but in case you want increase perfomance of serialization and deserialization, you can install ``ujson`` or ``rapidjson``


-------------------
🔹 Dive-in Example
-------------------
**aioqiwi** is a convenient tool with one-night solved architecture and its models generated from API-docs

.. code:: python

    import asyncio

    from aioqiwi import Wallet
    from aioqiwi.utils import BeautifulSum

    async def qiwi():
        async with Wallet("TOKEN from https://qiwi.com/api") as wallet:
            wallet.phone_number = '+7878787878'  # phone number is not required by default, but some methods need it
            balance = await wallet.balance()
            print("ACCOUNTS:")
            for acc in balance.Accounts:
                print(acc.alias, BeautifulSum(acc.Balance).pretty)

    asyncio.run(qiwi())


--------------------
📣 Handling updates
--------------------
**aioqiwi** provides user-friendly webhooks handler


.. code:: python

    from aioqiwi.wallet import QiwiUpdate, Wallet
    from aioqiwi.utils import BeautifulSum

    wallet = Wallet("...")

    @wallet.on_update(incoming=True)
    async def payments_handler(event: QiwiUpdate):
        print(f"{event.Payment.account} sent you {BeautifulSum(event.Payment).pretty}")

    @wallet.on_update(incoming=True, comment_regex=r"^(special_code|another_special_code)+$")
    async def secret_payments_handler(event: QiwiUpdate):
        print("*tovarish mayor suspiciously*",
              f"- WHO THE HECK IS `{event.Payment.account}`, HOW DID HE GET OUR CODE?",
              sep="\n",)

    wallet.idle(port=6969)


----------------------
💸 Making transactions
----------------------


.. code:: python

    import asyncio
    from aioqiwi import Wallet
    from aioqiwi.utils import BeautifulSum

    async def txn():
        async with Wallet('...') as wallet:
            payment = await wallet.transaction(14.88, '+7899966669')
            print(BeautifulSum(payment.Sum).pretty)

    asyncio.run(txn())


---------------------------------------------------
🔥 Qiwi new API p2p transactions(bill-payments)
---------------------------------------------------
Cool qiwi bills!


.. code:: python

    import asyncio
    from aioqiwi import QiwiKassa

    async def kassa():
        async with QiwiKassa("SECRET KEY from p2p.qiwi.com or kassa.qiwi.com") as kassa:
            sent_invoice = await kassa.new_bill(14.88, lifetime=44)
            # setting lifetime to 44 ahead today [default is 10] 45 - is max
            print("Url to pay:", sent_invoice.pay_url)

    asyncio.run(kassa())


`sent_invoice.pay_url` will redirect us to something like:

.. image:: https://imbt.ga/gO8EzaFItB


---------------------------
💳 Handling bill payments
---------------------------


.. code:: python


    from aioqiwi.kassa import QiwiKassa, BillUpdate

    kassa = QiwiKassa('PRIVATE_KEY')

    @kassa.on_update(lambda bill: bill.Bill.Amount.currency == 'RUB')
    async def my_shiny_rubles_handler(bill_update: BillUpdate):
        # do something
        pass

    kassa.idle()


--------------------
🗺 QIWI terminals
--------------------

**aioqiwi** covers qiwi's `MAPS
<https://developer.qiwi.com/ru/qiwi-map>`_ api in aioqiwi.terminals module


-----------------------------
🍼 Non-model returns(json)
-----------------------------


.. code:: python


        import asyncio
        from aioqiwi import Wallet

        async def json_response():
            async with Wallet('...') as wallet:
                wallet.as_model = False
                print(await wallet.balance())

        asyncio.run(json_response())


-------------------
❓ HOW-TOs
-------------------

You can find examples in ``examples/`` directory in github repository. For start examples above should be enough.

----------------
👥 Contributing
----------------

It'd great if you issue some design components. Meantime api-designs are awful, I know.


---------------------------
🔧 TODOs
---------------------------

- **Error handling** 🔥 (for now you can handle aioqiwi.models.exceptions.ModelConversionError using ``as_model``)
- **Tests** 🔥
- **Documentation**

------------------------------------------
👨‍👨‍👦‍👦 Community
------------------------------------------

**My group**
`✈️ Telegram
<https://t.me/joinchat/B2cC_hSIAiYXxqKghdguCA>`_
