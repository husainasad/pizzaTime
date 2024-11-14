from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[schemas.topping.Topping])
def list_toppings(db: Session = Depends(get_db)):
    return crud.topping.get_toppings(db)

@router.post("/", response_model=schemas.topping.Topping)
def add_topping(topping: schemas.topping.ToppingCreate, db: Session = Depends(get_db)):
    db_topping = crud.topping.create_topping(db, topping)
    if not db_topping:
        raise HTTPException(status_code=400, detail="Failed to create topping")
    return db_topping

@router.put("/{topping_id}", response_model=schemas.topping.Topping)
def update_topping(topping_id: int, topping_update: schemas.topping.ToppingUpdate, db: Session = Depends(get_db)):
    db_topping = crud.topping.update_topping(db, topping_id, topping_update)
    if db_topping is None:
        raise HTTPException(status_code=404, detail="Topping not found")
    return db_topping

@router.delete("/{topping_id}", response_model=dict)
def remove_topping(topping_id: int, db: Session = Depends(get_db)):
    db_topping = crud.topping.get_topping_by_id(db, topping_id)
    if not db_topping:
        raise HTTPException(status_code=404, detail="Topping not found")

    if not crud.topping.delete_topping(db, topping_id):
        raise HTTPException(status_code=500, detail="Failed to delete topping")
    return {"detail": "Topping deleted"}