from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ToppingBase(BaseModel):
    name: str

class ToppingCreate(ToppingBase):
    pass

class ToppingUpdate(ToppingBase):
    name: Optional[str] = None

class Topping(ToppingBase):
    id: int

    model_config = ConfigDict(from_attributes=True)