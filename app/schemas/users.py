from pydantic import BaseModel
from pydantic.networks import EmailStr

from app.schemas.actors import ActorSchema
from app.schemas.genres import GenreSchema


class UserBaseSchema(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBaseSchema):
    password: str

class UserSchema(UserBaseSchema):
    id: int
    
    class Config:
        from_attributes = True

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    favorite_genres: list[GenreSchema]
    favorite_actors: list[ActorSchema]

    class Config:
        orm_mode = True