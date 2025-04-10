from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, conint, constr
from typing import Optional

app = FastAPI()

class User(BaseModel):
    username: str
    age: conint(gt=18)  # Age must be greater than 18
    email: EmailStr  # Must be a valid email address
    password: constr(min_length=8, max_length=16)  # Password length between 8 and 16
    phone: Optional[str] = 'Unknown'  # Optional phone number with default value

@app.post("/submit")
async def create_user(user: User):
    return {"status": "success", "data": user.dict()}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error_messages = [{"loc": error["loc"], "msg": error["msg"], "type": error["type"]} for error in errors]
    return JSONResponse(
        status_code=422,
        content={"detail": error_messages, "hint": "Please check your input data for errors."},
    )
