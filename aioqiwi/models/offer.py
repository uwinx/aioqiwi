from dataclasses import dataclass


@dataclass(init=False)
class Offer:
    alias: str
    currency: int
