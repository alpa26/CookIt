from deep_translator import GoogleTranslator
from sqlalchemy import or_
import re



def translate_batch(word_list):
    """Пакетный перевод всего списка"""
    try:
        translator = GoogleTranslator(source='en', target='ru')
        translations = translator.translate_batch(word_list)
        return translations
    except Exception as e:
        print(f"Ошибка пакетного перевода: {e}")
        return word_list

def normalize_ingredient(ingredient):
    """Нормализация названия ингредиента"""
    return ingredient.lower().strip()


def find_recipes_by_ingredients_precise(ingredients_list, db_session, limit=20):

    conditions = []

    for ingredient in ingredients_list:
        normalized = normalize_ingredient(ingredient)

        conditions.append(KukingRecept.recept_sostav.ilike(f"%{normalized}%"))

        if normalized.endswith(('а', 'я', 'о', 'е', 'ь')):
            plural_form = normalized + 'ы'
            conditions.append(KukingRecept.recept_sostav.ilike(f"%{plural_form}%"))

    recipes = db_session.query(KukingRecept).filter(or_(*conditions)).limit(limit).all()
    return recipes
