from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query

import models
import schemas
from database import get_db
from pagination import PaginationParams, pagination_params
from services import apply_pagination

router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@router.get(
    "",
    response_model=list[schemas.IngredientResponse]
)
def get_ingredients(
    search: str | None = Query(
        None,
        min_length=1,
        description="Поиск ингредиентов по названию или slug"
    ),
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(pagination_params),
):
    query = db.query(models.Ingredient)

    if search:
        query = query.filter(
            or_(
                models.Ingredient.name.ilike(f"%{search}%"),
                models.Ingredient.slug.ilike(f"%{search}%")
            )
        )

    ingredients = apply_pagination(
        query=query.order_by(models.Ingredient.name),
        limit=pagination.limit,
        offset=pagination.offset,
    ).all()

    return ingredients
