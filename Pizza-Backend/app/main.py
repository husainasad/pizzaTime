from fastapi import FastAPI
from app.views import topping_views, pizza_views
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(topping_views.router, prefix="/toppings", tags=["Toppings"])
app.include_router(pizza_views.router, prefix="/pizzas", tags=["Pizzas"])