import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import pizza_models
from app.crud import pizza_crud
from app.schemas import pizza_schemas


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


# Test for `get_pizzas`
def test_get_pizzas(db):
    # Create some pizzas in the test database
    pizza_1 = pizza_models.Pizza(name="Margherita")
    pizza_2 = pizza_models.Pizza(name="Pepperoni")
    db.add(pizza_1)
    db.add(pizza_2)
    db.commit()

    # Get all pizzas
    pizzas = pizza_crud.get_pizzas(db)
    assert len(pizzas) == 2
    assert pizzas[0].name == "Margherita"
    assert pizzas[1].name == "Pepperoni"


# Test for `get_pizza_by_id`
def test_get_pizza_by_id(db):
    # Create a pizza in the test database
    pizza_1 = pizza_models.Pizza(name="Hawaiian")
    db.add(pizza_1)
    db.commit()

    # Retrieve the pizza by ID
    fetched_pizza = pizza_crud.get_pizza_by_id(db, pizza_1.id)
    assert fetched_pizza is not None
    assert fetched_pizza.name == "Hawaiian"

    # Try to fetch a non-existing pizza
    non_existing_pizza = pizza_crud.get_pizza_by_id(db, 999)
    assert non_existing_pizza is None


# Test for `create_pizza`
def test_create_pizza(db):
    pizza_data = pizza_schemas.PizzaCreate(name="Veggie Supreme", toppings=[])

    # Create a pizza
    created_pizza = pizza_crud.create_pizza(db, pizza_data)
    assert created_pizza is not None
    assert created_pizza.name == "Veggie Supreme"

    # Attempt to create a pizza with a duplicate name
    duplicate_pizza_data = pizza_schemas.PizzaCreate(name="Veggie Supreme", toppings=[])
    created_pizza = pizza_crud.create_pizza(db, duplicate_pizza_data)
    assert created_pizza is None

# Test for `update_pizza`
def test_update_pizza(db):
    # Create a pizza in the test database
    pizza_1 = pizza_models.Pizza(name="Cheese Pizza")
    db.add(pizza_1)
    db.commit()

    pizza_update_data = pizza_schemas.PizzaUpdate(name="Cheese Pizza Deluxe", toppings=[])

    # Update the pizza name
    updated_pizza = pizza_crud.update_pizza(db, pizza_1.id, pizza_update_data)
    assert updated_pizza is not None
    assert updated_pizza.name == "Cheese Pizza Deluxe"

    # Attempt to update a non-existing pizza
    non_existing_update = pizza_crud.update_pizza(db, 999, pizza_update_data)
    assert non_existing_update is None


# Test for `delete_pizza`
def test_delete_pizza(db):
    # Create a pizza in the test database
    pizza_1 = pizza_models.Pizza(name="BBQ Chicken")
    db.add(pizza_1)
    db.commit()

    # Delete the pizza
    result = pizza_crud.delete_pizza(db, pizza_1.id)
    assert result is True

    # Attempt to delete a non-existing pizza
    result = pizza_crud.delete_pizza(db, 999)
    assert result is False