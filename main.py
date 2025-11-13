import subprocess
from fastapi import FastAPI, File, UploadFile, HTTPException,Query
import httpx
from fastapi.middleware.cors import CORSMiddleware
from exceptions import NoIngredientsDetectedError
from services import translate_batch
from sqlalchemy import func
app = FastAPI()
from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, get_db, Base
import os
from models import Recipe, RecipeIngredient, Ingredient, RecipeIngredientGroup
from sqlalchemy import text, inspect

load_dotenv()
ML_URL = os.getenv("ML_URL", "http://127.0.0.1:8080/predict/")

print("✅ FastAPI загружается...")
app = FastAPI()

# Добавляем SessionMiddleware (обязательно для OAuth)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "supersecret"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Аналог CORS_ALLOWED_ORIGINS
    allow_credentials=True,  # Аналог CORS_ALLOW_CREDENTIALS
    allow_methods=["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"],  # Аналог CORS_ALLOW_METHODS
    allow_headers=[
        "accept",
        "accept-encoding",
        "authorization",
        "content-type",
        "dnt",
        "origin",
        "user-agent",
        "x-csrftoken",
        "x-requested-with",
    ],  # Аналог CORS_ALLOW_HEADERS
)

# Настраиваем OAuth
oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

BASE_DIR = os.path.dirname(__file__)  # директория, где лежит main.py
DROP_FILE = os.path.join(BASE_DIR, "sql", "drop.sql")
TABLES_FILE = os.path.join(BASE_DIR, "sql", "tables.sql")
INSERT_CATEGORIES_FILE = os.path.join(BASE_DIR, "sql", "insert_categories.sql")
INSERT_CUISINES_FILE = os.path.join(BASE_DIR, "sql", "insert_cuisines.sql")
INSERT_INGREDIENT_GROUPS_FILE = os.path.join(BASE_DIR, "sql", "insert_ingredient_groups.sql")
INSERT_INGREDIENTS_FILE = os.path.join(BASE_DIR, "sql", "insert_ingredients.sql")
INSERT_INSTRUCTIONS_FILE = os.path.join(BASE_DIR, "sql", "insert_instructions.sql")
INSERT_RECIPE_INGREDIENT_GROUPS_FILE = os.path.join(BASE_DIR, "sql", "insert_recipe_ingredient_groups.sql")
INSERT_RECIPE_INGREDIENTS_FILE = os.path.join(BASE_DIR, "sql", "insert_recipe_ingredients.sql")
INSERT_RECIPE_TAGS_FILE = os.path.join(BASE_DIR, "sql", "insert_recipe_tags.sql")
INSERT_RECIPES_FILE = os.path.join(BASE_DIR, "sql", "insert_recipes.sql")
INSERT_TAGS_FILE = os.path.join(BASE_DIR, "sql", "insert_tags.sql")


def execute_sql_file(filename, conn):
    with open(filename, "r", encoding="utf-8") as f:
        sql_content = f.read()

    statements = []
    current = []
    for line in sql_content.splitlines():
        line = line.strip()
        if not line or line.startswith("--") or line.startswith("/*"):
            continue
        current.append(line)
        if line.endswith(";"):
            stmt = " ".join(current).strip()
            if stmt:
                statements.append(stmt)
            current = []

    for stmt in statements:
        stmt = stmt.replace("%", "%%")
        conn.execute(text(stmt))
    conn.commit()


def table_has_data(conn, table_name):
    """Возвращает True, если в таблице есть хотя бы одна запись"""
    result = conn.execute(text(f"SELECT EXISTS (SELECT 1 FROM {table_name} LIMIT 1)"))
    return result.scalar()  # True/False


def init_db():
    try:
        with engine.connect() as conn:
            inspector = inspect(engine)
            tables_created = False
            print("🔄 Инициализация базы запущена")


            # Так нада
            """
            print("💣 Очищаем схему...")
            execute_sql_file(DROP_FILE, conn)
            """
            # Создаём таблицы, если их нет
            if not inspector.has_table("recipes") or not inspector.has_table("ingredients"):
                print("⚒️ Создаём таблицы...")
                execute_sql_file(TABLES_FILE, conn)
                tables_created = True

            # Вставляем данные, только если таблицы пустые
            if not table_has_data(conn, "recipes"):
                print("📦 Вставляем данные в таблицы...")
                execute_sql_file(INSERT_TAGS_FILE, conn)
                print(" ✅ (1/10) Теги загружены")
                execute_sql_file(INSERT_CATEGORIES_FILE, conn)
                print(" ✅ (2/10) Категории №1 загружены")
                execute_sql_file(INSERT_CUISINES_FILE, conn)
                print(" ✅ (3/10) Категории №2 загружены")
                execute_sql_file(INSERT_INGREDIENTS_FILE, conn)
                print(" ✅ (4/10) Ингридиенты загружены")
                execute_sql_file(INSERT_INGREDIENT_GROUPS_FILE, conn)
                print(" ✅ (5/10) Группы ингридиентов загружены")
                execute_sql_file(INSERT_RECIPES_FILE, conn)
                print(" ✅ (6/10) Рецепты загружены")
                execute_sql_file(INSERT_RECIPE_TAGS_FILE, conn)
                print(" ✅ (7/10) Таблица recipe_tags для связи M2M заполнена")
                execute_sql_file(INSERT_INSTRUCTIONS_FILE, conn)
                print(" ✅ (8/10) Инструкции загружены")
                execute_sql_file(INSERT_RECIPE_INGREDIENT_GROUPS_FILE, conn)
                print(" ✅ (9/10) Таблица recipe_ingredient_groups для связи M2M заполнена")
                execute_sql_file(INSERT_RECIPE_INGREDIENTS_FILE, conn)
                print(" ✅ (10/10) Таблица recipe_ingredients для связи M2M заполнена")
            else:
                print("✅ Данные уже есть, пропускаем вставку")

            print("✅ Инициализация базы завершена")
    except Exception as e:
        print(f"❗️❗️❗️ Ошибка при инициализация базы: {e}")
        print("❌ Инициализация базы прервана")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return {"message": "Привет! API работает 🚀"}

