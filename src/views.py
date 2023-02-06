from abc import ABC, abstractmethod
from collections import OrderedDict

from dto import NoteDto


class ListItem:

    def __init__(self, name: str, action) -> None:
        self.name = name
        self.action = action


class BaseView(ABC):

    @abstractmethod
    def show(self):
        pass


class ListView(BaseView):

    def __init__(self, 
                message: str, 
                items: OrderedDict[str, ListItem], 
                footer: int = 0, 
                error: str = None) -> None:
        self.message = message
        self.items = items
        self.footer = footer
        self.error = error

    def show(self):
        if self.error != None:
            show_message(self.error)
        return select_item_in_dict(self.message, self.items, self.footer)


class ItemView(BaseView):

    def __init__(self, 
                message: str, 
                items: list[str], 
                zero_item: str = None, 
                error: str = None) -> None:
        self.message = message
        self.items = items
        self.zero_item = zero_item
        self.error = error

    def show(self):
        if self.error != None:
            show_message(self.error)
        return select_item_in_dict(self.message, self.items, self.zero_item)


class CreateView(BaseView):

    def __init__(self, items: dict[str, str], action) -> None:
        self.items = items
        self.action = action

    def show(self):
        result = input_form(self.items)
        note = NoteDto(
            name=result["name"],
            body=result["body"]
        )
        return lambda: self.action(note)


def show_message(message: str) -> None:
    print(message)


def input_number(message: str = None, min: int = None, max: int = None) -> int:
    if min != None and max != None and max < min:
        max = min
    if message == None:
        message = f"Укажите число{f' от {min}' if type(min) == int else ''}{f' до {max}' if type(max) == int else ''}: "
    while True:
        try:
            result = int(input(message))
            if (type(min) == int and result < min) or (type(max) == int and result > max):
                show_message("Нарушен диапазон! Повторите попытку...")
                continue
            return result
        except TypeError:
            show_message("Некорректный ввод! Повторите попытку...")


def input_str(message: str) -> str:
    return input(message)


def input_form(items: dict[str, str]) -> dict[str, str]:
    result = {}
    for key in items.keys():
        result[key] = input_str(items[key])
    return items


def select_item(message: str, items: list[str], zero_item: str = None) -> int:
    for i in range(len(items)):
        show_message(f"{i + 1}. {items[i]}")
    if zero_item != None:
        show_message(f"\n{0}. {zero_item}")
    show_message("")
    return input_number(message, 1 if zero_item == None else 0, len(items))


def select_item_in_dict(message: str, items: OrderedDict[str, ListItem], footer: int = 0):
    i = 0
    for key in items:
        show_message(f"{key} >> {items[key].name}")
        i += 1
        if i == len(items) - footer:
            show_message("")
    show_message("")
    while True:
        key = input_str(message)
        if key not in items.keys():
            show_message(f"Команда {key} не найдена! Повторите попытку...")
        else:
            return items[key].action
