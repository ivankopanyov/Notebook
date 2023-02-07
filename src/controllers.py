"""Модуль контроллеров."""

from datetime import datetime

from .base.controllers import BaseController
from .base.views import BaseView
from .dto import SimpleNoteDto
from .models import Note
from .business import (
    show_notes_list,
    show_note
)
from .mapper import note_to_dto


class NoteController(BaseController):
    """Класс, описывающий контроллер заметок."""

    def create(self, entity: SimpleNoteDto) -> BaseView:
        """Метод создания заметки."""
        now = datetime.now()
        self.repository.insert(
            Note(
                name=entity.name,
                body=entity.body,
                create_date=now,
                update_date=now
            )
        )
        return self.get_all()

    def get(self, id: int) -> BaseView:
        """Метод получения заметки."""
        note = self.repository.select(id)
        return show_note(note=note_to_dto(note), controller=self)

    def get_all(self, order_by_update_date: bool = False, desc: bool = False) -> BaseView:
        """Метод получения всех заметкок."""
        notes = self.repository.select_all()
        notes.sort(
            key=lambda x: x.update_date if order_by_update_date == True else x.id, 
            reverse=desc
        )
        return show_notes_list(
            notes=list(map(note_to_dto, self.repository.select_all())),
            controller=self
        )

    def update(self, id: int, entity: SimpleNoteDto) -> BaseView:
        """Метод изменения заметки."""
        note = self.repository.select(id)
        note.name = entity.name
        note.body = entity.body
        note.update_date = datetime.now()
        self.repository.update(note)
        return self.get_all()

    def delete(self, id: int) -> BaseView:
        """Метод удаления заметки."""
        self.repository.delete(id)
        return self.get_all()
