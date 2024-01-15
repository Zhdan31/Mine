from pymongo import MongoClient

def test_mongo_connection():
    try:
        client = MongoClient("mongodb+srv://zhdan:HKLIDp7feZTKTWFz@cluster0.jty3nsg.mongodb.net/retryWrites=true&w=majority")
        db = client.book_db
        
        collection_name = db["books"]

        print("Connection to book Db successful.")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = test_mongo_connection()

    if success:
        print("MongoDB tests passed.")
    else:
        print("MongoDB tests failed.")