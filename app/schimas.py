import re
from typing import Optional
from pydantic import BaseModel, Field, EmailStr,validator
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId,alias="_id")
    first_name: str = Field(...)
    last_name: str = Field(...)
    phone_number: str = Field(...,regex="^(\\+98|0)?9\\d{9}$")
    email: EmailStr = Field(...)
    password: str = Field(...)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        



class UserLightIn(BaseModel):
    phone_number: str = Field(..., regex="^(\\+98|0)?9\\d{9}$")
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserLighOut(BaseModel):
    phone_number: str= Field(..., regex="^(\\+98|0)?9\\d{9}$")
    verified: bool = False
    email: EmailStr 

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
