from datetime import datetime


class BaseModel:

    def __init__(self, 
                id: int = 0, 
                create_date: datetime = datetime.now(), 
                update_date: datetime = datetime.now()) -> None:
        if id != None:
            self.id = id
        self.create_date = create_date
        self.update_date = update_date


class Note(BaseModel):

    def __init__(self,
                id: int = 0, 
                name: str = '', 
                body: str = '', 
                create_date: datetime = datetime.now(), 
                update_date: datetime = datetime.now()):
        super().__init__(id, create_date, update_date)
        self.name = name
        self.body = body
