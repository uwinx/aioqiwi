import logging
import uuid
import base64

from ..models import sent_invoice
from ..mixin import QiwiMixin, serialize
from ..utils.currency_utils import Currency
from ..utils.time_utils import TimeRange
from ..utils.phone import parse_phone

logger = logging.getLogger("aioqiwi")


class QiwiKassa(QiwiMixin):
    def __init__(self, api_hash: str):
        """
        Beta of kassa.qiwi.com currently developing
        :param api_hash: Qiwi unique token given for an account
        """
        session = self._new_http_session(api_hash)
        self.__session = session

        self.__get = session.get
        self.__post = session.post
        self.__put = session.put
        self.__delete = session.delete
        self.__patch = session.patch

    @staticmethod
    def generate_bill_id():
        # further monkey-patches are welcome
        return (
            base64.urlsafe_b64encode(uuid.uuid3(uuid.uuid4(), "").bytes)
            .decode()
            .rstrip("=")
            .upper()
        )

    async def issue_invoice(
        self,
        amount: float,
        peer: int or str = None,
        peer_email: str = None,
        lifetime: TimeRange = TimeRange(10),
        currency: str or int or Currency = Currency["rub"],
        comment: str = "via aioqiwi",
        bill_id: str = None,
    ) -> sent_invoice.SentInvoice:
        """

        :param amount: invoice amount rounded down to two decimals
        :param peer: phone number to which invoice issued
        :param peer_email: client's e-mail
        :param lifetime: invoice due date, pass TimeRange class which is cool and convenient
        :param currency: pass Currency object or integer code like <845> of currency or str code like <'USD'>
        :param comment: invoice commentary
        :param bill_id: unique invoice identifier in merchant's system
        :return: SentInvoice if success
        """
        ccode = (
            currency.code
            if isinstance(currency, Currency.currency)
            else Currency[currency].code
        )
        url = "https://api.qiwi.com/partner/bill/v1/bills/{bill_id}".format(
            bill_id=bill_id or self.generate_bill_id()
        )

        data = serialize(
            self.param_filter(
                {
                    "amount": {"currency": ccode, "value": amount},
                    "comment": comment,
                    "expirationDateTime": lifetime.to_date.today,
                    "customer": {"phone": parse_phone(peer), "account": peer_email}
                    if peer and peer_email
                    else {},
                    "customFields": {},
                }
            )
        )

        async with self.__put(data=data, url=url) as response:
            return await self._make_return(response, sent_invoice.SentInvoice)

    # session-related
    async def close(self):
        await self.__session.close()

    # `async with` block
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
