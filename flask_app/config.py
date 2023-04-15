import os

from dotenv import load_dotenv
from pydantic import Field, BaseSettings

load_dotenv()


POSTGRES_CONN_STR = os.environ.get('POSTGRES_CONN_STR', 500)


class RedisConfig(BaseSettings):
    host: str = Field(env="REDIS_HOST")
    port: int = Field(env="REDIS_PORT")


redis_config = RedisConfig()