from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str
    followers: list['UserSchema'] = []
    following: list['UserSchema'] = []

    class Config:
        from_attributes = True
