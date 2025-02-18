from motor.motor_asyncio import AsyncIOMotorClient

from app.config import MONGO_NAME, MONGO_PASSWORD, MONGO_URI, MONGO_USER


async def _check_connection():
    """DB 커넥션 테스트"""
    client = AsyncIOMotorClient(
        f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_URI}/{MONGO_NAME}"
    )

    try:
        info = await client.server_info()
        print("MongoDB 연결 성공")
    except Exception as e:
        print("MongoDB 연결 실패")
