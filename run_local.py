import uvicorn

from test.fixtures.create_database_resources import create_users_table, create_wallets_table
from test.fixtures.util import set_fake_aws_credentials

set_fake_aws_credentials()
create_users_table()
create_wallets_table()

if __name__ == "__main__":
        from main import app
        uvicorn.run(app, host="0.0.0.0", port=5500)