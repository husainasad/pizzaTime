import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.pizza_models import Base, Pizza, Topping

# Create a testing database engine (using SQLite in-memory)
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Setup fixture for creating the tables and providing a session
@pytest.fixture(scope="function")
def db_session():
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

# Test creating a Topping
def test_create_topping(db_session):
    topping = Topping(name="Mushrooms")
    db_session.add(topping)
    db_session.commit()

    fetched_topping = db_session.query(Topping).filter_by(name="Mushrooms").first()
    assert fetched_topping is not None
    assert fetched_topping.name == "Mushrooms"

# Test creating a Pizza
def test_create_pizza(db_session):
    pizza = Pizza(name="Margherita")
    db_session.add(pizza)
    db_session.commit()

    fetched_pizza = db_session.query(Pizza).filter_by(name="Margherita").first()
    assert fetched_pizza is not None
    assert fetched_pizza.name == "Margherita"

# Test the many-to-many relationship between Pizza and Topping
def test_pizza_topping_relationship(db_session):
    # Create toppings
    cheese = Topping(name="Cheese")
    tomato = Topping(name="Tomato")

    # Create a pizza and add toppings
    pizza = Pizza(name="Cheese Pizza", toppings=[cheese, tomato])

    db_session.add(pizza)
    db_session.commit()

    # Fetch the pizza from the database
    fetched_pizza = db_session.query(Pizza).filter_by(name="Cheese Pizza").first()
    assert fetched_pizza is not None
    assert len(fetched_pizza.toppings) == 2

    topping_names = [topping.name for topping in fetched_pizza.toppings]
    assert "Cheese" in topping_names
    assert "Tomato" in topping_names

# Test unique constraint on topping name
def test_unique_topping_name(db_session):
    topping1 = Topping(name="Pepperoni")
    topping2 = Topping(name="Pepperoni")

    db_session.add(topping1)
    db_session.commit()

    # Adding the second topping should raise an IntegrityError due to the unique constraint
    with pytest.raises(Exception):
        db_session.add(topping2)
        db_session.commit()

# Test unique constraint on pizza name
def test_unique_pizza_name(db_session):
    pizza1 = Pizza(name="Margherita")
    pizza2 = Pizza(name="Margherita")

    db_session.add(pizza1)
    db_session.commit()

    # Adding the second pizza should raise an IntegrityError due to the unique constraint
    with pytest.raises(Exception):
        db_session.add(pizza2)
        db_session.commit()