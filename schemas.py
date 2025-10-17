from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: str
    avatar_url: str | None = None

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class RecipeBase(BaseModel):
    title: str
    description: str
    image_url: str

class RecipeCreate(RecipeBase):
    pass

class RecipeResponse(RecipeBase):
    id: int
    created_at: datetime
    author: UserResponse | None

    class Config:
        from_attributes = True

class KukingCategoryResponse(BaseModel):
    id_category: int
    category_name: str

    class Config:
        from_attributes = True


class KukingReceptResponse(BaseModel):
    id_recepts: int
    recept_name: str
    recept_sostav: str | None = None
    recept_instuction: str
    podcategory: str
    recept_category: int

    class Config:
        from_attributes = True

class FavoriteResponse(BaseModel):
    id: int
    recipe: RecipeResponse
    created_at: datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True