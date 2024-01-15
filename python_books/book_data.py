from pydantic import BaseModel

class Book(BaseModel):
    title : str
    author : str
    publisher : str
    publication_date : str
    isbn : int
    genre : str
    pages : int