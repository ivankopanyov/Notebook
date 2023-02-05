from models import BaseModel
from serializers import BaseSerializer
from file import FileManager


class Database:

    def select(self, id: int) -> BaseModel | None:
        pass

    def select_all(self) -> list[BaseModel]:
        pass

    def insert(self, entity: BaseModel) -> None:
        pass

    def update(self, entity: BaseModel) -> None:
        pass

    def delete(self, id: int) -> None:
        pass


class FileDatabase(Database):

    __cache__: list[BaseModel] = None
    __current_id__: int = 0

    def __init__(self, 
                serializer: BaseSerializer, 
                file_manager: FileManager) -> None:
        self.serializer = serializer
        self.file_manager = file_manager

    def select(self, id: int) -> BaseModel | None:
        if self.__cache__ == None:
            self.__get_cache__()
        for note in self.__cache__:
            if note.id == id:
                return note
        return None

    def select_all(self) -> list[BaseModel]:
        if self.__cache__ == None:
            self.__get_cache__()
        return self.__cache__

    def insert(self, entity: BaseModel) -> None:
        # if type(entity != BaseModel):
        #     return
        if self.__current_id__ == 0:
            self.__get_current_id__()
        entity.id = self.__current_id__
        if self.__cache__ == None:
            self.__get_cache__()
        self.__cache__.append(entity)
        self.__set_cache__()
        self.__current_id__ += 1

    def update(self, entity: BaseModel) -> None:
        # if type(entity) != BaseModel:
        #     return
        if self.__cache__ == None:
            self.__get_cache__()
        for item in self.__cache__:
            if item.id == entity.id:
                self.__cache__.remove(item)
                self.__cache__.append(entity)
                self.__set_cache__()
                break

    def delete(self, id: int) -> None:
        if self.__cache__ == None:
            self.__get_cache__()
        for note in self.__cache__:
            if note.id == id:
                self.__cache__.remove(note)
                self.__set_cache__()
                break

    def __get_cache__(self):
        data = self.file_manager.read()
        self.__cache__ = self.serializer.encode(data)
    
    def __set_cache__(self):
        data = self.serializer.decode(self.__cache__)
        self.file_manager.write(data)

    def __get_current_id__(self):
        if self.__cache__ == None:
            self.__get_cache__()
        if len(self.__cache__) == 0:
            self.__current_id__ = 1
            return
        self.__current_id__ = self.__cache__[-1].id + 1
