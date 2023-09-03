from bogir.mima_merch_manager import MimaMerchantManager
from bogir.everymatrix_merch_manager import EveryMatrixMerchantManager
from bogir.base_merchant_manager import BaseMerchantManager


class MerchantFactory:
    @staticmethod
    def build_merchant(merchant_name: str, schema_type: str) -> BaseMerchantManager:
        """
        Factory method which returns merchant manager class by given parameter merchant_name.
        """
        merchant_name = merchant_name.lower()
        if merchant_name == "mima":
            return MimaMerchantManager(schema_type)
        if merchant_name == "everymatrix":
            return EveryMatrixMerchantManager(schema_type)

        raise ValueError(f"There is no merchant with name {merchant_name}")
