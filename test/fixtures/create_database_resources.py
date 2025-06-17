import boto3
from settings import api_settings

from test.data.users import DEFAULT_USER_RECORD
from test.data.wallets import DEFAULT_WALLET_DATA


def get_db_resources():
    dynamo_client = boto3.client("dynamodb")
    dynamo_resource = boto3.resource("dynamodb")
    tables = dynamo_client.list_tables()["TableNames"]
    return dynamo_client, dynamo_resource, tables

def create_wallets_table():
    dynamo_client, dynamo_resource, tables = get_db_resources()

    if api_settings.wallets_table_name not in tables:
        dynamo_client.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName': 'user_id',
                    'AttributeType': 'S'
                },
            ],
            TableName=api_settings.wallets_table_name,
            KeySchema=[
                {
                    'AttributeName': 'user_id',
                    'KeyType': 'HASH'
                },
            ],
            BillingMode='PAY_PER_REQUEST',
            TableClass='STANDARD'
        )

        wallets_table = dynamo_resource.Table(api_settings.wallets_table_name)

        wallets_table.put_item(Item=DEFAULT_WALLET_DATA)

def create_users_table():
    dynamo_client, dynamo_resource, tables = get_db_resources()

    if api_settings.users_table_name not in tables:

        dynamo_client.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S'
                },
            ],
            TableName=api_settings.users_table_name,
            KeySchema=[
                {
                    'AttributeName': 'username',
                    'KeyType': 'HASH'
                },
            ],
            BillingMode='PAY_PER_REQUEST',
            TableClass='STANDARD'
        )

        users_table = dynamo_resource.Table(api_settings.users_table_name)

        users_table.put_item(Item=DEFAULT_USER_RECORD)
