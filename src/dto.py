"""Модуль классов трансфер объектов."""

class SimpleNoteDto:
    """Класс, описывающий объект, хранящий полезные данные заметки."""

    def __init__(self, name: str, body: str) -> None:
        """Инициализация объекта."""
        self.name = name
        self.body = body


class NoteDto:
    """Класс, описывающий объект, хранящий все данные заметки."""

    def __init__(self,
                id: int, 
                name: str, 
                body: str, 
                create_date: str, 
                update_date: str) -> None:
        """Инициализация объекта."""
        self.id = id
        self.name = name
        self.body = body
        self.create_date = create_date
        self.update_date = update_date
