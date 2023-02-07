"""Модуль с классами для работы с файлами."""

import pathlib


class FileManager:
    """Класс, описывающий объект для работы с файлом."""

    def __init__(self, file_name: str) -> None:
        """Инициализация объекта для работы с переданным файлом."""
        self.file_name = file_name

    def read(self) -> str:
        """Метод чтения из файла."""
        if pathlib.Path(self.file_name).is_file():
            with open(self.file_name, 'r', encoding='utf8') as file:
                return file.read()
        else:
            return None

    def write(self, data: str) -> None:
        """Метод записи в файл."""
        with open(self.file_name, 'w') as file:
            file.write('')
        with open(self.file_name, 'a', encoding='utf8') as file:
            file.write(data)
