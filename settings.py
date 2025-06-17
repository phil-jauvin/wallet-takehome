from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    nbp_api_url: str = "https://api.nbp.pl/api"
    nbp_api_conversion_endpoint: str = "exchangerates/rates/c/%s?format=json"
    aws_region: str = "us-east-1"
    cache_ttl: int = 60
    jwt_secret_key_name: str = "JWT_SECRET_KEY"
    environment: str = "LOCAL"
    wallets_table_name: str = "user_wallets"
    users_table_name: str = "user_data"




api_settings = Settings()