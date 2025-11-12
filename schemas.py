from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True


# Cuisine models
class CuisineBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None


class CuisineCreate(CuisineBase):
    pass


class CuisineResponse(CuisineBase):
    id: int

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


class IngredientCreate(IngredientBase):
    pass


class IngredientGroupBase(BaseModel):
    name: Optional[str] = None
    sort_order: Optional[int] = None
    list: List[IngredientBase] = []


class IngredientGroupCreate(IngredientGroupBase):
    pass


class InstructionBase(BaseModel):
    text: str
    image: Optional[str] = None
    step_number: int


class InstructionCreate(InstructionBase):
    pass


class TagBase(BaseModel):
    name: str
    slug: Optional[str] = None


class TagCreate(TagBase):
    pass


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
    category_name: Optional[str] = None  # Исправлено с category
    cuisine_name: Optional[str] = None   # Исправлено с cuisine

    ingredients: List[IngredientGroupCreate] = []  # Исправлено тип
    instructions: List[InstructionCreate] = []     # Исправлено имя поля и тип
    tags: List[TagCreate] = []                     # Исправлено тип


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
    ingredients: List[IngredientResponse] = []  # Исправлено с list

    class Config:
        from_attributes = True


class InstructionResponse(InstructionBase):
    id: int
    recipe_id: int

    class Config:
        from_attributes = True


class TagResponse(TagBase):
    id: int

    class Config:
        from_attributes = True

class RecipeIngredientBase(BaseModel):
    name: Optional[str] = None
    value: Optional[str] = None
    type: Optional[str] = None
    amount: Optional[str] = None
    notes: Optional[str] = None
    sort_order: Optional[int] = None

class RecipeIngredientResponse(RecipeIngredientBase):
    id: int
    recipe_group_id: int
    ingredient_id: Optional[int] = None

    class Config:
        from_attributes = True

class RecipeTagResponse(BaseModel):
    recipe_id: int
    tag_id: int
    tag: Optional["TagResponse"] = None  # Добавь связь с тегом

    class Config:
        from_attributes = True

class RecipeIngredientGroupBase(BaseModel):
    sort_order: Optional[int] = None

class RecipeIngredientGroupResponse(RecipeIngredientGroupBase):
    id: int
    recipe_id: int
    group_id: int
    group: Optional["IngredientGroupResponse"] = None
    ingredients: List[RecipeIngredientResponse] = []

    class Config:
        from_attributes = True

class RecipeResponse(RecipeBase):
    id: int
    category_id: Optional[int] = None
    cuisine_id: Optional[int] = None
    category_name: Optional[str] = None
    cuisine_name: Optional[str] = None
    created_at: datetime

    category_rel: Optional[CategoryResponse] = None
    cuisine_rel: Optional[CuisineResponse] = None
    recipe_ingredient_groups: List[RecipeIngredientGroupResponse] = []
    recipe_tags: List[RecipeTagResponse] = []
    instructions: List[InstructionResponse] = []

    class Config:
        from_attributes = True


class RecipeListResponse(BaseModel):
    id: int
    title: str
    category_name: Optional[str] = None  # Исправлено с category
    cuisine_name: Optional[str] = None   # Исправлено с cuisine
    poster: Optional[str] = None
    difficulty: Optional[str] = None
    cooktime: Optional[str] = None
    vegan: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


# User models
class UserBase(BaseModel):
    name: str
    email: str
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    google_id: Optional[str] = None  # Добавлено отсутствующее поле


class UserResponse(UserBase):
    id: int
    google_id: Optional[str] = None  # Добавлено отсутствующее поле
    created_at: datetime

    class Config:
        from_attributes = True


# Favorite models
class FavoriteBase(BaseModel):
    recipe_id: int


class FavoriteCreate(FavoriteBase):
    pass


class FavoriteResponse(FavoriteBase):
    id: int
    user_id: int
    created_at: datetime
    recipe: Optional[RecipeListResponse] = None  # Добавлено для связи с рецептом

    class Config:
        from_attributes = True