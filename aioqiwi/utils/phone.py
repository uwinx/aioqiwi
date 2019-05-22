import re


def parse_phone(phone):
    """
    Parse given phone number
    :param phone:
    :return: phone as digit or None
    """
    if isinstance(phone, int):
        return str(phone)
    else:
        phone = re.sub(r"[+()\s-]", "", str(phone))
        if phone.isdigit():
            return phone
    raise ValueError("Incorrect phone number")
