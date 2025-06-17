import requests
from cachetools import cached, TTLCache
from fastapi import HTTPException, status

from settings import api_settings

from clients.exchange_rates.base import BaseExchangeRateClient

from models.wallet import Currency


CONVERSION_URL = f"{api_settings.nbp_api_url}/{api_settings.nbp_api_conversion_endpoint}"


class NBPExchangeRateClient(BaseExchangeRateClient):

    # The function has a cache mechanism to prevent spamming the NBP API, the result
    # will be cached for as long as defined by the cache ttl value.
    # By default, we set this setting to 5 minutes.
    @classmethod
    @cached(cache=TTLCache(maxsize=10, ttl=api_settings.cache_ttl))
    def get_rate(cls, currency_code: str) -> float:
        """
        Returns the rate of PLN to given currency.
        """
        # Check that we're passing in a valid currency
        Currency(currency_code)

        formatted_conversion_url = CONVERSION_URL % currency_code.lower()
        nbp_api_response = requests.get(formatted_conversion_url)

        if nbp_api_response.status_code == 200:
            return nbp_api_response.json()["rates"][0]["ask"]

        # TODO: maybe this should go to the parent class ?
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not retrieve exchange rate information",
        )
