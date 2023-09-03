from typing import TypedDict
from enum import StrEnum


class TransactionTypes(StrEnum):
    """
    Enum for MIMA merchant which requires transaction_types in body of the request.
    """

    BET = "bet"
    ROLLBACK = "rollback"
    WIN = "win"


class RequestBody(TypedDict):
    """
    Base class for checking incoming dict it will prevent developers making from typos.
    """

    token: str
    amount: float | int
    round_id: str
    external_id: str
    transaction_type: TransactionTypes
