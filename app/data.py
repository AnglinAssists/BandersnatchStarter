from os import getenv
from pymongo import MongoClient
from MonsterLab import Monster
from dotenv import load_dotenv
import pandas as pd
from certifi import where


class Database:
    """
    A Database class to manage a MongoDB database connection and provide CRUD functionality
    on a specific collection.

    CRUD Operations:
        - Create: Insert documents into the database (e.g., `create`, `seed` methods).
        - Read: Read documents from the database (e.g., `read_all`, `read_one`, `dataframe` methods).
        - Update: Update existing documents in the collection (e.g., `update_one` method).
        - Delete: Remove documents from the collection (e.g., `delete_one`, `reset` methods).
    """

    load_dotenv()
    database = MongoClient(getenv("DB_URL"), tlsCAFile=where())["Database"]

    def __init__(self, collection: str):
        """
        Initialize the database object with a specific collection name.

        Args:
            collection (str): The name of the collection to work with in the database.
        """
        self.collection = self.database[collection]

    # Create Functionality
    def create(self, document: dict) -> bool:
        """
        Insert a single document into the collection.

        Args:
            document (dict): The document to insert into the collection.

        Returns:
            bool: True if the insertion was acknowledged, False otherwise.
        """
        result = self.collection.insert_one(document)
        return result.acknowledged

    def seed(self, amount: int) -> bool:
        """
        Bulk-insert multiple randomly generated Monster objects into the collection.

        Args:
            amount (int): The number of Monster objects to insert.

        Returns:
            bool: True if the insertion was acknowledged, False otherwise.
        """
        monsters = [Monster().to_dict() for _ in range(1, amount + 1)]
        result = self.collection.insert_many(monsters)
        return result.acknowledged

    # Read Functionality
    def read_all(self) -> list:
        """
        Retrieve all documents from the collection.

        Returns:
            list: A list of all documents in the collection as dictionaries.
        """
        return list(self.collection.find({}, {"_id": 0}))

    def read_one(self, query: dict) -> dict:
        """
        Retrieve a single document from the collection that matches the query.

        Args:
            query (dict): The query used to find a document.

        Returns:
            dict: A dictionary representing the matching document, or None if no match is found.
        """
        return self.collection.find_one(query, {"_id": 0})

    def dataframe(self) -> pd.DataFrame:
        """
        Retrieve all documents and their attributes from the collection as a pandas DataFrame.

        Returns:
            pandas.DataFrame: A DataFrame containing all the document data.
        """
        data = self.read_all()
        return pd.DataFrame(data)

    # Update Functionality
    def update_one(self, query: dict, update_values: dict) -> bool:
        """
        Update specific fields in a single document that matches the query.

        Args:
            query (dict): The query to match the document to update.
            update_values (dict): A dictionary of fields to update, e.g., {"$set": {"field_name": "new_value"}}.

        Returns:
            bool: True if the update was acknowledged, False otherwise.
        """
        result = self.collection.update_one(query, update_values)
        return result.acknowledged

    # Delete Functionality
    def delete_one(self, query: dict) -> bool:
        """
        Delete a single document from the collection that matches the query.

        Args:
            query (dict): The query to match the document to delete.

        Returns:
            bool: True if the deletion was acknowledged, False otherwise.
        """
        result = self.collection.delete_one(query)
        return result.acknowledged

    def reset(self) -> bool:
        """
        Delete all documents from the collection.

        Returns:
            bool: True if the deletion was acknowledged, False otherwise.
        """
        result = self.collection.delete_many({})
        return result.acknowledged

    # Other Utility Functions
    def count(self) -> int:
        """
        Count the number of documents in the collection.

        Returns:
            int: The total number of documents in the collection.
        """
        return self.collection.count_documents({})

    def html_table(self) -> str:
        """
        Convert the collection's documents into an HTML table.

        Uses the `dataframe` method to retrieve data and convert it into an HTML table.

        Returns:
            str: An HTML string representation of the collection data.
        """
        return self.dataframe().to_html()


if __name__ == '__main__':
    db = Database("monsters")
    db.reset()
    db.seed(1000)

    # Example usages of CRUD operations:
    print(db.count())
    print("Inserting a new monster...")
    new_monster = {"name": "FaKE Monster", "type": "Fire", "strength": 85}
    db.create(new_monster)

    print("Reading a specific document...")
    print(db.read_one({"name": "FaKE Monster"}))

    print("Updating the monster's strength...")
    db.update_one({"name": "FaKE Monster"}, {"$set": {"strength": 95}})
    print(db.read_one({"name": "FaKE Monster"}))

    print("Deleting the monster...")
    db.delete_one({"name": "FaKE Monster"})
    print(f"Document count after deletion: {db.count()}")

    print("HTML Table of all data:")
    print(db.html_table())
    print(db.dataframe())

