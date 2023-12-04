from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

# Pydantic model for request & response


class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id: int
    email:EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
class LocationCreate(BaseModel):
    longitude: float
    latitude: float
    name: str
    description: str
    created_by: str




class LocationResponse(LocationCreate):
    locationid:int
    created_at: datetime
    owner_id:int
    
    class Config:
        orm_mode = True
    
    



class Token(BaseModel):
    access_token : str
    token_type : str  

class TokenData(BaseModel):
    id: Optional[str] = None

