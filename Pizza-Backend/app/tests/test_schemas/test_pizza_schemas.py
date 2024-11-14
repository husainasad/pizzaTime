import pytest
from pydantic import ValidationError
from app.schemas.pizza_schemas import Pizza, PizzaCreate

def test_pizza_create_schema():
    # Valid input
    pizza = PizzaCreate(name="Pepperoni", toppings=[1, 2])
    assert pizza.name == "Pepperoni"
    assert pizza.toppings == [1, 2]

    # Missing required field
    with pytest.raises(ValidationError):
        PizzaCreate()

    # Incorrect type for toppings
    with pytest.raises(ValidationError):
        PizzaCreate(name="Veggie", toppings="invalid")

def test_pizza_with_default_toppings():
    # Test default value for toppings
    pizza = PizzaCreate(name="Margherita")
    assert pizza.toppings == []

def test_pizza_serialization():
    # Test the orm_mode and serialization
    topping_data = {"id": 1, "name": "Onions"}
    pizza_data = {"id": 1, "name": "Hawaiian", "toppings": [topping_data]}

    pizza = Pizza(**pizza_data)
    assert pizza.id == 1
    assert pizza.name == "Hawaiian"
    assert len(pizza.toppings) == 1
    assert pizza.toppings[0].name == "Onions"
