from pydantic import BaseModel
from typing import Optional

class ToppingBase(BaseModel):
    name: str

class ToppingCreate(ToppingBase):
    pass

class ToppingUpdate(ToppingBase):
    name: Optional[str]

class Topping(ToppingBase):
    id: int

    class Config:
        orm_mode = True