from pydantic import BaseModel


class TODOCreate(BaseModel):
    desc: str
    completed: bool


class TODOUpdate(TODOCreate):
    id: int

    class Config:
        orm_mode = True
