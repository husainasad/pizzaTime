from pydantic import BaseModel
from typing import List, Optional
from app.schemas.topping import Topping

class PizzaBase(BaseModel):
    name: str

class PizzaCreate(PizzaBase):
    toppings: List[int]

class PizzaUpdate(PizzaBase):
    toppings: Optional[List[int]] = None

class Pizza(PizzaBase):
    id: int
    toppings: List[Topping]

    class Config:
        orm_mode = True