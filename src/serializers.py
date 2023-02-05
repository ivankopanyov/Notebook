from datetime import datetime
import json

from models import Note


class BaseSerializer:

    def decode(self, objects: list[object]):
        pass
    
    def encode(self, data: str) -> list[object]:
        pass


class JsonNoteSerializer(BaseSerializer):

    def decode(self, objects: list[Note]) -> str:
        result = []
        for note in objects:
            result.append({
                "id": note.id,
                "name": note.name,
                "body": note.body,
                "create_date": f"{note.create_date:%d.%m.%Y %H:%M:%S}",
                "update_date": f"{note.update_date:%d.%m.%Y %H:%M:%S}"
        })
        return json.dumps(result)

    def encode(self, data: str) -> list[Note]:
        result = []
        for note in json.loads(data):
            result.append(Note(
                id=note["id"],
                name=note["name"],
                body=note["body"],
                create_date=datetime.strptime(note["create_date"], "%d.%m.%Y %H:%M:%S"),
                update_date=datetime.strptime(note["update_date"], "%d.%m.%Y %H:%M:%S")
            ))
        return result
