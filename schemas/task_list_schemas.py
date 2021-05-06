from typing import Optional, List

from pydantic import BaseModel

from schemas.task_schemas import TODORead


class TListCreate(BaseModel):
    desc: Optional[str]


class TListRead(TListCreate):
    id: int
    tasks: List[TODORead]

    class Config:
        orm_mode = True


class TListUpdate(TListCreate):
    desc: str

    class Config:
        orm_mode = True
