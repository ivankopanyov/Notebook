from models import BaseModel
from serializers import BaseSerializer

class Database:

    __cache__: list[BaseModel] = None
    __current_id__: int = 0

    def __init__(self, serializer: BaseSerializer) -> None:
        self.serializer = serializer

    @classmethod
    def select(self, id: int) -> BaseModel | None:
        if self.__cache__ == None:
            self.__get_cache__()
        for note in self.__cache__:
            if note.id == id:
                return note
        return None

    @classmethod
    def select_all(self) -> list[BaseModel]:
        if self.__cache__ == None:
            self.__get_cache__()
        return self.__cache__

    @classmethod
    def insert(self, note: BaseModel) -> None:
        if type(note != BaseModel):
            return
        if self.__current_id__ == 0:
            self.__get_last_id__()
        note.id = self.__current_id__
        if self.__cache__ == None:
            self.__get_cache__()
        self.__cache__.append(note)
        self.__set_cache__()

    @classmethod
    def update(self, note: BaseModel) -> None:
        if type(note) != BaseModel:
            return
        if self.__cache__ == None:
            self.__get_cache__()
        for item in self.__cache__:
            if item.id == note.id:
                self.__cache__.remove(item)
                self.__cache__.append(note)
                self.__set_cache__()
                break

    @classmethod
    def delete(self, id: int) -> None:
        if self.__cache__ == None:
            self.__get_cache__()
        for note in self.__cache__:
            if note.id == id:
                self.__cache__.remove(note)
                self.__set_cache__()
                break

    def __get_cache__(self):
        pass
    
    def __set_cache__(self):
        pass

    def __get_last_id__(self):
        if self.__cache__ == None:
            self.__get_cache__()
        self.__current_id__ = self.__cache__[-1].id + 1
