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

    pip install "https://github.com/uwinx/aioqiwi/archive/master.zip"

---------------
🔸 Dependencies
---------------

+------------+--------------------+-----------+
| Library    | Description        | Optional  |
+============+====================+===========+
|  aiohttp   | http server/client |    \-     |
+------------+--------------------+-----------+
|  pydantic  | schema validation  |    \-     |
+------------+--------------------+-----------+
|  ujson     | json de/serializer |    \+     |
+------------+--------------------+-----------+
|  rapidjson | json de/serializer |    \+     |
+------------+--------------------+-----------+
|  orjson    | json de/serializer |    \+     |
+------------+--------------------+-----------+

-------------------
🔹 Dive-in Example
-------------------

.. code:: python

    import asyncio

    from aioqiwi import Wallet

    async def qiwi():
        wallet = Wallet("TOKEN from https://qiwi.com/api")
        wallet.phone_number = '+7878787878'  # phone number is not required by default, but some methods need it
        balance = await wallet.balance()
        await wallet.close()
        print("ACCOUNTS:")
        for acc in balance.accounts:
            print(acc.alias, acc.balance)

    asyncio.run(qiwi())


--------------------
📣 Handling updates
--------------------
**aioqiwi** provides user-friendly webhooks handler


.. code:: python

    from aioqiwi.wallet import WebHook, Wallet

    wallet = Wallet("...")

    @wallet.on_update(lambda event: ...)
    async def payments_handler(hook: WebHook):
        print(f"{hook.payment.account} sent you {BeautifulSum(event.Payment).pretty}")

    @wallet.on_update()
    async def secret_payments_handler(event: WebHook):
        await something(event.payment.commission.amount)

    wallet.idle(port=8090)


----------------------
💸 Making transactions
----------------------


.. code:: python

    import asyncio
    from aioqiwi import Wallet

    async def txn():
        wallet = Wallet('...')
        payment = await wallet.transaction(14.88, '+7899966669')
        print(payment.sum.amount)
        await wallet.close()

    asyncio.run(txn())


---------------------------------------------------
🔥 Qiwi new API p2p transactions(bill-payments)
---------------------------------------------------
Cool qiwi bills!


.. code:: python

    import asyncio
    from aioqiwi import QiwiKassa

    async def kassa():
        kassa = QiwiKassa("SECRET KEY from p2p.qiwi.com or kassa.qiwi.com")
        sent_invoice = await kassa.new_bill(14.88, lifetime=44)
        # setting lifetime to 44 ahead today [default is 10] 45 - is max
        print("Url to pay:", sent_invoice.pay_url)
        await kassa.close()

    asyncio.run(kassa())


`sent_invoice.pay_url` will redirect us to something like:

.. image:: https://imbt.ga/gO8EzaFItB


---------------------------
💳 Handling bill payments
---------------------------


.. code:: python


    from aioqiwi.kassa import QiwiKassa, BillUpdate

    kassa = QiwiKassa('PRIVATE_KEY')

    @kassa.on_update(lambda bill: bill.bill.amount.currency == 'RUB')
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
            wallet = with Wallet('...')
            wallet.as_model = False
            print(await wallet.balance())
            # some json value printed
            await wallet.close()

        asyncio.run(json_response())


-------------------
❓ HOW-TOs
-------------------

You can find examples in ``examples/`` directory in github repository. For start examples above should be enough.


---------------------------
🔧 TODOs
---------------------------

- **Tests** 🔥

------------------------------------------
👨‍👨‍👦‍👦 Community
------------------------------------------

**My group**
`✈️ Telegram
<https://t.me/joinchat/B2cC_hSIAiYXxqKghdguCA>`_
