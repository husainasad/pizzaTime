from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from app.schemas.topping_schemas import Topping

class PizzaBase(BaseModel):
    name: str

class PizzaCreate(PizzaBase):
    toppings: List[int] = Field(default_factory=list)

class PizzaUpdate(PizzaBase):
    toppings: Optional[List[int]] = None

class Pizza(PizzaBase):
    id: int
    toppings: List[Topping]

    model_config = ConfigDict(from_attributes=True)