from fastapi import HTTPException

class NoIngredientsDetectedError(HTTPException):
    """Не обнаружено ингредиентов на изображении"""
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="На изображении не обнаружено ингредиентов. Попробуйте другое фото."
        )
