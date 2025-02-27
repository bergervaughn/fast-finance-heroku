from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from userinfo import User, Role, Status

app = FastAPI()

db: List[User] = [
    User(
        id="testAdmin",
        hashed_pass="temp",
        # email is default for now so this test user can receive emails
        role = Role.admin,
        status=True,
        first_name="Dave",
        last_name="Administrator"
    ),
    User(
        id="sampleAccountant",
        hashed_pass="temp",
        role=Role.accountant,
        status=True,
        first_name="John",
        last_name="Accounting"
    )
]
# adding a comment here

class Request(BaseModel):
    type: str = None
    req: str = None

@app.get("/")
async def root():
    return {"Greeting": "Hello team. I have successfully hosted my API through ngrok. I am on a roll tonight."}

@app.get("/users")
async def fetch_users():
    return db

@app.post("/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}
#weird shit going on tonight

@app.put("/users/update")
async def update_user(user: User):
    for u in db:
        if user.id == u.id:
            if user.hashed_pass is not None:
                u.hashed_pass = user.hashed_pass
            if user.email is not None:
                u.email = user.email
            if user.status is not None:
                u.status = user.status
            if user.first_name is not None:
                u.first_name = user.first_name
            if user.last_name is not None:
                u.last_name = user.last_name
            return {f"User with ID {user.id} updated successfully."}
    raise HTTPException(
        status_code=404,
        detail=f"User with ID: {user.id} does not exist."
    )