from typing import List
from threading import Lock

class ModelManager:
    _instance = None
    _lock = Lock()

    def __init__(self):
        self.available_models = [
            "amazon/nova-2-lite-v1:free",
            "nvidia/nemotron-nano-12b-v2-vl:free",
            "mistralai/mistral-small-3.1-24b-instruct:free"
        ]
        self.primary_model = self.available_models[0]
        self.fallback_model = self.available_models[0]
        self.is_repeat = True

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize()
            return cls._instance

    def _initialize(self):
        self.is_repeat = True

    def set_models(self, primary: str, fallback: str):
        if primary in self.available_models and fallback in self.available_models:
            self.primary_model = primary
            self.fallback_model = fallback
        else:
            raise ValueError("Модели должны быть из списка available_models")

    def set_repeat(self, repeat: bool):
        self.is_repeat = repeat

    def get_settings(self):
        return {
            "is_repeat": self.is_repeat,
            "primary": self.primary_model,
            "fallback": self.fallback_model,
            "available": self.available_models
        }

MODEL_MANAGER = ModelManager()