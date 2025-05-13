from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.exceptions import (
    DuplicatedErrorException,
    UnknownErrorException,
    exception_handler,
)
from app.routers import auth, easter_egg, users

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Http 엔드포인트
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(easter_egg.router)

app.add_exception_handler(DuplicatedErrorException, exception_handler)
app.add_exception_handler(UnknownErrorException, exception_handler)
