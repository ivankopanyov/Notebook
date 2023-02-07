"""Модуль репозиториев."""

from .base.repositories import BaseRepository
from .base.models import BaseModel
from .base.serializers import BaseSerializer
from .file import FileManager


class FileRepository(BaseRepository):
    """Класс, описывающий репозиторий, хранящий объекты в файле."""

    __cache__: list[BaseModel] = None
    """Кэш объектов."""

    __current_id__: int = 0
    """Текущий идентификатор для присвоения новому объекту."""

    def __init__(self, 
                serializer: BaseSerializer, 
                file_manager: FileManager) -> None:
        """Инициализация объекта репозитория."""
        self.serializer = serializer
        self.file_manager = file_manager

    def select(self, id: int) -> BaseModel:
        """Метод получения объекта из репозитория."""
        if self.__cache__ == None:
            self.__get_cache__()
        for note in self.__cache__:
            if note.id == id:
                return note
        return None

    def select_all(self) -> list[BaseModel]:
        """Метод получения всех объектов из репозитория."""
        if self.__cache__ == None:
            self.__get_cache__()
        return self.__cache__

    def insert(self, entity: BaseModel) -> None:
        """Метод добавления объекта в репозиторий."""
        if self.__current_id__ == 0:
            self.__get_current_id__()
        entity.id = self.__current_id__
        if self.__cache__ == None:
            self.__get_cache__()
        self.__cache__.append(entity)
        self.__set_cache__()
        self.__current_id__ += 1

    def update(self, entity: BaseModel) -> None:
        """Метод изменения объекта в репозитории."""
        if self.__cache__ == None:
            self.__get_cache__()
        for item in self.__cache__:
            if item.id == entity.id:
                self.__cache__.remove(item)
                self.__cache__.append(entity)
                self.__set_cache__()
                break

    def delete(self, id: int) -> None:
        """Метод удаления объекта из репозитория."""
        if self.__cache__ == None:
            self.__get_cache__()
        for note in self.__cache__:
            if note.id == id:
                self.__cache__.remove(note)
                self.__set_cache__()
                break

    def __get_cache__(self):
        """Метод получения объектов из файла."""
        data = self.file_manager.read()
        self.__cache__ = self.serializer.decode(data) if data != None else []
    
    def __set_cache__(self):
        """Метод записи объектов в файл."""
        data = self.serializer.encode(self.__cache__)
        self.file_manager.write(data)

    def __get_current_id__(self):
        """Метод получения текущего идентификатора."""
        if self.__cache__ == None:
            self.__get_cache__()
        if len(self.__cache__) == 0:
            self.__current_id__ = 1
            return
        self.__current_id__ = self.__cache__[-1].id + 1
