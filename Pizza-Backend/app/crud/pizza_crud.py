from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import pizza_models
from app.schemas import pizza_schemas

def get_pizzas(db: Session):
    return db.query(pizza_models.Pizza).all()

def get_pizza_by_id(db: Session, pizza_id: int):
    return db.get(pizza_models.Pizza, pizza_id)

def create_pizza(db: Session, pizza: pizza_schemas.PizzaCreate):
    try:
        new_pizza = pizza_models.Pizza(name=pizza.name)
        
        if pizza.toppings:
            toppings = db.query(pizza.Topping).filter(pizza.Topping.id.in_(pizza.toppings)).all()
            new_pizza.toppings.extend(toppings)

        db.add(new_pizza)
        db.commit()
        db.refresh(new_pizza)
        return new_pizza
    except IntegrityError:
        db.rollback()
        return None

def update_pizza(db: Session, pizza_id: int, pizza_update: pizza_schemas.PizzaUpdate):
    new_pizza = db.get(pizza_models.Pizza, pizza_id)

    if not new_pizza:
        return None

    if pizza_update.name:
        new_pizza.name = pizza_update.name

    if pizza_update.toppings is not None:
        toppings = db.query(pizza_models.Topping).filter(pizza_models.Topping.id.in_(pizza_update.toppings)).all()
        new_pizza.toppings = toppings

    db.commit()
    db.refresh(new_pizza)
    return new_pizza

def delete_pizza(db: Session, pizza_id: int):
    cur_pizza = db.get(pizza_models.Pizza, pizza_id)

    if cur_pizza:
        db.delete(cur_pizza)
        db.commit()
        return True
    
    return False