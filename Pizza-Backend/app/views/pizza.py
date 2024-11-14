from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[schemas.pizza.Pizza])
def list_pizzas(db: Session = Depends(get_db)):
    return crud.pizza.get_pizzas(db)

@router.post("/", response_model=schemas.pizza.Pizza)
def add_pizza(pizza_create: schemas.pizza.PizzaCreate, db: Session = Depends(get_db)):
    db_pizza = crud.pizza.create_pizza(db, pizza_create)
    if not db_pizza:
        raise HTTPException(status_code=400, detail="Failed to create Pizza")
    return db_pizza

@router.put("/{pizza_id}", response_model=schemas.pizza.Pizza)
def update_pizza(pizza_id: int, pizza_update: schemas.pizza.PizzaUpdate, db: Session = Depends(get_db)):
    updated_pizza = crud.pizza.update_pizza(db, pizza_id=pizza_id, pizza_update=pizza_update)
    
    if not updated_pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")

    return updated_pizza

@router.delete("/{pizza_id}", response_model=dict)
def remove_pizza(pizza_id: int, db: Session = Depends(get_db)):
    db_pizza = crud.pizza.get_pizza_by_id(db, pizza_id)
    if not db_pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")
    if not crud.pizza.delete_pizza(db, pizza_id):
        raise HTTPException(status_code=500, detail="Failed to delete pizza")
    return {"detail": "Pizza deleted"}