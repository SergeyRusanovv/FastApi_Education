from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import List, Dict, Union, Optional

from auth.base_config import auth_backend, fastapi_users, current_user
from auth.schemas import UserRead, UserCreate
from redis import asyncio as aioredis

from config import REDIS_HOST, REDIS_PORT
from operations.router import router as router_operation
from tasks.router import router as tasks_router
from pages.router import router as pages_router
from chat.router import router as chats_router


app = FastAPI(title="My beautiful app")
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(
	fastapi_users.get_auth_router(auth_backend),
	prefix="/auth/jwt",
	tags=["auth"],
)

app.include_router(
	fastapi_users.get_register_router(UserRead, UserCreate),
	prefix="/auth",
	tags=["auth"],
)

app.include_router(router_operation)
app.include_router(tasks_router)
app.include_router(pages_router)
app.include_router(chats_router)


origins = [
	"http://localhost.tiangolo.com",
	"https://localhost.tiangolo.com",
	"http://localhost",
	"http://localhost:8080",
]


@app.on_event("startup")
async def startup():
	redis = aioredis.from_url(
		f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf-8", decode_responses=True
	)
	FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
	return JSONResponse(
		status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
		content=jsonable_encoder({"detail": exc.errors()}),
	)


app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
	allow_headers=[
		"Content-Type",
		"Set-Cookie",
		"Access-Control-Allow-Headers",
		"Access-Control-Allow-Origin",
		"Authorization",
	],
)


fake_users: List[Dict[str, Union[int, str]]] = [
	{"id": 1, "role": "admin", "name": "Bob"},
	{"id": 2, "role": "investor", "name": "John"},
	{
		"id": 3,
		"role": "trader",
		"name": "Matt",
		"degree": [
			{"id": 1, "created_at": "2022-12-05 10:37:22", "type_degree": "expert"},
		],
	},
]

fake_traders: List[Dict[str, Union[str, int]]] = [
	{
		"id": 1,
		"user_id": 1,
		"currency": "BTC",
		"side": "buy",
		"price": 123,
		"amount": 2.23,
	},
	{
		"id": 2,
		"user_id": 1,
		"currency": "BTC",
		"side": "sell",
		"price": 129,
		"amount": 2.50,
	},
]


@app.get("/")
async def hello():
	return {"Hello": "World"}


class DegreeType(Enum):
	newbie = "newbie"
	expert = "expert"


class Degree(BaseModel):
	id: int
	created_at: datetime
	type_degree: str


class User(BaseModel):
	id: int
	role: str
	name: str
	degree: Optional[List[Degree]] = []


@app.get("/users/{user_id}", response_model=List[User])
async def get_user(user_id: int):
	return [user for user in fake_users if user.get("id") == user_id]


@app.get("/trades")
async def get_trades(limit: int = 1, offset: int = 0):
	return fake_traders[offset:][:limit]


@app.post("/users/{user_id}")
async def change_user_name(user_id: int, new_name: str):
	current_user = list(filter(lambda user: user.get("id") == user_id, fake_users))[0]
	current_user["name"] = new_name
	return {"status": 200, "data": current_user}


class Trade(BaseModel):
	id: int
	user_id: int
	currency: str = Field(max_length=5)
	side: str
	price: float = Field(ge=0)
	amount: float


@app.post("/trades")
async def add_trades(trades: List[Trade]):
	fake_traders.extend(trades)
	return {"status": 201, "info": "Done", "data": fake_traders}


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
	return f"Hello, {user.email}"


@app.get("/unprotected-route")
def unprotected_route():
	return "Hello, anonym"
