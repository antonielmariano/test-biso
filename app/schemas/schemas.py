from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    release_year: int
    director_id: int

class MovieCreate(MovieBase):
    genre_ids: List[int]
    actor_ids: List[int]

class Movie(MovieBase):
    id: int
    genres: List["Genre"]
    actors: List["Actor"]
    director: "Director"
    average_rating: Optional[float] = None
    
    class Config:
        from_attributes = True

class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int
    
    class Config:
        from_attributes = True

class ActorBase(BaseModel):
    name: str

class ActorCreate(ActorBase):
    pass

class Actor(ActorBase):
    id: int
    
    class Config:
        from_attributes = True

class DirectorBase(BaseModel):
    name: str

class DirectorCreate(DirectorBase):
    pass

class Director(DirectorBase):
    id: int
    
    class Config:
        from_attributes = True

class RatingBase(BaseModel):
    score: float

class RatingCreate(RatingBase):
    movie_id: int

class Rating(RatingBase):
    id: int
    user_id: int
    movie_id: int
    
    class Config:
        from_attributes = True

# Update forward references
Movie.update_forward_refs() 