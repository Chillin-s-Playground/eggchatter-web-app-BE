import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


def _getenv(name: str, default: str = None) -> str | None:
    value = os.getenv(name, default)
    return value


class Configs(BaseSettings):

    # 공통 엔진
    DB_ENGINE: str = _getenv("DB_ENGINE")
    # 실제 DB
    DB_USER: str = _getenv("DB_USER")
    DB_PASSWORD: str = _getenv("DB_PASSWORD")
    DB_HOST: str = _getenv("DB_HOST")
    DB_PORT: str = _getenv("DB_PORT")
    DATA_BASE: str = _getenv("DATA_BASE")
    # 테스트용 DB
    TEST_DB_USER: str = _getenv("DB_USER")
    TEST_DB_PASSWORD: str = _getenv("DB_PASSWORD")
    TEST_DB_HOST: str = _getenv("DB_HOST")
    TEST_DB_PORT: str = _getenv("DB_PORT")
    TEST_DATA_BASE: str = _getenv("DATA_BASE")

    DATABASE_URI: str = (
        "{db_engine}://{user}:{password}@{host}:{port}/{database}".format(
            db_engine=DB_ENGINE,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DATA_BASE,
        )
    )

    TEST_DATABASE_URI: str = (
        "{db_engine}://{user}:{password}@{host}:{port}/{database}".format(
            db_engine=DB_ENGINE,
            user=TEST_DB_USER,
            password=TEST_DB_PASSWORD,
            host=TEST_DB_HOST,
            port=TEST_DB_PORT,
            database=TEST_DATA_BASE,
        )
    )

    # Auth
    KAKAO_API_KEY: str = _getenv("KAKAO_API_KEY")
    KAKAO_REDIRECT_URI: str = _getenv("KAKAO_REDIRECT_URI")

    SECRET_KEY: str = _getenv("SECRET_KEY")
    REFRESH_SECRET_KEY: str = _getenv("REFRESH_SECRET_KEY")
    ALGORITHM: str = _getenv("ALGORITHM")


configs = Configs()
