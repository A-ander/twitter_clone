from pydantic import BaseModel


class Result(BaseModel):
    result: bool

    class ConfigDict:
        from_attributes = True
