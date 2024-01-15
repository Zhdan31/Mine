from fastapi.testclient import TestClient
from mongo_book import app
import pytest

client = TestClient(app)

#Body for test data
@pytest.fixture
def test_post_book_data():
    return {
        "title": "Test Book",
        "author": "Test Author",
        "publisher": "Test Publisher",
        "publication_date": "2022-01-01",
        "isbn": 1234567890, 
        "genre": "Fiction",
        "pages": 200
    }

def test_post_book(test_post_book_data):
    response = client.post("/book", json=test_post_book_data)
    assert response.status_code == 200
    assert "id" in response.json()

#def test_get_all_books():
#    response = client.get("/book")
#    assert response.status_code == 200
#    assert isinstance(response.json(), list)
#
#def test_put_book(test_post_book_data):
#    # Create a book using the test_post_book_data schema
#    post_response = client.post("/book", json=test_post_book_data)
#    assert post_response.status_code == 200
#
#    # Extract the book_id from the response of the POST request
#    book_id = post_response.json()["id"]
#
#    updated_data = {
#        "title": "Test Updated Book",
#        "author": "Test Updated Author",
#        "publisher": "Test Updated Publisher",
#        "publication_date": "2022-02-02",
#        "isbn": 1234567892, 
#        "genre": "Updated Fiction",
#        "pages": 202
#    }
#
#    put_response = client.put(f"/book/{book_id}", json=updated_data)
#    assert put_response.status_code == 200
#    assert put_response.json() == {"message": "Book updated successfully"}
#
#def test_delete_book(test_post_book_data):
#    post_response = client.post("/book", json=test_post_book_data)
#    assert post_response.status_code == 200
#
#    book_id = post_response.json()["id"]
#
#    delete_response = client.delete(f"/book/{book_id}")
#    assert delete_response.status_code == 200
#    assert delete_response.json() == {"message": "Book deleted successfully"}

if __name__ == "__main__":
    exit_code = pytest.main(["-v", __file__])
    
    if exit_code == 0:
        print("All tests passed.")
    else:
        print("Some tests failed.")
