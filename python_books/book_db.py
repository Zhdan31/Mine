from pymongo import MongoClient

client = MongoClient("mongodb+srv://zhdan:HKLIDp7feZTKTWFz@cluster0.jty3nsg.mongodb.net/retryWrites=true&w=majority")

db = client.book_db

collection_name = db["books"]