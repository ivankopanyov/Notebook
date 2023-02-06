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

    def create(self, entity: NoteDto) -> ListView:
        now = datetime.now()
        self.db.insert(
            Note(
                name=entity.name,
                body=entity.body,
                create_date=now,
                update_date=now
            )
        )
        return lambda: self.get_all()

    def get(self, id: int) -> ListView:
        note = self.db.select(id)
        message = f"{note.id}. {note.name}\n\n"
        message += f"Создано: {note.create_date:%d.%m.%Y %H:%M:%S}\n"
        message += f"Изменено: {note.update_date:%d.%m.%Y %H:%M:%S}\n\n"
        message += note.body
        selected_list = SelectedList()
        selected_list.add(
            SelectedListItem(
                key="update",
                title="Изменить заметку",
                action=lambda: self.__update_note__(id)
            )
        )
        selected_list.add(
            SelectedListItem(
                key="delete",
                title="Удалить заметку",
                action=lambda: self.delete(id)
            )
        )
        selected_list.add(
            SelectedListItem(
                key="back",
                title="Назад",
                action=lambda: self.get_all()
            )
        )
        return ListView(selected_list, message)

    def get_all(self, order_by_update_date: bool = False, desc: bool = False) -> ListView:
        notes = self.db.select_all()
        selected_list = SelectedList(0 if len(notes) == 0 else 6)
        message = "Список заметок пуст" if len(notes) == 0 else None
        if len(notes) > 0:
            notes.sort(
                key=lambda x: x.update_date if order_by_update_date == True else x.id, 
                reverse=desc
            )
            for note in notes:
                selected_list.add(SelectedListItem(
                    key=f"{note.id}",
                    title=f"{note.name} (Изменено: {note.update_date:%d.%m.%Y %H:%M:%S})",
                    action=lambda: self.get(note.id)
                ))
        selected_list.add(SelectedListItem(
            key="add",
            title="Создать заметку",
            action=lambda: self.__create_note__()
        ))
        if len(notes) > 0:
            selected_list.add(SelectedListItem(
                key="sort id",
                title="Сортировка по ID",
                action=lambda: self.get_all()
            ))
            selected_list.add(SelectedListItem(
                key="sort id desc",
                title="Сортировка по ID в обратном порядке",
                action=lambda: self.get_all(desc=True)
            ))
            selected_list.add(SelectedListItem(
                key="sort date",
                title="Сортировка по дате изменения",
                action=lambda: self.get_all(order_by_update_date=True)
            ))
            selected_list.add(SelectedListItem(
                key="sort date desc",
                title="Сортировка по дате изменения в обратном порядке",
                action=lambda: self.get_all(order_by_update_date=True, desc=True)
                )
            )
        selected_list.add(
            SelectedListItem(key="exit", title="Выход", action=lambda: sys.exit())
        )
        return ListView(selected_list, message)

    def update(self, id: int, entity: NoteDto) -> ListView:
        note = self.db.select(id)
        note.name = entity.name
        note.body = entity.body
        note.update_date = datetime.now()
        self.db.update(note)
        return lambda: self.get(id)

    def delete(self, id: int) -> ListView:
        self.db.delete(id)
        return self.get_all()

    def __create_form__(self) -> Form:
        form = Form()
        form.add(FormStringItem(key="name", title="Название заметки: "))
        form.add(FormStringItem(key="body", title="Текст заметки: "))
        return form
        
    def __create_note__(self):
        form = self.__create_form__()
        return FormView(form, 
            lambda values: self.create(
                entity=NoteDto(
                    name=values["name"],
                    body=values["body"]
                )
            ), 
            "Создание заметки"
        )

    def __update_note__(self, id: int):
        form = self.__create_form__()
        return FormView(form, 
            lambda values: self.update(
                id=id,
                entity=NoteDto(
                    name=values["name"],
                    body=values["body"]
                )
            ), 
            "Изменение заметки"
        )