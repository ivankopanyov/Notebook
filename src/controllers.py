from datetime import datetime

from dto import NoteDto
from models import Note
from db import Database


class BaseController:

    def __init__(self, db: Database) -> None:
        self.db = db

    def create(self, entity: object) -> None:
        pass

    def get(self, id: int) -> object:
        pass

    def get_all(self) -> list[object]:
        pass

    def update(self, id: int, entity: object) -> None:
        pass

    def delete(self, id: int) -> None:
        pass


class NoteController(BaseController):

    def create(self, entity: NoteDto) -> None:
        if type(entity) != NoteDto:
            raise TypeError()
        now = datetime.now()
        self.db.insert(
            Note(
                name=entity.name,
                body=entity.body,
                create_date=now,
                update_date=now
            )
        )

    def get(self, id: int) -> Note:
        if type(id) != int or id <= 0:
            raise TypeError()
        result = self.db.select(id)
        if result == None:
            raise TypeError()
        return result

    def get_all(self) -> list[Note]:
        return self.db.select_all()

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
