"""Модуль функций преобразования объектов."""

from datetime import datetime

from .models import Note
from .dto import NoteDto
from .settings import DATETIME_FORMAT


def note_to_dto(note: Note) -> NoteDto:
    """Функция преобразования объекта заметки в трансфер объект."""
    return NoteDto(
        id=note.id,
        name=note.name,
        body=note.body,
        create_date=note.create_date.strftime(DATETIME_FORMAT),
        update_date=note.update_date.strftime(DATETIME_FORMAT)
    )


def dto_to_note(note: NoteDto) -> Note:
    """Функция преобразования трансфер объекта в трансфер объект заметки."""
    return Note(
        id=note.id,
        name=note.name,
        body=note.body,
        create_date=datetime.strptime(note.create_date, DATETIME_FORMAT),
        update_date=datetime.strptime(note.update_date, DATETIME_FORMAT)
    )
