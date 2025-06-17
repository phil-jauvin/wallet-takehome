import os

import pytest

from test.data.wallets import DEFAULT_WALLET_DATA

from models.wallet import CommonWalletData, ClientWallet

CURRENT_DDB_ENDPOINT = os.environ.get("AWS_ENDPOINT_URL_DYNAMODB")

class TestAPI:

    def setup_class(self):
        if CURRENT_DDB_ENDPOINT:
            del os.environ["AWS_ENDPOINT_URL_DYNAMODB"]

    def teardown_class(self):
        if CURRENT_DDB_ENDPOINT:
            os.environ["AWS_ENDPOINT_URL_DYNAMODB"] = CURRENT_DDB_ENDPOINT

    @pytest.fixture
    def login(self, mocked_aws):
        """
        Performs the login flow and returns
        login information needed for other tests
        """
        res = mocked_aws.post(
            url="/token",
            data={
                "username": "pjauvin",
                "password": "supermariobros",
                "grant_type": "password"
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

        yield res.json()

    def test_login_success(self, mocked_aws, login):
        """
        Check whether the login flow can be done correctly
        """
        response = login
        assert "access_token" in response
        assert response["token_type"] == "bearer"


    def test_login_wrong_password(self, mocked_aws):
        """
        Verify that we aren't able to login if we submit
        the wrong password for our user
        """
        res = mocked_aws.post(
            url="/token",
            data={
                "username": "pjauvin",
                "password": "thisiswrongandshoudfail",
                "grant_type": "password"
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

        response = res.json()

        assert res.status_code == 401
        assert "access_token" not in response


    def test_retrieve_wallet(self, mocked_aws, login):
        """
        Check whether the user's wallet can be
        retrieved correctly
        """
        res = mocked_aws.get(
            url="/wallet",
            headers={'Authorization': f"Bearer {login["access_token"]}"}
        )

        ClientWallet.model_validate(res.json())
        assert res.status_code == 200

    def test_retrieve_wallet_authorisation(self, mocked_aws, login):
        """
        Ensure that a user wallet can
        only be fetched with the correct authorisation
        """
        res = mocked_aws.get(
            url="/wallet",
            headers={'Authorization': f"Bearer yabbadabbadoo"}
        )

        assert res.status_code == 401

    def test_retrieve_wallet_original(self, mocked_aws, login):
        """
        Check whether the user's original wallet
        information can be retrieved correctly
        """
        res = mocked_aws.get(
            url="/wallet/original",
            headers={'Authorization': f"Bearer {login["access_token"]}"}
        )

        CommonWalletData.model_validate(res.json())
        assert res.status_code == 200


    def test_retrieve_wallet_original_authorisation(self, mocked_aws, login):
        """
        Ensure that a user wallet can
        only be fetched with the correct authorisation
        """
        res = mocked_aws.get(
            url="/wallet/original",
            headers={'Authorization': f"Bearer yabbadabbadoo"}
        )

        assert res.status_code == 401

    def test_add_balance(self, mocked_aws, login):
        """
        Ensure that the user can add to a particular
        currency balance
        """
        res = mocked_aws.post(
            url="/wallet/add/JPY/100",
            headers={'Authorization': f"Bearer {login["access_token"]}"}
        )

        assert res.status_code == 200

        res = mocked_aws.get(
            url="/wallet/original",
            headers={'Authorization': f"Bearer {login["access_token"]}"}
        )

        response = res.json()

        target_value = DEFAULT_WALLET_DATA["balances"]["JPY"] + 100

        assert response["balances"]["JPY"] ==  target_value


    def test_add_balance_negative(self, mocked_aws, login):
        """
        Verify that an invalid value can't be
        sent through to the add balance endpoint
        """
        res = mocked_aws.post(
            url="/wallet/add/JPY/-100",
            headers={'Authorization': f"Bearer {login["access_token"]}"}
        )

        assert res.status_code == 422

        res = mocked_aws.get(
            url="/wallet/original",
            headers={'Authorization': f"Bearer {login["access_token"]}"}
        )

        response = res.json()

        target_value = DEFAULT_WALLET_DATA["balances"]["JPY"]

        assert response["balances"]["JPY"] ==  target_value

    def test_add_balance_authorisation(self, mocked_aws, login):
        """
        Ensure that the user can only add to a particular
        currency balance if the correct auth is present
        """
        res = mocked_aws.post(
            url="/wallet/add/JPY/100",
            headers={'Authorization': f"Bearer zooweemama"}
        )

        assert res.status_code == 401

        res = mocked_aws.get(
            url="/wallet/original",
            headers={'Authorization': f"Bearer {login["access_token"]}"}
        )

        response = res.json()

        target_value = DEFAULT_WALLET_DATA["balances"]["JPY"]

        assert response["balances"]["JPY"] ==  target_value

    def test_subtract_balance(self, mocked_aws, login):
        """
        Ensure that the user can subtract from a particular
        currency balance
        """
        res = mocked_aws.post(
            url="/wallet/subtract/USD/1",
            headers={'Authorization': f"Bearer {login["access_token"]}"}
        )

        assert res.status_code == 200

        res = mocked_aws.get(
            url="/wallet/original",
            headers={'Authorization': f"Bearer {login["access_token"]}"}
        )

        response = res.json()

        target_value = DEFAULT_WALLET_DATA["balances"]["USD"] - 1

        assert response["balances"]["USD"] ==  target_value


    def test_subtract_balance_negative(self, mocked_aws, login):
        """
        Verify that an invalid value can't be
        sent through to the subtract balance endpoint
        """
        res = mocked_aws.post(
            url="/wallet/subtract/USD/-1",
            headers={'Authorization': f"Bearer {login["access_token"]}"}
        )

        assert res.status_code == 422

        res = mocked_aws.get(
            url="/wallet/original",
            headers={'Authorization': f"Bearer {login["access_token"]}"}
        )

        response = res.json()

        target_value = DEFAULT_WALLET_DATA["balances"]["USD"]

        assert response["balances"]["USD"] ==  target_value

    def test_subtract_balance_authorisation(self, mocked_aws, login):
        """
        Ensure that the user can only subtract from a particular
        currency balance if the correct auth is present
        """
        res = mocked_aws.post(
            url="/wallet/subtract/USD/1",
            headers={'Authorization': f"Bearer zooweemama"}
        )

        assert res.status_code == 401

        res = mocked_aws.get(
            url="/wallet/original",
            headers={'Authorization': f"Bearer {login["access_token"]}"}
        )

        response = res.json()

        target_value = DEFAULT_WALLET_DATA["balances"]["USD"]

        assert response["balances"]["USD"] ==  target_value


