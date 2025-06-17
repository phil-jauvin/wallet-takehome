class BaseExchangeRateClient:

    @classmethod
    def get_rate(cls, currency_code: str) -> float:
        raise NotImplementedError


class ExchangeRateAPIError(RuntimeError):
    pass