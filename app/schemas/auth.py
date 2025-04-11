from typing import Optional
from pydantic import BaseModel

class TokenOut(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str 
    
class LoginSchema(BaseModel):
    email: str
    password: str