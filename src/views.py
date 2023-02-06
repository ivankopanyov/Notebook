from abc import ABC, abstractmethod
from collections import OrderedDict

from dto import NoteDto


class SelectedListItem:

    def __init__(self,
                key: str,
                title: str,
                action) -> None:
        self.key = key
        self.title = title
        self.action = action


class SelectedList:

    def __init__(self, footer: int = 0) -> None:
        self.items: OrderedDict[str, SelectedListItem] = OrderedDict()
        self.footer = footer

    def add(self, item: SelectedListItem) -> None:
        self.items[item.key] = item

    def select(self):
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
                return self.items[key].action


class FormItem(ABC):

    def __init__(self, 
                key: str,
                title: str,
                min: int = -1, 
                max: int = -1) -> None:
        self.key = key
        self.title = title
        self.min = min
        self.max = max if max >= min else min
    
    @abstractmethod
    def input_value(self):
        pass

class FormStringItem(FormItem):
    
    def input_value(self) -> str:
        while True:
            result = input(self.title)
            if (self.min >= 0 and len(result) < self.min) or (self.max >= 0 and len(result) > self.max):
                print("Некорректная длина строки! Повторите попытку...")
            else:
                return result


class FormIntItem(FormItem):

    def input_value(self) -> int:
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

    def __init__(self) -> None:
        self.items: OrderedDict[str, FormItem] = OrderedDict()

    def add(self, item: FormItem) -> None:
        self.items[item.key] = item
    
    def fill(self) -> dict:
        result = {}
        for key in self.items.keys():
            result[key] = self.items[key].input_value()
        return result


class BaseView(ABC):

    @abstractmethod
    def show(self):
        pass


class ListView(BaseView):

    def __init__(self, 
                selected_list: SelectedList, 
                message: str | None = None) -> None:
        self.selected_list = selected_list
        self.message = message
    
    def show(self):
        if self.message != None:
            print(self.message)
            print()
        return self.selected_list.select()


class FormView(BaseView):

    def __init__(self, 
                form: Form,
                action,
                message: str | None = None) -> None:
        self.form = form
        self.action = action
        self.message = message
    
    def show(self) -> dict:
        print(self.message)
        print()
        return self.action(self.form.fill())
