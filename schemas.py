from pydantic import BaseModel
from datetime import datetime

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    image: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Cuisine models
class CuisineBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    image: Optional[str] = None


class CuisineCreate(CuisineBase):
    pass


class CuisineResponse(CuisineBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Ingredient models
class IngredientBase(BaseModel):
    name: str
    slug: Optional[str] = None
    notes: Optional[str] = None
    value: Optional[str] = None
    type: Optional[str] = None
    amount: Optional[str] = None
    sort_order: Optional[int] = None


class IngredientGroupBase(BaseModel):
    name: Optional[str] = None
    sort_order: Optional[int] = None
    list: List[IngredientBase] = []


class InstructionBase(BaseModel):
    text: str
    image: Optional[str] = None
    step_number: int


class TagBase(BaseModel):
    name: str
    slug: Optional[str] = None


# Recipe models
class RecipeBase(BaseModel):
    source: Optional[str] = None
    title: str
    description: Optional[str] = None
    note: Optional[str] = None
    poster: Optional[str] = None
    difficulty: Optional[str] = None
    cooktime: Optional[str] = None
    preparetime: Optional[str] = None
    video: Optional[str] = None
    vegan: bool = False


class RecipeCreate(RecipeBase):
    category_id: Optional[int] = None
    cuisine_id: Optional[int] = None
    # Для обратной совместимости
    category: Optional[str] = None
    category_slug: Optional[str] = None
    cuisine: Optional[str] = None
    cuisine_slug: Optional[str] = None

    ingredients: List[IngredientGroupBase] = []
    instruction: List[InstructionBase] = []
    tags: List[TagBase] = []


class RecipeUpdate(BaseModel):
    source: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    note: Optional[str] = None
    category_id: Optional[int] = None
    cuisine_id: Optional[int] = None
    poster: Optional[str] = None
    difficulty: Optional[str] = None
    cooktime: Optional[str] = None
    preparetime: Optional[str] = None
    video: Optional[str] = None
    vegan: Optional[bool] = None


# Response models
class IngredientResponse(IngredientBase):
    id: int
    group_id: int

    class Config:
        from_attributes = True


class IngredientGroupResponse(IngredientGroupBase):
    id: int
    recipe_id: int
    ingredients: List[IngredientResponse] = []

    class Config:
        from_attributes = True


class InstructionResponse(InstructionBase):
    id: int
    recipe_id: int

    class Config:
        from_attributes = True


class TagResponse(TagBase):
    id: int
    recipe_id: int

    class Config:
        from_attributes = True


class RecipeResponse(RecipeBase):
    id: int
    category_id: Optional[int] = None
    cuisine_id: Optional[int] = None
    category: Optional[str] = None
    category_slug: Optional[str] = None
    cuisine: Optional[str] = None
    cuisine_slug: Optional[str] = None
    created_at: datetime

    # Relationships
    category_rel: Optional[CategoryResponse] = None
    cuisine_rel: Optional[CuisineResponse] = None
    ingredient_groups: List[IngredientGroupResponse] = []
    instructions: List[InstructionResponse] = []
    tags: List[TagResponse] = []

    class Config:
        from_attributes = True


class RecipeListResponse(BaseModel):
    id: int
    title: str
    category: Optional[str] = None
    category_slug: Optional[str] = None
    cuisine: Optional[str] = None
    cuisine_slug: Optional[str] = None
    poster: Optional[str] = None
    difficulty: Optional[str] = None
    cooktime: Optional[str] = None
    vegan: bool = False
    created_at: datetime

    class Config:
        from_attributes = True

# User

class UserBase(BaseModel):
    name: str
    email: str
    avatar_url: str | None = None

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True