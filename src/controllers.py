from datetime import datetime

from dto import NoteDto
from models import Note
from db import Database

class NoteController:

    def __init__(self, db: Database) -> None:
        self.db = db

    def create(self, note: NoteDto) -> None:
        if type(note) != NoteDto:
            raise TypeError()
        now = datetime.now()
        self.db.insert(
            Note(
                name=note.name,
                body=note.body,
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

    def get_all(self):
        return self.db.select_all()

    def update(self, id: int, note: NoteDto):
        if type(id) != int or id <= 0 or type(note) != NoteDto:
            raise TypeError()
        
        try:
            current_node = self.get(id)
            current_node.name = note.name
            current_node.body = note.body
            current_node.update_date = datetime.now()
        except TypeError:
            raise TypeError()

    def delete(self, id: int):
        self.db.delete(id)