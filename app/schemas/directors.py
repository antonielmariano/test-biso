from pydantic import BaseModel

class DirectorBaseSchema(BaseModel):
    name: str

class DirectorCreate(DirectorBaseSchema):
    pass

class DirectorSchema(DirectorBaseSchema):
    id: int
    
    class Config:
        from_attributes = True