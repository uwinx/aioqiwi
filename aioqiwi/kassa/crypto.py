from hashlib import sha256
from hmac import HMAC


def hmac_key(secret, amount, status, bill_id, site_id):
    # {amount.currency}|{amount.value}|{billId}|{siteId}|{status.value}
    invoice_parameters = (
        f"{amount.currency}|{amount.value}|{bill_id}|{site_id}|{status.value}"
    )
    return HMAC(sha256, secret, invoice_parameters)
