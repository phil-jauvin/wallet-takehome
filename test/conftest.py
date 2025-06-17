from fastapi.testclient import TestClient

from test.fixtures.util import set_fake_aws_credentials

from moto import mock_aws

import pytest

from test.fixtures.create_database_resources import create_users_table, create_wallets_table


@pytest.fixture
def aws_credentials():
   set_fake_aws_credentials()

@pytest.fixture()
def mocked_aws(aws_credentials):
    with mock_aws():
        from main import app
        create_users_table()
        create_wallets_table()
        yield TestClient(app)

