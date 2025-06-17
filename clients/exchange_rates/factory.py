from typing import Type

from clients.exchange_rates.base import BaseExchangeRateClient
from clients.exchange_rates.nbp_client import NBPExchangeRateClient

from models.wallet import LocalCurrency


class ExchangeRateClientFactory:
    """
    Factory class that returns the correct client to be used
    for fetching exchange rate information.
    """

    @staticmethod
    def get_client(currency: LocalCurrency) -> Type[BaseExchangeRateClient]:
        if currency == LocalCurrency.PLN:
            return NBPExchangeRateClient

        raise ValueError(f"Currency {str(currency)} doesn't have an exchange rate client")
