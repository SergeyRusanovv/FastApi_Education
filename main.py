from fastapi import FastAPI
from typing import List, Dict, Union


app = FastAPI(
    title="My beautiful app"
)


fake_users: List[Dict[str, Union[int, str]]] = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "investor", "name": "John"},
    {"id": 3, "role": "trader", "name": "Matt"}
]

fake_traders: List[Dict[str, Union[str,  int]]] = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.23},
    {"id": 2, "user_id": 1, "currency": "BTC", "side": "sell", "price": 129, "amount": 2.50},

]


@app.get("/")
async def hello():
    return {"Hello": "World"}


@app.get("/users/{user_id}")
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
