from ..core.tooling.htstrings import HeadTailString


class WalletURL(HeadTailString):
    __head__ = "https://edge.qiwi.com/"


class urls:
    me = WalletURL("person-profile/v1/profile/current")
    identification = WalletURL("identification/v1/persons/{}/identification")
    history = WalletURL("payment-history/v2/persons/{}/payments")
    stats = WalletURL("payment-history/v2/persons/{}/payments/total")
    cheque = WalletURL("payment-history/v1/transactions/{}/cheque/file")
    request_cheque = WalletURL("payment-history/v1/transactions/{}/cheque/send")
    payment_info = WalletURL("payment-history/v2/transactions/{}")

    class web_hooks:
        register = WalletURL("payment-notifier/v1/hooks")
        active = WalletURL("/active", head=register)
        test = WalletURL("/test", head=register)
        delete = WalletURL("/{}", head=register)

    class balance:
        base = WalletURL("funding-sources/v2/persons/")
        balance = WalletURL("{}/accounts", head=base)
        available_aliases = WalletURL("/offer", head=balance)
        set_new_balance = WalletURL("/{}", head=balance)

    class payments:
        base = WalletURL("sinap/api/v2/terms/{}/payments")
        providers = WalletURL("", head="https://qiwi.com/mobile/detect.action")
        commission = WalletURL("sinap/providers/{}/onlineCommission")
