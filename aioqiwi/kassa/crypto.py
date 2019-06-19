from hashlib import sha256
from hmac import new


def hmac_key(secret, amount, status, bill_id, site_id):
    # {amount.currency}|{amount.value}|{billId}|{siteId}|{status.value}
    invoice_parameters = (
        f"{amount.currency}|{amount.value}|{bill_id}|{site_id}|{status.value}"
    ).encode("utf-8")

    seckey = sha256()
    seckey.update(secret.encode("utf-8"))

    return new(seckey, invoice_parameters, sha256)
