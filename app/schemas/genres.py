from pydantic import BaseModel


class GenreBaseSchema(BaseModel):
    name: str

class GenreCreate(GenreBaseSchema):
    pass

class GenreSchema(GenreBaseSchema):
    id: int
    
    class Config:
        from_attributes = True