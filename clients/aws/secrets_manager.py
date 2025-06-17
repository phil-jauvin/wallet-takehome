import boto3

from settings import api_settings


# Since there isn't a very good way of running
# a standalone AWS secrets manager locally I've written a mock
# class to imitate the functionality when running locally.
# For the sake of simplicity I didn't rely on a tool like Localstack in this case.

class MockedSecretsManager:

    _mocked_secrets = {
        api_settings.jwt_secret_key_name: "DUMMYSECRETKEYFORTESTING"
    }

    def get_secret_value(self, SecretId):
        return {
            "SecretString": self._mocked_secrets[SecretId]
        }


if api_settings.environment == "LOCAL":
    secrets_client = MockedSecretsManager()
else:
    secrets_client = boto3.client("secretsmanager")







