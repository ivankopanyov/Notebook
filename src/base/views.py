"""Модуль базовых представлений."""

from abc import ABC, abstractmethod


class BaseView(ABC):
    """Абстрактный класс, описывающий базовое представление."""

    @abstractmethod
    def show(self):
        """Абстарактный метод вывода представления на экран."""
        pass
