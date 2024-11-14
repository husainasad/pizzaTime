from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Table
from sqlalchemy.orm import relationship
from app.database import Base

class Topping(Base):
    __tablename__ = "toppings"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    pizzas = relationship("Pizza", secondary="pizza_toppings", back_populates="toppings")

class Pizza(Base):
    __tablename__ = "pizzas"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    toppings = relationship("Topping", secondary="pizza_toppings", back_populates="pizzas")

pizza_toppings = Table(
    "pizza_toppings",
    Base.metadata,
    Column("pizza_id", Integer, ForeignKey("pizzas.id"), primary_key=True),
    Column("topping_id", Integer, ForeignKey("toppings.id"), primary_key=True)
)