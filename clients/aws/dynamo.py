import boto3

from settings import api_settings

dynamo_client = boto3.client("dynamodb")
dynamo_resource = boto3.resource("dynamodb")
wallets_table = dynamo_resource.Table(api_settings.wallets_table_name)
users_table = dynamo_resource.Table(api_settings.users_table_name)