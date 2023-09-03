from typing import Any
from abc import ABC, abstractmethod

import humps
import requests


class BaseMerchantManager(ABC):
    """
    Abstract base class for defining interface for child classes.
    """

    def __init__(self, schema_type: str):
        self.schema_type = schema_type

    def _convert_request_data(self, data: Any):
        """
        We have more than one merchant and merchants have different json key types for example:
        Camelize, Pascalize and so on.
        This function helps us to convert from snake type
        to any type which is required by merchant.
        """
        return getattr(humps, self.schema_type)(data)

    def _send_transaction(self, url: str, data: Any):
        """
        Private function for sending transactions to core.
        """
        converted_data = self._convert_request_data(data)
        res = requests.post(url, json=converted_data)
        return res

    @abstractmethod
    def send_bet(self, url: str, amount: int | float, player: Any) -> requests.Response:
        """
        Abstract method for sending player bet to merchant.
        """

    @abstractmethod
    def send_win(self, url: str, amount: int | float, player: Any) -> requests.Response:
        """
        Abstract method for sending player win to merchant.
        """

    @abstractmethod
    def send_rollback(
        self, url: str, amount: int | float, player: Any
    ) -> requests.Response:
        """
        Abstract method for sending rollback request to merchant.
        """
