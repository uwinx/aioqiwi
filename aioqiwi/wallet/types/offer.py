"""
Main model: Offer
"""
from aioqiwi.types import BaseModel


class Offer(BaseModel):
    alias: str
    currency: int
