from aioqiwi.wallet import Wallet, types, enums
from aioqiwi.core.currencies import Currency

from aioqiwi import Wallet

wallet = Wallet("api-key", phone_number="phone-number")


async def main():
    # using context manager to close wallet connector after we finish
    async with wallet:
        payment_type = types.P2PPayment(
            id=None,
            sum=types.payment.Sum(
                amount=0.18,
                currency=Currency.get("RUB").isoformat
            ),
            comment="hEy_IaM_uSiNg_AiOqIwI",
            paymentMethod=enums.PaymentMethodConst,
            fields=types.Fields(
                account="RECEIVER\'S PHONE NUMBER"
            )
        )

        txn = await wallet.transaction(
            provider_id=enums.Provider.QIWI_WALLET,
            payment_type=payment_type
        )

        print(txn)
