from pydantic import BaseModel, ValidationError
from pydantic import ConfigDict


class User(BaseModel):
    id: int
    name: str

class TagSchema(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    description: str | None


class TagModelSchema(TagSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    
        
class NotFoundResponse(BaseModel):
    message: str