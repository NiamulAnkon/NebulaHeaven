from pymongo import MongoClient
import gridfs
import os

class Database:
    def __init__(self):
        # Connect to MongoDB
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["NebulaHeavenDB"]
        self.fs = gridfs.GridFS(self.db)  # GridFS for file storage
        self.collection = self.db["files"]  # Collection for file metadata

    def add_file(self, file_path):
        """ Store a file in MongoDB """
        if not os.path.exists(file_path):
            print("File not found!")
            return
        
        filename = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            file_id = self.fs.put(f, filename=filename)

        file_metadata = {
            "filename": filename,
            "file_id": file_id,
            "original_path": file_path
        }
        self.collection.insert_one(file_metadata)
        print(f"File '{filename}' added successfully.")

    def download_file(self, filename, save_path):
        """ Retrieve a file from MongoDB and save it locally """
        file_metadata = self.collection.find_one({"filename": filename})
        if not file_metadata:
            print("File not found in database!")
            return

        file_data = self.fs.get(file_metadata["file_id"])
        with open(os.path.join(save_path, filename), "wb") as f:
            f.write(file_data.read())
        
        print(f"File '{filename}' downloaded successfully to {save_path}")

    def delete_file(self, filename):
        """ Delete a file from MongoDB """
        file_metadata = self.collection.find_one({"filename": filename})
        if not file_metadata:
            print("File not found in database!")
            return
        
        self.fs.delete(file_metadata["file_id"])  # Remove file from GridFS
        self.collection.delete_one({"filename": filename})  # Remove metadata
        print(f"File '{filename}' deleted successfully.")

    def list_files(self):
        """ List all stored files """
        files = self.collection.find()
        for file in files:
            print(f"- {file['filename']} (ID: {file['file_id']})")