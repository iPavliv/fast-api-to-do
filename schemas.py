from typing import Optional

from pydantic import BaseModel


class TODOCreate(BaseModel):
    desc: str
    completed: Optional[bool]


class TODORead(TODOCreate):
    id: int
    desc: Optional[str]

    class Config:
        orm_mode = True


class TODOUpdate(TODOCreate):
    desc: Optional[str]

    class Config:
        orm_mode = True
