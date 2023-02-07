"""Модуль базовых контроллеров."""

from abc import ABC, abstractmethod

from .repositories import BaseRepository
from .models import BaseModel
from .views import BaseView


class BaseController(ABC):
    """Абстрактный класс, описывающий базовый контроллер."""

    def __init__(self, repository: BaseRepository) -> None:
        """Инициализация экземпляра базового контроллера."""
        self.repository = repository

    @abstractmethod
    def create(self, entity: BaseModel) -> BaseView:
        """Абстарактный метод создания объекта."""
        pass

    @abstractmethod
    def get(self, id: int) -> BaseView:
        """Абстарактный метод получения объекта."""
        pass

    @abstractmethod
    def get_all(self) -> BaseView:
        """Абстарактный метод получения всех объектов."""
        pass

    @abstractmethod
    def update(self, id: int, entity: BaseModel) -> BaseView:
        """Абстарактный метод изменения объекта."""
        pass

    @abstractmethod
    def delete(self, id: int) -> BaseView:
        """Абстарактный метод удаления объекта."""
        pass
