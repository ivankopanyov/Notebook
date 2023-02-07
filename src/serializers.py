"""Модуль сериалайзеров."""

import json

from .base.serializers import BaseSerializer
from .models import Note
from .mapper import (
    note_to_dto, 
    dto_to_note
)
from .dto import NoteDto


class JsonNoteSerializer(BaseSerializer):
    """
    Класс, описывающий объект сериалайзера, 
    сериализующего объекты заметок в json.
    """

    def encode(self, objects: list[Note]) -> str:
        """Метод сериализации списка объектов заметок в json."""
        result = []
        for item in objects:
            note = note_to_dto(item)
            result.append({
                "id": note.id,
                "name": note.name,
                "body": note.body,
                "create_date": note.create_date,
                "update_date": note.update_date
        })
        return json.dumps(result)

    def decode(self, data: str) -> list[Note]:
        """Метод десериализации json в спискок объектов заметок."""
        result = []
        for note in json.loads(data):
            result.append(dto_to_note(NoteDto(
                id=note["id"],
                name=note["name"],
                body=note["body"],
                create_date=note["create_date"],
                update_date=note["update_date"]
            )))
        return result
