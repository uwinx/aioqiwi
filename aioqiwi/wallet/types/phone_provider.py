"""
Main model: Provider
"""
from typing import Any, Optional

from aioqiwi.types import BaseModel


class Code(BaseModel):
    value: str
    _name: Optional[str] = None


class Provider(BaseModel):
    code: Code
    message: str
    data: Optional[str] = None
    messages: Optional[Any] = None
