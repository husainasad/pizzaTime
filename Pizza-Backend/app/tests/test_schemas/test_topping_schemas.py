import pytest
from pydantic import ValidationError
from app.schemas.topping_schemas import Topping, ToppingCreate, ToppingUpdate

def test_topping_create_schema():
    # Valid input
    topping = ToppingCreate(name="Mushrooms")
    assert topping.name == "Mushrooms"

    # Missing required field
    with pytest.raises(ValidationError):
        ToppingCreate()

    # Incorrect type
    with pytest.raises(ValidationError):
        ToppingCreate(name=123)

def test_topping_update_schema():
    # Valid input
    topping = ToppingUpdate(name="Mushrooms")
    assert topping.name == "Mushrooms"

    # Empty name in update
    topping = ToppingUpdate()
    assert topping.name is None

    # Incorrect type
    with pytest.raises(ValidationError):
        ToppingUpdate(name=123)

def test_topping_serialization():
    topping_data = {"id": 1, "name": "Pepperoni"}
    topping = Topping(**topping_data)

    assert topping.id == 1
    assert topping.name == "Pepperoni"
    assert topping.model_dump() == {"id": 1, "name": "Pepperoni"}