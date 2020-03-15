from ..core.tooling.htstrings import HeadTailString


class KassaURL(HeadTailString):
    __head__ = "https://api.qiwi.com/"


class urls:
    base = KassaURL("partner/bill/v1/bills/")
    bill = KassaURL("{}", head=base)
    reject = KassaURL("{}/reject", head=base)
    refund = KassaURL("refunds/{}", head=base)
