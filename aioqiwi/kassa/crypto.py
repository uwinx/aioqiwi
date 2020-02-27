import binascii
from hmac import new
from hashlib import sha256


def hmac_key(key, amount, status, bill_id, site_id):
    byte_key = binascii.unhexlify(key)
    invoice_params = (
        f"{amount.currency}|{amount.value}|{bill_id}|{site_id}|{status.value}"
    ).encode("utf-8")

    return new(byte_key, invoice_params, sha256).hexdigest().upper()
