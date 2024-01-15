from fastapi import FastAPI
from book_route import book_router

app = FastAPI()

app.include_router(book_router)

# uvicorn app_book:app --reload --port 8000