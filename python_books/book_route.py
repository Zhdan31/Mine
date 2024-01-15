from fastapi import APIRouter, HTTPException
from book_data import Book
from book_db import collection_name
from book_schema import list_serial
from bson import ObjectId
import logging

book_router = APIRouter()

# POST Request Method
@book_router.post("/book")
async def post_book(book: Book):
    try:
        result = collection_name.insert_one(dict(book))
        return {"id": str(result.inserted_id)}
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# GET Request Method
@book_router.get("/book")
async def get_all_books():
    try:
        books = list_serial(collection_name.find())
        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# PUT Request Method
@book_router.put("/book/{id}")
async def put_book(id: str, book: Book):
    try:
        result = collection_name.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": dict(book)}
        )
        if result is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return {"message": "Book updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# DELETE Request Method
@book_router.delete("/book/{id}")
async def delete_book(id: str):
    try:
        result = collection_name.find_one_and_delete({"_id": ObjectId(id)})
        if result is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return {"message": "Book deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))