# POST — создание пользователя
@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

# GET — получить всех пользователей

#@app.get("/users/", response_model=list[schemas.UserResponse])
def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.get("/auth/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    print("Redirecting to:", redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/callback", name="auth_callback")
async def auth_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo")
        print("Google user:", user_info)
        return user_info
    except Exception as e:
        return {"error": str(e)}

@app.get("/tags", response_model=list[schemas.TagResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.TagResponse).all()

@app.get("/categories", response_model=list[schemas.CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.CategoryResponse).all()

@app.post("/recipes/search/by-ingredients", response_model=list[schemas.RecipeListResponse])
def search_recipes_by_ingredients(request: schemas.IngredientSearchRequest,
                                  limit: int = 20,
                                  db: Session = Depends(get_db)):
    ingredient_names = [i.name.strip().lower() for i in request.ingredients if i.name.strip()]

    subq = (
        db.query(
            Recipe.id.label("recipe_id"),
            func.count(func.distinct(Ingredient.id)).label("match_count")
        )
        .join(Recipe.recipe_ingredient_groups)  # Recipe → RecipeIngredientGroup
        .join(RecipeIngredient, RecipeIngredient.recipe_group_id == RecipeIngredientGroup.id)
        .join(Ingredient, Ingredient.id == RecipeIngredient.ingredient_id)
        .filter(
            func.lower(Ingredient.name).in_(ingredient_names) |
            func.lower(Ingredient.slug).in_(ingredient_names)
        )
        .group_by(Recipe.id)
        .subquery()
    )

    query = (
        db.query(Recipe, subq.c.match_count)
        .join(subq, Recipe.id == subq.c.recipe_id)
        .order_by(subq.c.match_count.desc())
        .limit(limit)
        .all()
    )

    results = []

    for r, match_count in query:
        matched_ingredients = (
            db.query(Ingredient.name)
            .join(RecipeIngredient, Ingredient.id == RecipeIngredient.ingredient_id)
            .join(RecipeIngredientGroup, RecipeIngredient.recipe_group_id == RecipeIngredientGroup.id)
            .filter(
                RecipeIngredientGroup.recipe_id == r.id,
                func.lower(Ingredient.name).in_(ingredient_names)
            )
            .distinct()
            .all()
        )

        matched_list = [i[0] for i in matched_ingredients]

        results.append(
            {
                "id": r.id,
                "title": r.title,
                "category_name": r.category_name,
                "cuisine_name": r.cuisine_name,
                "poster": r.poster,
                "difficulty": r.difficulty,
                "cooktime": r.cooktime,
                "vegan": r.vegan,
                "created_at": r.created_at,
                "match_count": match_count,
                "matched_ingredients": matched_list
            }
        )

    return results

    #return db.query(models.Recipe).limit(limit).all()

@app.get("/recipes/all", response_model=list[schemas.RecipeListResponse])
def get_recipes(limit: int = 20, db: Session = Depends(get_db)):
    return db.query(models.Recipe).limit(limit).all()


@app.get("/recipes/search/{search_word}",response_model=list[schemas.RecipeListResponse])
def get_recepts_by_word(search_word: str, limit: int = 20, db: Session = Depends(get_db)):
    recept = db.query(models.Recipe).filter(models.Recipe.title.ilike(f"%{search_word}%")).limit(limit).all()
    if not recept:
        raise HTTPException(status_code=404, detail="Рецепты не найдены")
    return recept

@app.get("/recipes/{recept_id}", response_model=schemas.RecipeResponse)
def get_recept(recept_id: int, db: Session = Depends(get_db)):
    recept = db.query(models.Recipe).filter(models.Recipe.id == recept_id).first()
    if not recept:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    return recept

@app.post("/upload-photo/")
async def upload_photo(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Файл должен быть изображением")

    image_data = await file.read()

    # Отправляем другому сервису
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            files = {'file': (file.filename, image_data, file.content_type)}
            response = await client.post(
                ML_URL,
                files=files
            )
            response.raise_for_status()

            # Получаем JSON ответ
            result = response.json()
            ingredients = [detection["class_name"] for detection in result["detections"]]

            tr_ingredients = translate_batch(ingredients)

            if not tr_ingredients:
                raise NoIngredientsDetectedError()

            return {
                "message": "Фото успешно обработано",
                "found_ingredients_count": len(tr_ingredients),
                "ingredients": tr_ingredients
            }

            """
            found_recipes = [] #find_recipes_by_ingredients_precise(tr_ingredients, db, limit=20)

            return {
                "message": "Фото успешно обработано",
                "detected_ingredients": tr_ingredients,
                "found_recipes_count": len(found_recipes),
                "recipes": [
                    {
                        "id": recipe.id_recepts,
                        "name": recipe.recept_name,
                        "ingredients": recipe.recept_sostav,
                        "instructions": recipe.recept_instuction,
                        "category_id": recipe.recept_category,
                        "podcategory": recipe.podcategory
                    } for recipe in found_recipes
                ]
            }
            """
        except NoIngredientsDetectedError:
            raise
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Таймаут при обращении к внешнему сервису")
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Ошибка внешнего сервиса: {str(e)}")