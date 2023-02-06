from datetime import datetime
from abc import ABC, abstractmethod
import sys

from dto import NoteDto
from models import Note
from db import Database
from views import *


class BaseController(ABC):

    def __init__(self, db: Database) -> None:
        self.db = db

    @abstractmethod
    def create(self, entity: object) -> None:
        pass

    @abstractmethod
    def get(self, id: int) -> object:
        pass

    @abstractmethod
    def get_all(self) -> BaseView:
        pass

    @abstractmethod
    def update(self, id: int, entity: object) -> None:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass


class NoteController(BaseController):

    def create(self, entity: NoteDto) -> ItemView:
        now = datetime.now()
        self.db.insert(
            Note(
                name=entity.name,
                body=entity.body,
                create_date=now,
                update_date=now
            )
        )

    def get(self, id: int) -> ItemView:
        if type(id) != int or id <= 0:
            raise TypeError()
        result = self.db.select(id)
        if result == None:
            raise TypeError()
        return result

    def get_all(self, order_by_update_date: bool = False, desc: bool = False) -> ListView:
        notes = self.db.select_all()
        if order_by_update_date == True:
            notes.sort(key=lambda x: x.update_date, reverse=desc)
        else:
            notes.sort(key=lambda x: x.id, reverse=desc)
        items = OrderedDict()
        for note in notes:
            items[f"{note.id}"] = ListItem(
                name=f"{note.name} (Изменено: {note.update_date:%d.%m.%Y %H:%M:%S})", 
                action=lambda id: self.get(id)
            )
        items["add"] = ListItem(
            name="Создать заметку", 
            action=lambda note: self.create(note)
        )
        items["sort id"] = ListItem(
            name="Сортировка по id",
            action=lambda: self.get_all()
        )
        items["sort id desc"] = ListItem(
            name="Сортировка по id в обратном порядке", 
            action=lambda: self.get_all(desc=True)
        )
        items["sort date"] = ListItem(
            name="Сортировка по дате изменения", 
            action=lambda: self.get_all(order_by_update_date=True)
        )
        items["sort date desc"] = ListItem(
            name="Сортировка по дате изменения в обратном порядке", 
            action=lambda: self.get_all(order_by_update_date=True, desc=True)
        )
        items["add"] = ListItem(name="Создать заметку", action=None)
        items["exit"] = ListItem(name="Выход", action=lambda: sys.exit())
        return ListView(
            message="Укажите номер заметки или команду: ",
            items=items,
            footer=6,
            error="\tСписок заметок пуст!" if len(notes) == 0 else None
        )

    def update(self, id: int, entity: NoteDto) -> None:
        if type(id) != int or id <= 0 or type(entity) != NoteDto:
            raise TypeError()
        try:
            current_node = self.get(id)
            current_node.name = entity.name
            current_node.body = entity.body
            current_node.update_date = datetime.now()
        except TypeError:
            raise TypeError()

    def delete(self, id: int) -> None:
        self.db.delete(id)
