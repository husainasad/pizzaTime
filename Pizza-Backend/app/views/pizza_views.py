from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import pizza_crud
from app.schemas import pizza_schemas
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[pizza_schemas.Pizza])
def list_pizzas(db: Session = Depends(get_db)):
    return pizza_crud.get_pizzas(db)

@router.post("/", response_model=pizza_schemas.Pizza)
def add_pizza(pizza_create: pizza_schemas.PizzaCreate, db: Session = Depends(get_db)):
    db_pizza = pizza_crud.create_pizza(db, pizza_create)
    if not db_pizza:
        raise HTTPException(status_code=400, detail="Failed to create Pizza")
    return db_pizza

@router.put("/{pizza_id}", response_model=pizza_schemas.Pizza)
def update_pizza(pizza_id: int, pizza_update: pizza_schemas.PizzaUpdate, db: Session = Depends(get_db)):
    updated_pizza = pizza_crud.update_pizza(db, pizza_id=pizza_id, pizza_update=pizza_update)
    
    if not updated_pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")

    return updated_pizza

@router.delete("/{pizza_id}", response_model=dict)
def remove_pizza(pizza_id: int, db: Session = Depends(get_db)):
    db_pizza = pizza_crud.get_pizza_by_id(db, pizza_id)
    if not db_pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")
    if not pizza_crud.delete_pizza(db, pizza_id):
        raise HTTPException(status_code=500, detail="Failed to delete pizza")
    return {"detail": "Pizza deleted"}