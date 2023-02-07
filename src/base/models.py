"""Модуль базовых моделей."""

from datetime import datetime
from abc import ABC


class BaseModel(ABC):
    """Абстрактный класс, описывающий базовое представление."""

    def __init__(self, 
                id: int = 0, 
                create_date: datetime = datetime.now(), 
                update_date: datetime = datetime.now()) -> None:
        """Инициализация экземпляра базового представления."""
        self.id = id
        self.create_date = create_date
        self.update_date = update_date
