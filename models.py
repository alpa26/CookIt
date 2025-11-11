from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, BigInteger
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

    recipes = relationship("Recipe", back_populates="author")
    favorites = relationship("Favorite", back_populates="user")

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(Text)
    category = Column(String(255))
    category_slug = Column(String(255))
    title = Column(String(500), nullable=False)
    description = Column(Text)
    note = Column(Text)
    cuisine = Column(String(255))
    cuisine_slug = Column(String(255))
    poster = Column(Text)
    difficulty = Column(String(100))
    cooktime = Column(String(100))
    preparetime = Column(String(100))
    video = Column(Text)
    vegan = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    ingredient_groups = relationship("IngredientGroup", back_populates="recipe", cascade="all, delete-orphan")
    instructions = relationship("Instruction", back_populates="recipe", cascade="all, delete-orphan")
    tags = relationship("Tag", back_populates="recipe", cascade="all, delete-orphan")


class IngredientGroup(Base):
    __tablename__ = "ingredient_groups"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"))
    name = Column(String(255))
    sort_order = Column(Integer)

    # Relationships
    recipe = relationship("Recipe", back_populates="ingredient_groups")
    ingredients = relationship("Ingredient", back_populates="group", cascade="all, delete-orphan")


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

    # Relationships
    group = relationship("IngredientGroup", back_populates="ingredients")


class Instruction(Base):
    __tablename__ = "instructions"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"))
    text = Column(Text, nullable=False)
    image = Column(Text)
    step_number = Column(Integer)

    # Relationships
    recipe = relationship("Recipe", back_populates="instructions")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    slug = Column(String(255))

    # Relationships
    recipe = relationship("Recipe", back_populates="tags")

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="favorites")
    recipe = relationship("Recipe", back_populates="favorited_by")