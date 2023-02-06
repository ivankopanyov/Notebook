from file import FileManager
from serializers import JsonNoteSerializer
from db import FileDatabase
from controllers import BaseController, NoteController


def run():
    controller = __build__()
    __start__(controller)


def __build__() -> BaseController:
    file_manager = FileManager("db.json")
    serializer = JsonNoteSerializer()
    db = FileDatabase(serializer=serializer, file_manager=file_manager)
    return NoteController(db)


def __start__(controller: BaseController) -> None:
    action = lambda: controller.get_all()
    while True:
        print(f"action = {type(action)}")
        view = action()
        
        print(f"view = {type(view)}")
        action = view.show()


if __name__ == "__main__":
    run()
