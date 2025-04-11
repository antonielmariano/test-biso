from pydantic import BaseModel
from typing import List, Optional

from app.schemas.actors import ActorSchema
from app.schemas.directors import DirectorSchema
from app.schemas.genres import GenreSchema
    
class MovieBaseSchema(BaseModel):
    title: str
    description: Optional[str] = None
    release_year: int

class MovieCreate(MovieBaseSchema):
    director_name: str
    genres: List[str]
    actors: List[str]

class MovieSchema(MovieBaseSchema):
    id: int
    genres: List[GenreSchema]
    actors: List[ActorSchema]
    director: Optional[DirectorSchema] = None
    average_rating: Optional[float] = None
    
    class Config:
        from_attributes = True

MovieSchema.update_forward_refs() 