from pydantic import BaseModel


class MediaSchema(BaseModel):
    file: str
    type: str

    class Config:
        from_attributes = True
