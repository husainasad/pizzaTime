from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import pizza_models
from app.schemas import topping_schemas

def get_toppings(db: Session):
    return db.query(pizza_models.Topping).all()

def get_topping_by_id(db: Session, topping_id: int):
    return db.get(pizza_models.Topping, topping_id)

def create_topping(db: Session, topping: topping_schemas.ToppingCreate):
    try:
        new_topping = pizza_models.Topping(name=topping.name)
        db.add(new_topping)
        db.commit()
        db.refresh(new_topping)
        return new_topping
    except IntegrityError:
        db.rollback()
        return None

def update_topping(db: Session, topping_id: int, topping_update: topping_schemas.ToppingUpdate):
    new_topping = db.get(pizza_models.Topping, topping_id)

    if not new_topping:
        return None
    
    if topping_update.name:
        new_topping.name = topping_update.name

    db.commit()
    db.refresh(new_topping)

    return new_topping

def delete_topping(db: Session, topping_id: int):
    cur_topping = db.get(pizza_models.Topping, topping_id)
    
    if cur_topping:
        db.delete(cur_topping)
        db.commit()
        return True
    
    return False