from pydantic import BaseModel


class ActorBaseSchema(BaseModel):
    name: str

class ActorCreate(ActorBaseSchema):
    pass

class ActorSchema(ActorBaseSchema):
    id: int
    
    class Config:
        from_attributes = True