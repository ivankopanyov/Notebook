from file import FileManager
from serializers import JsonNoteSerializer
from db import FileDatabase
from controllers import NoteController
from dto import NoteDto
import time

def main():
    file_manager = FileManager("db.json")
    serializer = JsonNoteSerializer()
    db = FileDatabase(serializer=serializer, file_manager=file_manager)
    controller = NoteController(db)

if __name__ == "__main__":
    main()
