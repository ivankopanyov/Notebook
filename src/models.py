"""Модуль классов моделей."""

from datetime import datetime

from .base.models import BaseModel


class Note(BaseModel):
    """Класс, описывающий модель заметки"""

    def __init__(self,
                id: int = 0, 
                name: str = '', 
                body: str = '', 
                create_date: datetime = datetime.now(), 
                update_date: datetime = datetime.now()) -> None:
        """Инициализация объекта заметки"""
        super().__init__(id, create_date, update_date)
        self.name = name
        self.body = body
