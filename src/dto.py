from datetime import datetime


class NoteDto:

    def __init__(self, 
                name: str, 
                body: str):
        self.name = name
        self.body = body
