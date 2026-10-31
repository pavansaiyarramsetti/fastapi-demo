from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()
class User(BaseModel):
    id: int
    name: str
    age: int

users =[{
        "name": "John Doe",
        "id": 1,
        "age": 30
    }] 
OPEN_PATHS = {"/docs", "/redoc", "/openapi.json"}
@app.middleware("http")
async def check_api_key(request, call_next):
    api_key = request.headers.get("X-API-Key")
    if request.url.path in OPEN_PATHS:
        return await call_next(request)
    if api_key != "my-secret-api-key":
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})
    return await call_next(request)

@app.get("/welcome")
async def welcome():
    return {"message": "Welcome to the API! here is the change"}

@app.get("/user")
def user_profile():
    return users
@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}



@app.post("/users/")
async def create_user(user: User):
    users.append(user.dict())
    return {"message": "User created successfully", "user": user}