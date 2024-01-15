def individual_serial(book)->dict:
    return {
        "Id": str(book["_id"]),
        "Title": book["title"],
        "Author": book["author"],
        "Publisher": book["publisher"],
        "Publication date":book["publication_date"],
        "Isbn": book["isbn"],
        "Genre": book["genre"],
        "Pages": book["pages"]
    }

def list_serial(books)-> list:
    return[individual_serial(book) for book in books]