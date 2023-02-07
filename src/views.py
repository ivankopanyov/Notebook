"""Модуль представлений."""

from abc import ABC, abstractmethod
from collections import OrderedDict

from .base.views import BaseView


class SelectedListItem:
    """Класс, описывающий элемент списка для выбора."""

    def __init__(self,
                key: str,
                title: str,
                action) -> None:
        """Инициализация элемента списка."""
        self.key = key
        self.title = title
        self.action = action


class SelectedList:
    """Класс, описывающий список."""

    def __init__(self, footer: int = 0) -> None:
        """Инициализация списка."""
        self.items: OrderedDict[str, SelectedListItem] = OrderedDict()
        self.footer = footer

    def add(self, item: SelectedListItem) -> None:
        """Метод добавления элемента в список."""
        self.items[item.key] = item

    def select(self):
        """Метод выбора элемента списка."""
        i = 0
        for key in self.items.keys():
            print(f"{key} >> {self.items[key].title}")
            i += 1
            if i == len(self.items) - self.footer:
                print()
        print()
        while True:
            key = input("Укажите номер пункта меню или команду: ")
            if key not in self.items.keys():
                print(f"Команда {key} не найдена! Повторите попытку...")
            else:
                print()
                return self.items[key].action


class FormItem(ABC):
    """Абстрактный класс, описывающий элемент формы для заполнения."""

    def __init__(self, 
                key: str,
                title: str,
                min: int = -1, 
                max: int = -1) -> None:
        """Инициализация элемента формы."""
        self.key = key
        self.title = title
        self.min = min
        self.max = max if max >= min else min
    
    @abstractmethod
    def input_value(self):
        """Абстрактный метод заполнения элемента формы."""
        pass


class FormStringItem(FormItem):
    """Класс, описывающий элемент формы для ввода строки."""
    
    def input_value(self) -> str:
        """Метод заполнения элемента формы."""
        while True:
            result = input(self.title)
            if (self.min >= 0 and len(result) < self.min) or (self.max >= 0 and len(result) > self.max):
                print("Некорректная длина строки! Повторите попытку...")
            else:
                return result


class FormIntItem(FormItem):
    """Класс, описывающий элемент формы для ввода целого числа."""

    def input_value(self) -> int:
        """Метод заполнения элемента формы."""
        while True:
            try:
                result = int(input(self.title))
                if (self.min >= 0 and result < self.min) or (self.max >= 0 and result > self.max):
                    print("Нарушен диапазон! Повторите попытку...")
                else:
                    return result
            except TypeError:
                print("Некорректный ввод! Повторите попытку...")


class Form:
    """Класс, описывающий форму для заполнения."""

    def __init__(self) -> None:
        """Инициализация объекта формы."""
        self.items: OrderedDict[str, FormItem] = OrderedDict()

    def add(self, item: FormItem) -> None:
        """Метод добавления элемента в форму."""
        self.items[item.key] = item
    
    def fill(self) -> dict:
        """Метод заполнения формы."""
        result = {}
        for key in self.items.keys():
            result[key] = self.items[key].input_value()
        print()
        return result


class ListView(BaseView):
    """Класс, описывающий представление для вывода списка."""

    def __init__(self, 
                selected_list: SelectedList, 
                message: str = None) -> None:
        """Инициализация представления."""
        self.selected_list = selected_list
        self.message = message
    
    def show(self):
        """Метод вывода представления на экран."""
        if self.message != None:
            print(self.message)
            print()
        return self.selected_list.select()


class FormView(BaseView):
    """Класс, описывающий представление для вывода формы."""

    def __init__(self, 
                form: Form,
                action,
                message: str = None) -> None:
        """Инициализация представления."""
        self.form = form
        self.action = action
        self.message = message
    
    def show(self):
        """Метод вывода представления на экран."""
        print(self.message)
        print()
        return self.action(self.form.fill())
