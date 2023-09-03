from typing import Dict
import requests

from bogir.base_merchant_manager import BaseMerchantManager
from bogir.schemas.mima import TransactionTypes, RequestBody


class MimaMerchantManager(BaseMerchantManager):
    """
    Class which provides api for making transactions(bet, win, rollback)
    sends api requests to mima core.
    WARNING: you should use this class only in workers(celery) if you
    will use this class in web server it may slow your server.
    """

    def parse_request_data_from_player(
        self, player: Dict, amount: int | float, transaction_type: TransactionTypes
    ) -> RequestBody:
        """
        Parses all necessary information from player dict object for request to core.
        """
        request_data: RequestBody = {
            "token": player["token"],
            "amount": amount,
            "round_id": player["round_id"],
            "external_id": str(player["_id"]),
            "transaction_type": transaction_type,
        }
        return request_data

    def send_bet(
        self, url: str, amount: int | float, player: Dict
    ) -> requests.Response:
        request_data = self.parse_request_data_from_player(
            player, amount, TransactionTypes.BET
        )
        return self._send_transaction(url, request_data)

    def send_win(
        self, url: str, amount: int | float, player: Dict
    ) -> requests.Response:
        request_data = self.parse_request_data_from_player(
            player, amount, TransactionTypes.WIN
        )
        return self._send_transaction(url, request_data)

    def send_rollback(
        self, url: str, amount: int | float, player: Dict
    ) -> requests.Response:
        request_data = self.parse_request_data_from_player(
            player, amount, TransactionTypes.ROLLBACK
        )
        return self._send_transaction(url, request_data)
