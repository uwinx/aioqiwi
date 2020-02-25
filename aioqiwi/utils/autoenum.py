import enum


class NamedEnum(enum.Enum):
    """
    NamedEnum overrides _generate_next_value_ of Enum to name values as they are when auto() is used
    """

    def _generate_next_value_(name, start, count, last_values):
        return name

    @classmethod
    def has(cls, item):
        return any(item == var.value for var in cls)

    @classmethod
    def where(cls, value: str) -> "NamedEnum":
        occ = [item for item in cls if (item.value == value) or (item == value)]
        return occ[-1] if occ else None


auto = enum.auto
