from typing import Annotated

from botocore.exceptions import ClientError

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from models.auth import Token
from models.util import NonNegativeDecimal
from models.wallet import ClientWallet, CommonWalletData, Currency

from services.wallet_service import WalletService
from services.auth_service import AuthService

app = FastAPI()


@app.get("/wallet/original")
async def get_original_wallet(user_id: Annotated[str, Depends(AuthService.get_user_id)]) -> CommonWalletData:
    """
    Returns an object containing wallet balances
    without conversions to local currency
    """
    data = WalletService.get_original_wallet(user_id)
    return data


@app.get("/wallet")
async def get_wallet(user_id: Annotated[str, Depends(AuthService.get_user_id)]) -> ClientWallet:
    """
    Returns an object containing wallet balances
    converted to local currency, as well as the sum of all balances
    """
    data = WalletService.get_local_currency_wallet(user_id)
    return data


@app.post("/wallet/add/{currency_code}/{balance}")
async def add_balance_to_wallet(
        currency_code: Currency,
        balance: NonNegativeDecimal,
        user_id: Annotated[str, Depends(AuthService.get_user_id)]
):
    """
    Adds a given quantity of a currency to the wallet
    """
    WalletService.add_to_wallet(user_id, currency_code, balance)


@app.post("/wallet/subtract/{currency_code}/{balance}")
async def subtract_balance_from_wallet(
        currency_code: Currency,
        balance: NonNegativeDecimal,
        user_id: Annotated[str, Depends(AuthService.get_user_id)]
):
    """
    Removes a given quantity of a currency from the wallet
    """
    try:
        WalletService.subtract_from_wallet(user_id, currency_code, balance)
    except ClientError as error:
        if error.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can't subtract more than balance",
            )


@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """
    Ingests a username/password combo and returns a token
    if the user information is valid
    """
    user = AuthService.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return AuthService.create_access_token(
        data={"sub": user.user_id}
    )