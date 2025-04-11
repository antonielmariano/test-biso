from pydantic import BaseModel


class RatingBaseSchema(BaseModel):
    score: float

class RatingCreate(RatingBaseSchema):
    movie_id: int

class RatingSchema(RatingBaseSchema):
    id: int
    user_id: int
    movie_id: int
    
    class Config:
        from_attributes = True