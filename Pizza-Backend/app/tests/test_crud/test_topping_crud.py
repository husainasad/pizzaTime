import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import pizza_models
from app.crud import topping_crud
from app.schemas import topping_schemas


# Create a test database engine and session
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the test database
pizza_models.Base.metadata.create_all(bind=engine)

# Fixture to create a new database session for each test
@pytest.fixture(scope="function")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
        pizza_models.Base.metadata.drop_all(bind=engine)
        pizza_models.Base.metadata.create_all(bind=engine)


# Test for `get_toppings`
def test_get_toppings(db):
    # Create some toppings in the test database
    topping_1 = pizza_models.Topping(name="Mushrooms")
    topping_2 = pizza_models.Topping(name="Pepperoni")
    db.add(topping_1)
    db.add(topping_2)
    db.commit()
    
    # Get all toppings
    toppings = topping_crud.get_toppings(db)
    assert len(toppings) == 2
    assert toppings[0].name == "Mushrooms"
    assert toppings[1].name == "Pepperoni"


# Test for `get_topping_by_id`
def test_get_topping_by_id(db):
    # Create a topping in the test database
    topping_1 = pizza_models.Topping(name="Olives")
    db.add(topping_1)
    db.commit()

    # Retrieve the topping by ID
    fetched_topping = topping_crud.get_topping_by_id(db, topping_1.id)
    assert fetched_topping is not None
    assert fetched_topping.name == "Olives"
    
    # Try to fetch a non-existing topping
    non_existing_topping = topping_crud.get_topping_by_id(db, 999)
    assert non_existing_topping is None


# Test for `create_topping`
def test_create_topping(db):
    topping_data = topping_schemas.ToppingCreate(name="Cheese")
    
    # Create a topping
    created_topping = topping_crud.create_topping(db, topping_data)
    assert created_topping is not None
    assert created_topping.name == "Cheese"
    
    # Attempt to create a topping with a duplicate name (IntegrityError)
    duplicate_topping_data = topping_schemas.ToppingCreate(name="Cheese")
    created_topping = topping_crud.create_topping(db, duplicate_topping_data)
    assert created_topping is None  # Should return None due to IntegrityError


# Test for `update_topping`
def test_update_topping(db):
    # Create a topping in the test database
    topping_1 = pizza_models.Topping(name="Mushrooms")
    db.add(topping_1)
    db.commit()

    topping_update_data = topping_schemas.ToppingUpdate(name="Olives")
    
    # Update the topping
    updated_topping = topping_crud.update_topping(db, topping_1.id, topping_update_data)
    assert updated_topping is not None
    assert updated_topping.name == "Olives"
    
    # Attempt to update a non-existing topping
    non_existing_update = topping_crud.update_topping(db, 999, topping_update_data)
    assert non_existing_update is None


# Test for `delete_topping`
def test_delete_topping(db):
    # Create a topping in the test database
    topping_1 = pizza_models.Topping(name="Onions")
    db.add(topping_1)
    db.commit()

    # Delete the topping
    result = topping_crud.delete_topping(db, topping_1.id)
    assert result is True

    # Attempt to delete a non-existing topping
    result = topping_crud.delete_topping(db, 999)
    assert result is False