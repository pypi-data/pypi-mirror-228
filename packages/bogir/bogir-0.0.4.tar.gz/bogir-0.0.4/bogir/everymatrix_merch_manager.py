from typing import Dict
import requests

from bogir.base_merchant_manager import BaseMerchantManager
from bogir.schemas.everymatrix import BaseRequestBody


class EveryMatrixMerchantManager(BaseMerchantManager):
    """
    Class which provides api for making transactions(bet, win, rollback)
    sends api requests to every matrix core.
    WARNING: you should use this class only in workers(celery) if you
    will use this class in web server it may slow your server.
    """

    def parse_request_data_from_player(
        self,
        amount: int | float,
        player: Dict,
    ) -> BaseRequestBody:
        """
        Parses all necessary information from player dict object for request to core.
        """
        request_data: BaseRequestBody = {
            "token": player["token"],
            "amount": amount,
            "currency": player.get("currency", "USD"),
            "game_id": player["game_id"],
            "round_id": player["round_id"],
            "external_id": str(player["_id"]),
            "hash": "",
        }
        return request_data

    def send_bet(
        self, url: str, amount: int | float, player: Dict
    ) -> requests.Response:
        request_data = self.parse_request_data_from_player(amount, player)
        return self._send_transaction(url, request_data)

    def send_win(
        self, url: str, amount: int | float, player: Dict
    ) -> requests.Response:
        request_data = self.parse_request_data_from_player(amount, player)
        request_data["bet_external_id"] = str(player["_id"])
        return self._send_transaction(url, request_data)

    def send_rollback(
        self, url: str, amount: int | float, player: Dict
    ) -> requests.Response:
        request_data = self.parse_request_data_from_player(amount, player)
        request_data["canceled_external_id"] = str(player["_id"])
        return self._send_transaction(url, request_data)
