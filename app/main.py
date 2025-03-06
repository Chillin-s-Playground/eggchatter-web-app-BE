from fastapi import FastAPI

from app.routers import auth, easter_egg, users

app = FastAPI()

# Http 엔드포인트
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(easter_egg.router)
