"""Модуль базовых репозиториев."""

from abc import ABC, abstractmethod

from .models import BaseModel


class BaseRepository(ABC):
    """Абстрактный класс, описывающий базовый репозиторий."""

    @abstractmethod
    def select(self, id: int) -> BaseModel:
        """Абстарактный метод получения объекта из репозитория."""
        pass

    @abstractmethod
    def select_all(self) -> list[BaseModel]:
        """Абстарактный метод получения всех объектов из репозитория."""
        pass

    @abstractmethod
    def insert(self, entity: BaseModel) -> None:
        """Абстарактный метод добавления объекта в репозиторий."""
        pass

    @abstractmethod
    def update(self, entity: BaseModel) -> None:
        """Абстарактный метод изменения объекта в репозитории."""
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        """Абстарактный метод удаления объекта из репозитория."""
        pass
