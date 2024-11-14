from fastapi import FastAPI
from app.views import topping, pizza
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(topping.router, prefix="/toppings", tags=["Toppings"])
app.include_router(pizza.router, prefix="/pizzas", tags=["Pizzas"])