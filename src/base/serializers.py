"""Модуль базовых сериалайзеров."""

from abc import ABC, abstractmethod

from .models import BaseModel


class BaseSerializer(ABC):
    """Абстрактный класс, описывающий базовый сериалайзер."""

    @abstractmethod
    def encode(self, objects: list[BaseModel]):
        """Абстарактный метод сериализации объекта."""
        pass
    
    @abstractmethod
    def decode(self, data: str) -> list[BaseModel]:
        """Абстарактный метод десериализации объекта."""
        pass
