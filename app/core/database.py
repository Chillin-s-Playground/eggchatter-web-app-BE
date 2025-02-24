from contextlib import asynccontextmanager
from typing import AsyncGenerator

from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database as MongoDatabase

from app.core.config import MONGO_NAME, MONGO_PASSWORD, MONGO_URI, MONGO_USER
from app.models.chats import Chats
from app.models.easter_egg import EasterEggs
from app.models.users import Users


async def _check_connection():
    """DB 커넥션 테스트"""
    client = AsyncIOMotorClient(
        f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_URI}?authSource={MONGO_USER}"
    )
    client[MONGO_NAME]

    try:
        await client.server_info()
        print("MongoDB 연결 성공")
    except Exception as e:
        print("MongoDB 연결 실패", str(e))


class MongoDB:
    def __init__(self) -> None:
        self._client = AsyncIOMotorClient(
            f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_URI}?authSource={MONGO_USER}"
        )
        self._db = self._client[MONGO_NAME]

    @asynccontextmanager
    async def start_session(self):
        """MongoDB 연결 및 session 관리"""
        session = None
        try:
            session = await self._client.start_session()
            await init_beanie(self._db, document_models=[Users, EasterEggs, Chats])
            yield session
        except Exception as e:
            print(f"Error: {str(e)}")
            raise e
        finally:
            # 트랜잭션이 완료된 후 세션 종료
            if session:
                await session.end_session()
                print("end session")


mongo_client = MongoDB()


async def get_db() -> AsyncGenerator:
    async with mongo_client.start_session() as session:
        db = mongo_client._db
        yield db
