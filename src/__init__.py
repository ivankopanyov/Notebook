"""Основной модуль приложения."""

from .serializers import JsonNoteSerializer
from .file import FileManager
from .controllers import NoteController
from .repositories import FileRepository
from .settings import DB_FILE_NAME


def run():
    """Функция запуска приложения."""
    controller = __build__()
    __start__(controller)


def __build__() -> NoteController:
    """Функция сборки приложения."""
    file_manager = FileManager(DB_FILE_NAME)
    serializer = JsonNoteSerializer()
    repository = FileRepository(serializer=serializer, file_manager=file_manager)
    return NoteController(repository)


def __start__(controller: NoteController) -> None:
    """Функция старта приложения."""
    action = lambda: controller.get_all()
    while True:
        view = action()
        action = view.show()
