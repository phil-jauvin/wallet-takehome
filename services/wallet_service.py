from decimal import Decimal

from clients.aws import wallets_table
from clients.exchange_rates import ExchangeRateClientFactory

from models.wallet import StoredWallet, ClientWallet, CommonWalletData


class WalletService:
    """
    Service allowing interaction with user currency holdings
    """

    @staticmethod
    def get_original_wallet(user_id: str) -> CommonWalletData:
        """
        Retrieve wallet data without performing any sort of conversion
        """
        data = WalletService._fetch_raw_wallet(user_id)
        return CommonWalletData(**data)

    @staticmethod
    def get_local_currency_wallet(user_id: str) -> ClientWallet:
        """
        Retrieve wallet data and convert
        foreign holdings into user's local currency
        """
        data = WalletService._fetch_raw_wallet(user_id)
        wallet = StoredWallet(**data)

        exchange_rate_client = ExchangeRateClientFactory.get_client(wallet.local_currency)
        converted_balances = {}
        balance_total = 0

        for currency, balance in wallet.balances.items():
            exchange_rate = exchange_rate_client.get_rate(currency)
            converted_balance = round(balance * exchange_rate, 2)
            converted_balances[currency] = converted_balance
            balance_total += converted_balance

        balance_total = round(balance_total, 2)
        return ClientWallet(balances=converted_balances, total=balance_total)

    @staticmethod
    def add_to_wallet(user_id: str, currency_code: str, balance: Decimal):
        """
        Add a given quantity to a user's currency holding
        """
        if balance > 0:
            WalletService._modify_balance(user_id, currency_code, balance)
        else:
            raise ValueError("balance value should be positive")

    @staticmethod
    def subtract_from_wallet(user_id: str, currency_code: str, balance: Decimal):
        """
        Remove a given quantity from a user's currency holding
        """
        if balance > 0:
            balance = balance * -1
            WalletService._modify_balance(user_id, currency_code, balance)
        else:
            raise ValueError("balance value should be positive")

    @staticmethod
    def _modify_balance(user_id: str, currency_code: str, balance: Decimal):
        """
        Helper function that will directly modify a user's currency holding
        """
        query_args = {
            "Key": {
                'user_id': user_id
            },
            # ADD will also subtract if we pass a negative number
            "UpdateExpression": "ADD balances.#currency :balVal",
            "ExpressionAttributeNames": {
                '#currency': currency_code,
            },
            "ExpressionAttributeValues": {
                ':balVal': balance,
            },
        }

        # We should not be able to subtract from the balance
        # in a way that would cause it to become negative...
        if balance < 0:
            # ...so let's add an update condition to make sure
            # that if we subtract from a currency that the currency holding won't go below zero
            query_args["ExpressionAttributeValues"][":absbalVal"] = abs(balance)
            query_args["ConditionExpression"] = "balances.#currency >= :absbalVal"

        wallets_table.update_item(**query_args)

    @staticmethod
    def _fetch_raw_wallet(user_id: str):
        """
        Retrieves raw wallet information from dynamodb
        """
        wallet_data = wallets_table.get_item(
            Key={
                "user_id": user_id
            },
            ProjectionExpression="balances, local_currency, user_id"
        )

        return wallet_data["Item"]
