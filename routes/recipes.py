from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud, schemas

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.post("/", response_model=schemas.RecipeResponse)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    # тут должен быть user_id (например, из JWT), пока захардкодим:
    user_id = 1
    return crud.create_recipe(db, recipe, user_id)

@router.get("/", response_model=list[schemas.RecipeResponse])
def list_recipes(db: Session = Depends(get_db)):
    return crud.get_recipes(db)
