"""Модуль бизнес логики приложения."""

import sys

from .views import (
    SelectedList,
    SelectedListItem,
    ListView,
    FormStringItem,
    Form,
    FormView
)
from .base.controllers import BaseController
from .dto import SimpleNoteDto, NoteDto


def show_notes_list(notes: list[NoteDto], controller: BaseController) -> ListView:
    """Функция создания представления списка заметок."""
    selected_list = SelectedList(0 if len(notes) == 0 else 6)
    message = "Список заметок пуст" if len(notes) == 0 else None
    for note in notes:
        selected_list.add(SelectedListItem(
            key=f"{note.id}",
            title=f"{note.name} (Изменено: {note.update_date})",
            action=lambda id=note.id: controller.get(id)
        ))
    selected_list.add(SelectedListItem(
        key="add",
        title="Создать заметку",
        action=lambda: __create_note__(controller).show()
    ))
    if len(notes) > 0:
        selected_list.add(SelectedListItem(
            key="sort id",
            title="Сортировка по ID",
            action=lambda: controller.get_all()
        ))
        selected_list.add(SelectedListItem(
            key="sort id desc",
            title="Сортировка по ID в обратном порядке",
            action=lambda: controller.get_all(desc=True)
        ))
        selected_list.add(SelectedListItem(
            key="sort date",
            title="Сортировка по дате изменения",
            action=lambda: controller.get_all(order_by_update_date=True)
        ))
        selected_list.add(SelectedListItem(
            key="sort date desc",
            title="Сортировка по дате изменения в обратном порядке",
            action=lambda: controller.get_all(order_by_update_date=True, desc=True)
            )
        )
    selected_list.add(
        SelectedListItem(key="exit", title="Выход", action=lambda: sys.exit())
    )
    return ListView(selected_list, message)


def show_note(note: NoteDto, controller: BaseController) -> ListView:
    """Функция создания представления заметки."""
    message = f"{note.id}. {note.name}\n\n"
    message += f"Создано: {note.create_date}\n"
    message += f"Изменено: {note.update_date}\n\n"
    message += note.body
    selected_list = SelectedList()
    selected_list.add(
        SelectedListItem(
            key="update",
            title="Изменить заметку",
            action=lambda: __update_note__(note.id, controller).show()
        )
    )
    selected_list.add(
        SelectedListItem(
            key="delete",
            title="Удалить заметку",
            action=lambda: controller.delete(note.id)
        )
    )
    selected_list.add(
        SelectedListItem(
            key="back",
            title="Назад",
            action=lambda: controller.get_all()
        )
    )
    return ListView(selected_list, message)


def __create_form__() -> Form:
    """Функция создания формы заметки."""
    form = Form()
    form.add(FormStringItem(key="name", title="Название заметки: "))
    form.add(FormStringItem(key="body", title="Текст заметки: "))
    return form
    

def __create_note__(controller: BaseController):
    """Функция создания представления формы для создания заметки."""
    form = __create_form__()
    return FormView(form, 
        lambda values: controller.create(
            entity=SimpleNoteDto(
                name=values["name"],
                body=values["body"]
            )
        ), 
        "Создание заметки"
    )


def __update_note__(id: int, controller: BaseController):
    """Функция создания представления формы для изменения заметки."""
    form = __create_form__()
    return FormView(form, 
        lambda values: controller.update(
            id=id,
            entity=SimpleNoteDto(
                name=values["name"],
                body=values["body"]
            )
        ), 
        "Изменение заметки"
    )
