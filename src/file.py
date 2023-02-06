import pathlib


class FileManager:

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def read(self) -> str | None:
        if pathlib.Path(self.file_name).is_file():
            with open(self.file_name, 'r', encoding='utf8') as file:
                return file.read()
        else:
            return None

    def write(self, data: str) -> None:
        with open(self.file_name, 'w', encoding='utf8') as file:
            file.write(data)
