import os

from dotenv import load_dotenv

load_dotenv()  # .env 파일에서 환경 변수 로드


def _getenv(name: str, default: str = None) -> str | None:
    value = os.getenv(name, default)
    return value


MONGO_URI = _getenv("MONGO_URI")
MONGO_NAME = _getenv("MONGO_NAME")
MONGO_USER = _getenv("MONGO_USER")
MONGO_PASSWORD = _getenv("MONGO_PASSWORD")
