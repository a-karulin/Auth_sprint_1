import os

from dotenv import load_dotenv
from pydantic import Field, BaseSettings

load_dotenv()


POSTGRES_CONN_STR = os.environ.get('POSTGRES_CONN_STR')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')
BASE_HOST = os.environ.get('BASE_HOST', 'http://127.0.0.1/')
RATE_LIMIT_COUNT = os.environ.get('RATE_LIMIT_COUNT', 1)


class RedisConfig(BaseSettings):
    host: str = Field(env="REDIS_HOST")
    port: int = Field(env="REDIS_PORT")


class GoogleConfig(BaseSettings):
    client_id: str = Field(env="GOOGLE_CLIENT_ID")
    secret: str = Field(env="GOOGLE_SECRET")


class YandexConfig(BaseSettings):
    client_id: str = Field(env="YANDEX_CLIENT_ID")
    secret: str = Field(env="YANDEX_SECRET")


redis_config = RedisConfig()
google_config = GoogleConfig()
yandex_config = YandexConfig()
