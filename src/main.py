from datetime import datetime

from models import Note
from serializers import NoteSerializer

note = Note("1", "123", datetime.now(), datetime.now())
json = NoteSerializer.to_json(note)
print(json)
note = NoteSerializer.from_json(json)
print(f"{note.name}, {note.body}, {note.create_date}, {note.update_date}")