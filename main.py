import subprocess

from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, get_db, Base
import os
from sqlalchemy import text

load_dotenv()
print("✅ FastAPI загружается...")
app = FastAPI()

# Добавляем SessionMiddleware (обязательно для OAuth)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "supersecret"))

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
TABLES_FILE = os.path.join(BASE_DIR, "sql", "tables.sql")
INSERTS_FILE = os.path.join(BASE_DIR, "sql", "inserts.sql")

def execute_sql_file(filename):
    """Выполняет SQL команды из файла через SQLAlchemy"""
    with open(filename, "r", encoding="utf-8") as f:
        sql_content = f.read()

    # Разбиваем на отдельные команды по ;
    statements = [stmt.strip() for stmt in sql_content.split(";") if stmt.strip()]

    success, fail = 0, 0
    with engine.connect() as conn:
        for stmt in statements:
            try:
                conn.execute(text(stmt))
                conn.commit()
                success += 1
            except Exception as e:
                conn.rollback()
                fail += 1
                print(f"❌ Ошибка при SQL:\n{stmt[:80]}...\nПричина: {e}\n")
    print(f"✅ Файл {filename} импортирован: {success} успешно, {fail} с ошибками.")

@app.on_event("startup")
def on_startup():
    print("📦 Создание таблиц...")
    execute_sql_file(TABLES_FILE)

    print("📦 Импорт данных...")
    execute_sql_file(INSERTS_FILE)

@app.get("/")
def root():
    return {"message": "Привет! API работает 🚀"}

# POST — создание пользователя
@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

# GET — получить всех пользователей
@app.get("/users/", response_model=list[schemas.UserResponse])
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

@app.get("/categories", response_model=list[schemas.KukingCategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.KukingCategory).all()


@app.get("/recepts", response_model=list[schemas.KukingReceptResponse])
def get_recepts(limit: int = 20, db: Session = Depends(get_db)):
    return db.query(models.KukingRecept).limit(limit).all()


@app.get("/recepts/{recept_id}", response_model=schemas.KukingReceptResponse)
def get_recept(recept_id: int, db: Session = Depends(get_db)):
    recept = db.query(models.KukingRecept).filter(models.KukingRecept.id_recepts == recept_id).first()
    if not recept:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    return recept