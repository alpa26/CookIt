from sqlalchemy.orm import Session
import models, schemas

def create_user(db: Session, google_id: str, email: str, name: str, avatar_url: str):
    user = db.query(models.User).filter(models.User.google_id == google_id).first()
    if user:
        return user
    new_user = models.User(google_id=google_id, email=email, name=name, avatar_url=avatar_url)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_recipe(db: Session, recipe: schemas.RecipeCreate, user_id: int):
    db_recipe = models.Recipe(**recipe.dict(), created_by=user_id)
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


def get_recipes(db: Session):
    return db.query(models.Recipe).all()


def add_favorite(db: Session, user_id: int, recipe_id: int):
    fav = models.Favorite(user_id=user_id, recipe_id=recipe_id)
    db.add(fav)
    db.commit()
    db.refresh(fav)
    return fav


def get_favorites(db: Session, user_id: int):
    return db.query(models.Favorite).filter(models.Favorite.user_id == user_id).all()
