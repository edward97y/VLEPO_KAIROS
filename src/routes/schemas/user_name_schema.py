from pydantic import BaseModel

class UserNameSchema(BaseModel):
    full_name: str