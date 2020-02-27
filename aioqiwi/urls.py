from urllib.parse import urljoin

BASE = "https://edge.qiwi.com/"


class Urls:
    base = BASE

    me = urljoin(BASE, "person-profile/v1/profile/current")
    identification = urljoin(BASE, "identification/v1/persons/{}/identification")
    history = urljoin(BASE, "payment-history/v2/persons/{}/payments")
    stats = urljoin(BASE, "payment-history/v1/persons/{}/payments/total")
    cheque = urljoin(BASE, "payment-history/v1/transactions/{}/cheque/file")

    class Hooks:
        register = urljoin(BASE, "payment-notifier/v1/hooks")
        active = register + "/active"
        test = register + "/test"
        delete = urljoin(register, "hooks/{}")

    class Balance:
        base = urljoin(BASE, "funding-sources/v2/persons/")
        balance = urljoin(base, "{}/accounts")
        available_aliases = urljoin(balance, "offer")
        set_new_balance = urljoin(balance, "accounts/{}")

    class Payments:
        base = urljoin(BASE, "sinap/api/v2/terms/{}/payments")
        to_qiwi = base.format("99")
        providers = "https://qiwi.com/mobile/detect.action"
        commission = urljoin(BASE, "sinap/providers/{}/onlineCommission")

    class P2PBillPayments:
        base = "https://api.qiwi.com/partner/bill/v1/bills/"
        bill = urljoin(base, "{}")
        reject = urljoin(bill, "{}/reject")
        refund = urljoin(bill, "{}/refunds/{}")

    class Maps:
        base = urljoin(BASE, "locator/v3/nearest/clusters")
        ttp_groups = urljoin(BASE, "locator/v3/ttp-groups")
