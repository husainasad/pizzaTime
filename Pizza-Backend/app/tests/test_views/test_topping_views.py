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

# Test for listing toppings
def test_list_toppings(db):
    # Add toppings to the database
    topping_1 = pizza_models.Topping(name="Mushrooms")
    topping_2 = pizza_models.Topping(name="Pepperoni")
    db.add(topping_1)
    db.add(topping_2)
    db.commit()

    # Send a GET request to list toppings
    response = client.get("/toppings/")
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Check if the correct toppings are returned
    toppings = response.json()
    assert len(toppings) == 2
    assert toppings[0]["name"] == "Mushrooms"
    assert toppings[1]["name"] == "Pepperoni"

# Test for creating a topping
def test_create_topping(db):
    topping_data = {"name": "Cheese"}

    # Send a POST request to create a topping
    response = client.post("/toppings/", json=topping_data)
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Check if the topping was created correctly
    topping = response.json()
    assert topping["name"] == "Cheese"
    
    # Attempt to create a duplicate topping
    duplicate_topping_data = {"name": "Cheese"}
    response = client.post("/toppings/", json=duplicate_topping_data)
    assert response.status_code == 400

# Test for updating a topping
def test_update_topping(db):
    # Add a topping to the database
    topping_1 = pizza_models.Topping(name="Olives")
    db.add(topping_1)
    db.commit()

    # Send a PUT request to update the topping
    updated_data = {"name": "Green Olives"}
    response = client.put(f"/toppings/{topping_1.id}", json=updated_data)
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Check if the topping was updated correctly
    topping = response.json()
    assert topping["name"] == "Green Olives"

    # Attempt to update a non-existing topping
    non_existing_update = {"name": "New Topping"}
    response = client.put("/toppings/999", json=non_existing_update)
    assert response.status_code == 404

# Test for deleting a topping
def test_delete_topping(db):
    # Add a topping to the database
    topping_1 = pizza_models.Topping(name="Onions")
    db.add(topping_1)
    db.commit()

    # Send a DELETE request to delete the topping
    response = client.delete(f"/toppings/{topping_1.id}")
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Check if the topping was deleted
    assert response.json() == {"detail": "Topping deleted"}

    # Attempt to delete a non-existing topping
    response = client.delete("/toppings/999")
    assert response.status_code == 404