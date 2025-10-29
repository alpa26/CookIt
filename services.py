from deep_translator import GoogleTranslator
from sqlalchemy import or_
import re

from models import KukingRecept


def translate_batch(word_list):
    """Пакетный перевод всего списка"""
    try:
        translator = GoogleTranslator(source='en', target='ru')
        # Пакетный перевод всего списка
        translations = translator.translate_batch(word_list)
        return translations
    except Exception as e:
        print(f"Ошибка пакетного перевода: {e}")
        return word_list

def normalize_ingredient(ingredient):
    """Нормализация названия ингредиента"""
    # Приводим к нижнему регистру и убираем лишние пробелы
    return ingredient.lower().strip()


def find_recipes_by_ingredients_precise(ingredients_list, db_session):
    """
    Более точный поиск с учетом различных форм слов
    """
    conditions = []

    for ingredient in ingredients_list:
        normalized = normalize_ingredient(ingredient)

        # Ищем в разных формах
        conditions.append(KukingRecept.recept_sostav.ilike(f"%{normalized}%"))

        # Если ингредиент в единственном числе, ищем также во множественном
        if normalized.endswith(('а', 'я', 'о', 'е', 'ь')):
            plural_form = normalized + 'ы'  # простая логика для множественного числа
            conditions.append(KukingRecept.recept_sostav.ilike(f"%{plural_form}%"))

    recipes = db_session.query(KukingRecept).filter(or_(*conditions)).all()
    return recipes