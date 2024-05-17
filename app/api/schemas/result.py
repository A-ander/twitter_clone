from pydantic import BaseModel


class Result(BaseModel):
    result: bool

    class Config:
        from_attributes = True
