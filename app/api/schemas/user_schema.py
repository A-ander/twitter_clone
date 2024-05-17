from pydantic import BaseModel

from app.api.schemas.result import Result


class UserSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserFullSchema(UserSchema):
    followers: list[UserSchema]
    following: list[UserSchema]


class UserResponse(Result):
    user: UserFullSchema
