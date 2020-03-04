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

+------------+--------------------+
| Library    | Description        |
+============+====================+
|  aiohttp   | http server/client |
+------------+--------------------+
|  pydantic  | schema validation  |
+------------+--------------------+

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

    @wallet.hm(lambda event: ...)
    async def payments_handler(hook: WebHook):
        print(f"{hook.payment.account} sent you {event.payment}")

    @wallet.hm()
    async def secret_payments_handler(event: WebHook):
        await something(event.payment.commission.amount)

    wallet.idle(port=8090)


If you don't want to set up server, aioqiwi provides contrib with


.. code:: python


    from aioqiwi.wallet import Wallet, types
    from aioqiwi.wallet.contrib import history_polling

    w = Waller(...)

    @w.hm()
    async def ph(event: types.PaymentData):
        ...

    history_polling(w, ...)


(!) It's different from original webhook type



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


-----------------------------
⛏ return policies
-----------------------------

aioqiwi's server.BaseWebHookView and requests.Requests support "return policy", it means you can get response/update in the form that suits your needs.
Read more:

>>> from aioqiwi.core import returns
>>> help(returns.ReturnType)


-------------------
❓ HOW-TOs
-------------------

You can find examples in ``examples/`` directory in github repository. For start examples above should be enough.


---------------------------
🔧 TODOs
---------------------------

- **Tests** 🔥

------------------------------------------
🐦 Community
------------------------------------------

**My group**
`✈️ Telegram
<https://t.me/joinchat/B2cC_hSIAiYXxqKghdguCA>`_
