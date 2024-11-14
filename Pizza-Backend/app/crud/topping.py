from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas

def get_toppings(db: Session):
    return db.query(models.pizza.Topping).all()

def get_topping_by_id(db: Session, topping_id: int):
    return db.query(models.pizza.Topping).get(topping_id)

def create_topping(db: Session, topping: schemas.topping.ToppingCreate):
    try:
        new_topping = models.pizza.Topping(name=topping.name)
        db.add(new_topping)
        db.commit()
        db.refresh(new_topping)
        return new_topping
    except IntegrityError:
        db.rollback()
        return None

def update_topping(db: Session, topping_id: int, topping_update: schemas.topping.ToppingUpdate):
    new_topping = db.query(models.pizza.Topping).get(topping_id)

    if not new_topping:
        return None
    
    if topping_update.name:
        new_topping.name = topping_update.name

    db.commit()
    db.refresh(new_topping)

    return new_topping

def delete_topping(db: Session, topping_id: int):
    cur_topping = db.query(models.pizza.Topping).get(topping_id)
    
    if cur_topping:
        db.delete(cur_topping)
        db.commit()
        return True
    
    return False