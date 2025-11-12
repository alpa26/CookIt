from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, BigInteger,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    google_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    avatar_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    favorites = relationship("Favorite", back_populates="user")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    slug = Column(String(255), unique=True, index=True)
    description = Column(Text)

    recipes = relationship("Recipe", back_populates="category_rel")


class Cuisine(Base):
    __tablename__ = "cuisines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    slug = Column(String(255), unique=True, index=True)
    description = Column(Text)

    recipes = relationship("Recipe", back_populates="cuisine_rel")


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category_name = Column(String(255))  # Оставляем для обратной совместимости
    title = Column(String(500), nullable=False)
    description = Column(Text)
    note = Column(Text)
    cuisine_id = Column(Integer, ForeignKey("cuisines.id"))
    cuisine_name = Column(String(255))  # Оставляем для обратной совместимости
    poster = Column(Text)
    difficulty = Column(String(100))
    cooktime = Column(String(100))
    preparetime = Column(String(100))
    video = Column(Text)
    vegan = Column(Boolean, default=False)
    rec_json = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    favorited_by = relationship("Favorite", back_populates="recipe")
    category_rel = relationship("Category", back_populates="recipes")
    cuisine_rel = relationship("Cuisine", back_populates="recipes")
    recipe_ingredient_groups = relationship(
        "RecipeIngredientGroup",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )

    recipe_tags = relationship(
        "RecipeTag",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )
    instructions = relationship(
        "Instruction",
        back_populates="recipe",
        cascade="all, delete-orphan",
        foreign_keys="[Instruction.recipe_id]"
    )



class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("ingredient_groups.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    slug = Column(String(255))
    notes = Column(Text)
    value = Column(String(100))
    type = Column(String(100))
    amount = Column(String(100))
    sort_order = Column(Integer)

class Instruction(Base):
    __tablename__ = "instructions"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"))
    text = Column(Text, nullable=False)
    image = Column(Text)
    step_number = Column(Integer)

    recipe = relationship("Recipe", back_populates="instructions")

class RecipeTag(Base):
    __tablename__ = "recipe_tags"

    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)

    recipe = relationship("Recipe", back_populates="recipe_tags")
    tag = relationship("Tag", back_populates="recipe_associations")

class IngredientGroup(Base):
    __tablename__ = "ingredient_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))

    recipe_associations = relationship("RecipeIngredientGroup", back_populates="group")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    parent_name = Column(String(255))
    parent_slug = Column(String(255))

    recipe_associations = relationship("RecipeTag", back_populates="tag")

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="favorites")
    recipe = relationship("Recipe", back_populates="favorited_by")

class RecipeIngredientGroup(Base):
    __tablename__ = "recipe_ingredient_groups"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"))
    group_id = Column(Integer, ForeignKey("ingredient_groups.id", ondelete="CASCADE"))
    sort_order = Column(Integer)

    recipe = relationship("Recipe", back_populates="recipe_ingredient_groups")
    group = relationship("IngredientGroup", back_populates="recipe_associations")
    ingredients = relationship("RecipeIngredient", back_populates="recipe_group", cascade="all, delete-orphan")

class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    id = Column(Integer, primary_key=True, index=True)
    recipe_group_id = Column(Integer, ForeignKey("recipe_ingredient_groups.id", ondelete="CASCADE"))
    ingredient_id = Column(Integer, ForeignKey("ingredients.id", ondelete="CASCADE"))
    name = Column(String(255))
    value = Column(String(100))
    type = Column(String(100))
    amount = Column(String(100))
    notes = Column(Text)
    sort_order = Column(Integer)

    recipe_group = relationship("RecipeIngredientGroup", back_populates="ingredients")
    ingredient = relationship("Ingredient")