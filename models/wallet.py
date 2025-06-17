from typing import Dict

from pydantic import BaseModel, NonNegativeFloat, PositiveFloat, UUID4

from enum import Enum


# This currency model is used for currencies that
# are held by the user.
class Currency(str, Enum):
    """
    Enum that contains all valid holding currencies supported by the API
    """
    JPY = "JPY"
    EUR = "EUR"
    USD = "USD"


# This currency model is used to define
# what currency the holding currencies can be converted to.
# For example, our USD holdings can be converted to PLN but not to GBP.
class LocalCurrency(str, Enum):
    """
    Enum that contains all valid local currencies supported by the API
    """
    PLN = "PLN"


class CommonWalletData(BaseModel):
    balances: Dict[Currency, NonNegativeFloat]


class StoredWallet(CommonWalletData):
    user_id: UUID4
    local_currency: LocalCurrency = LocalCurrency.PLN


class ClientWallet(CommonWalletData):
    total: PositiveFloat




