from pymongo import MongoClient
import os

class Database:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")  # Connect to MongoDB
        self.db = self.client["NebulaHeaven"]  # Database name
        self.collection = self.db["files"]  # Collection name

    def add_file(self, file_path):
        file_data = {"path": file_path}
        self.collection.insert_one(file_data)  # Insert file info into MongoDB

    def download_file(self, file_path, save_location):
        file_data = self.collection.find_one({"path": file_path})
        if file_data:
            with open(save_location, "wb") as file:
                file.write(file_data["data"])  # Save the file
        else:
            print("File not found in database.")

    def delete_file(self, file_path):
        self.collection.delete_one({"path": file_path})  # Delete file from MongoDB
