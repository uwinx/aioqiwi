===========
🥝 aioqiwi
===========

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black
    :alt: aioqiwi-code-style

.. image:: https://img.shields.io/badge/Python%203.7-blue.svg
    :target: https://www.python.org/
    :alt: Python-version

------------
Installation
------------

::

    pip install "https://github.com/uwinx/aioqiwi/archive/master.zip"

---------------
🔸 Dependencies
---------------
**aioqiwi** uses only aiohttp and that's enough, but in case you want increase perfomance of serialization and deserialization, you can install ``ujson`` or ``rapidjson``


-------------------
🔹 Dive-in Example
-------------------
**aioqiwi** is a convenient tool with one-night solved architecture and its models generated from API-docs

.. code:: python

    import asyncio
    from pprint import pprint

    from aioqiwi import QiwiAccount, BeatifulSum

    async def qiwi():
        async with QiwiAccount("APIHASH from https://qiwi.com/api") as client:
            me = await cl.me()
            pprint(me.params_dict)

            client.phone_number = '78787878723'
            balance = await client.balance()

            print("ACCOUNTS:")
            for acc in balance.Accounts:
                print(acc.alias, BeautifulSum(acc.Balance).pretty)

    asyncio.run(qiwi())


--------------------
📣 Handling updates
--------------------
**aioqiwi** provides user-friendly webhooks handler


.. code:: python

    from aioqiwi import QiwiUpdate, QiwiAccount, BeautifulSum

    client = QiwiAccount("...")

    @client.on.payment_event(incoming=True)
    async def outgoing_payments_handler(event: QiwiUpdate):
        print(f"{event.Payment.account} sent you {BeautifulSum(event.Payment).pretty}")

    @client.on.payment_event(incoming=True, comment_regex=r"^(special_code|another_special_code)+$")
    async def outgoing_payments_handler(event: QiwiUpdate):
        print("*tovarish mayor suspiciously*",
              f"- WHO THE HECK IS `{event.Payment.account}`, HOW DID HE GET OUR CODE?",
              sep="\n",)

    client.idle(port=6969)


----------------------
💸 Making transactions
----------------------


.. code:: python

    import asyncio
    from aioqiwi import QiwiAccount, BeautifulSum

    async def txn():
        async with QiwiAccount('...') as client:
            payment = await client.transaction(14.88, '+7899966669')
            print(BeautifulSum(payment.Sum).pretty)

    asyncio.run(txn())


---------------------------------------------------
🔥 Qiwi new API p2p transactions(bill-payments)[RAW]
---------------------------------------------------
I'm discovering this API, looks funny


.. code:: python

    import asyncio
    from aioqiwi import TimeRange, QiwiKassa

    async def kassa():
        async with QiwiKassa("SECRET KEY from p2p.qiwi.com or kassa.qiwi.com") as kassa:
            sent_invoice = await kassa.new_bill(14.88, lifetime=TimeRange(44))
            # setting lifetime to 44 ahead today [default is 10] 45 - is max
            print("Url to pay:", sent_invoice.pay_url)

    asyncio.run(kassa())


`sent_invoice.pay_url` will redirect us to something like:

.. image:: https://imbt.ga/gO8EzaFItB


---------------------------
💳 Handling bill payments
---------------------------


.. code:: python


    from aioqiwi import QiwiKassa, BillUpdate

    kassa = QiwiKassa('PRIVATE_KEY')

    @kassa.on_update(lambda bill: bill.Bill.Amount.currency == 'RUB')
    async def my_shiny_rubles_handler(bill_update: BillUpdate):
        # do something
        pass

    kassa.idle()


----------------
👥 Contributing
----------------

It'd great if you issue some design components. Meantime api-designs are awful, I know.

------------------------------------------
👨‍👨‍👦‍👦 Community
------------------------------------------

`✈️ Telegram
<https://t.me/joinchat/B2cC_hSIAiYXxqKghdguCA>`_

