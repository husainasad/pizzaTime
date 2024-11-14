import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import pizza_models
from app.database import engine
from sqlalchemy.orm import Session

# Create a TestClient instance to interact with FastAPI
client = TestClient(app)

# Setup the database for testing
@pytest.fixture(scope="function")
def db():
    # Create a new database session for each test
    pizza_models.Base.metadata.create_all(bind=engine)
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.rollback()
        db.close()
        pizza_models.Base.metadata.drop_all(bind=engine)
        pizza_models.Base.metadata.create_all(bind=engine)

# Test for listing pizzas
def test_list_pizzas(db):
    # Add pizzas to the database
    pizza_1 = pizza_models.Pizza(name="Margherita")
    pizza_2 = pizza_models.Pizza(name="Pepperoni")
    db.add(pizza_1)
    db.add(pizza_2)
    db.commit()

    # Send a GET request to list pizzas
    response = client.get("/pizzas/")
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Check if the correct pizzas are returned
    pizzas = response.json()
    assert len(pizzas) == 2
    assert pizzas[0]["name"] == "Margherita"
    assert pizzas[1]["name"] == "Pepperoni"

# Test for creating a pizza
def test_create_pizza(db):
    pizza_data = {"name": "Cheese Pizza"}

    # Send a POST request to create a pizza
    response = client.post("/pizzas/", json=pizza_data)
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Check if the pizza was created correctly
    pizza = response.json()
    assert pizza["name"] == "Cheese Pizza"
    
    # Attempt to create a pizza with a duplicate name
    duplicate_pizza_data = {"name": "Cheese Pizza"}
    response = client.post("/pizzas/", json=duplicate_pizza_data)
    assert response.status_code == 400

# Test for updating a pizza
def test_update_pizza(db):
    # Add a pizza to the database
    pizza = pizza_models.Pizza(name="Olives Pizza")
    db.add(pizza)
    db.commit()

    # Send a PUT request to update the pizza
    updated_data = {"name": "Green Olives Pizza"}
    response = client.put(f"/pizzas/{pizza.id}", json=updated_data)
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Check if the pizza was updated correctly
    updated_pizza = response.json()
    assert updated_pizza["name"] == "Green Olives Pizza"

    # Attempt to update a non-existing pizza
    non_existing_update = {"name": "New Pizza"}
    response = client.put("/pizzas/999", json=non_existing_update)
    assert response.status_code == 404

# Test for deleting a pizza
def test_delete_pizza(db):
    # Add a pizza to the database
    pizza = pizza_models.Pizza(name="Onions Pizza")
    db.add(pizza)
    db.commit()

    # Send a DELETE request to delete the pizza
    response = client.delete(f"/pizzas/{pizza.id}")
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Check if the pizza was deleted
    assert response.json() == {"detail": "Pizza deleted"}

    # Test: Attempt to delete a non-existing pizza
    response = client.delete("/pizzas/999")
    assert response.status_code == 404