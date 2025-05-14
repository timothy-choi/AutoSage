from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from RedisHelper import RedisHelper

app = FastAPI()
redis_helper = RedisHelper()

class KeyValue(BaseModel):
    key: str
    value: str
    expire: int | None = None

class KeyRequest(BaseModel):
    key: str

class HashRequest(BaseModel):
    key: str
    mapping: dict

class ListRequest(BaseModel):
    key: str
    value: str
    left: bool = True

@app.post("/redis/set")
def set_value(data: KeyValue):
    redis_helper.set_value(data.key, data.value, ex=data.expire)
    return {"message": f"Key '{data.key}' set successfully."}

@app.post("/redis/get")
def get_value(data: KeyRequest):
    value = redis_helper.get_value(data.key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": data.key, "value": value}

@app.delete("/redis/delete")
def delete_key(data: KeyRequest):
    deleted = redis_helper.delete_key(data.key)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"message": f"Key '{data.key}' deleted."}

@app.post("/redis/exists")
def key_exists(data: KeyRequest):
    exists = redis_helper.key_exists(data.key)
    return {"exists": exists}

@app.post("/redis/set_hash")
def set_hash(data: HashRequest):
    redis_helper.set_hash(data.key, data.mapping)
    return {"message": f"Hash '{data.key}' set."}

@app.post("/redis/get_hash")
def get_hash(data: KeyRequest):
    return {"key": data.key, "value": redis_helper.get_hash(data.key)}

@app.post("/redis/push_list")
def push_to_list(data: ListRequest):
    redis_helper.push_to_list(data.key, data.value, left=data.left)
    return {"message": f"Pushed to list '{data.key}'."}

@app.post("/redis/pop_list")
def pop_from_list(data: ListRequest):
    value = redis_helper.pop_from_list(data.key, left=data.left)
    if value is None:
        raise HTTPException(status_code=404, detail="List is empty or key doesn't exist")
    return {"value": value}
