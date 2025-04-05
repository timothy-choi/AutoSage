from fastapi import FastAPI, HTTPException, Depends, Request, Response
from pydantic import BaseModel, EmailStr, Field, constr
import httpx
import bcrypt
import redis
import os
import json
import uuid
from datetime import timedelta

app = FastAPI()

SECRET_KEY = os.urandom(24)

try:
    redis_client = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)
except Exception as e:
    raise RuntimeError(f"Failed to connect to Redis: {str(e)}")

def has_all_criteria(s: str) -> bool:
    return (
        any(c.isupper() for c in s) and
        any(c.islower() for c in s) and
        any(c.isdigit() for c in s) and
        any(c in "!@#$%^&*()_+-=[]{}|;:',.<>?/" for c in s)
    )

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=10, max_length=20)
    email: EmailStr
    password: str
    retype_password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class ChangeUsernameRequest(BaseModel):
    curr_username: str
    changed_username: str

class ChangePasswordRequest(BaseModel):
    changed_password: str
    retyped_password: str

async def get_session(request: Request):
    try:
        session_id = request.cookies.get("session_id")
        if session_id and redis_client.exists(session_id):
            return json.loads(redis_client.get(session_id))
        return None
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail=f"Session handling error: {str(e)}")

@app.post("/UserAuthProcess/Register")
async def register_user_auth(req: RegisterRequest):
    try:
        async with httpx.AsyncClient() as client:
            username_check = await client.get(f"http://localhost:5000/UserAuth/username/{req.username}")
            if username_check.status_code == 200:
                raise HTTPException(status_code=400, detail="Username already exists")

            email_check = await client.get(f"http://localhost:5000/UserAuth/email/{req.email}")
            if email_check.status_code == 200:
                raise HTTPException(status_code=400, detail="Email already exists")

            if req.password != req.retype_password or not has_all_criteria(req.password):
                raise HTTPException(status_code=400, detail="Invalid password or mismatch")

            hashed_salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(req.password.encode(), hashed_salt).decode()

            user_data = req.dict()
            user_data["password"] = hashed_password
            user_data["hash_value"] = hashed_salt.decode()

            response = await client.post("http://localhost:5000/UserAuth/", json=user_data)

            if response.status_code != 201:
                raise HTTPException(status_code=400, detail="Registration failed")

            return {"userAuthAccount": response.json()}
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"External API error: {str(e)}")

@app.get("/UserAuthProcess/LoggedIn")
async def is_logged_in(session: dict = Depends(get_session)):
    if not session:
        raise HTTPException(status_code=401, detail="Not logged in")
    return {"logged_in": True, "user": session}

@app.post("/UserAuthProcess/Login")
async def login_user(req: LoginRequest, response: Response):
    try:
        async with httpx.AsyncClient() as client:
            user_check = await client.get(f"http://localhost:5000/UserAuth/username/{req.username}")
            if user_check.status_code != 200:
                raise HTTPException(status_code=404, detail="User not found")

            user_data = user_check.json()

            if not bcrypt.checkpw(req.password.encode(), user_data["hashed_password"].encode()):
                raise HTTPException(status_code=401, detail="Invalid credentials")

            session_id = uuid.uuid4().hex
            session_data = {"username": req.username, "user_id": user_data["user_id"]}

            redis_client.setex(session_id, timedelta(days=1), json.dumps(session_data))
            response.set_cookie(key="session_id", value=session_id, httponly=True, secure=True, samesite="Lax")

            return {"message": "Login successful", "username": req.username}
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"External API error: {str(e)}")
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail=f"Session handling error: {str(e)}")

@app.post("/UserAuthProcess/Logout")
async def logout_user(request: Request, response: Response):
    try:
        session_id = request.cookies.get("session_id")
        if not session_id or not redis_client.exists(session_id):
            raise HTTPException(status_code=401, detail="Unauthorized user")

        redis_client.delete(session_id)
        response.delete_cookie("session_id")

        return {"message": "Logout successful"}
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail=f"Session handling error: {str(e)}")

@app.put("/UserAuthProcess/Username")
async def change_username(req: ChangeUsernameRequest):
    try:
        async with httpx.AsyncClient() as client:
            res1 = await client.put(f"http://localhost:5000/UserAuth/username/{req.curr_username}/{req.changed_username}")
            res2 = await client.put(f"http://localhost:5000/User/username/{req.curr_username}/{req.changed_username}")

            if res1.status_code != 200 or res2.status_code != 200:
                raise HTTPException(status_code=400, detail="Could not change username")

            return {"status": "successful"}
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"External API error: {str(e)}")

@app.put("/UserAuthProcess/Password/{user_auth_id}")
async def change_password(user_auth_id: uuid.UUID, req: ChangePasswordRequest):
    try:
        if req.changed_password != req.retyped_password or not has_all_criteria(req.changed_password):
            raise HTTPException(status_code=400, detail="Invalid password or mismatch")

        hashed_salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(req.changed_password.encode(), hashed_salt).decode()

        async with httpx.AsyncClient() as client:
            res = await client.put(f"http://localhost:5000/UserAuth/password/{user_auth_id}", json={
                "password": hashed_password,
                "hash_value": hashed_salt.decode()
            })

            if res.status_code != 200:
                raise HTTPException(status_code=400, detail="Could not change password")

        return {"status": "successful"}
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"External API error: {str(e)}")