from typing import TypedDict, NotRequired


class BaseRequestBody(TypedDict):
    """
    Base TypedDict class for Every Matrix merchant.
    """

    token: str
    amount: int | float
    currency: str
    game_id: str
    round_id: str
    external_id: str
    hash: str
    bet_external_id: NotRequired[str]
    canceled_external_id: NotRequired[str]
