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

    client.start_webhooks(port=6969)


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


------------
Contributing
------------

Contributions are welcome

----------
Community:
----------

`✈️ Telegram
<https://t.me/joinchat/B2cC_hSIAiYXxqKghdguCA>`_

