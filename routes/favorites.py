from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud, schemas

router = APIRouter(prefix="/favorites", tags=["favorites"])

@router.post("/{recipe_id}", response_model=schemas.FavoriteResponse)
def add_to_favorites(recipe_id: int, db: Session = Depends(get_db)):
    user_id = 1  # временно
    return crud.add_favorite(db, user_id, recipe_id)

@router.get("/", response_model=list[schemas.FavoriteResponse])
def list_favorites(db: Session = Depends(get_db)):
    user_id = 1
    return crud.get_favorites(db, user_id)