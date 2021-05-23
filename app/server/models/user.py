from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    auth_id: Optional[int]
    wallet: Optional[float]
    

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Judit Hernandez",
                "email": "judith@upc.edu",
                "password": "12345678",
            }
        
        }


class UpdateUserModel(BaseModel):
    fullname: Optional[str]
    email: Optional[str]
    password: Optional[str]
    auth_id: Optional[int]
    wallet: Optional[float]
    

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Judit Hernandez",
                "email": "judith@upc.edu",
                "password": "12345678",
                "wallet": 2.50,
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}