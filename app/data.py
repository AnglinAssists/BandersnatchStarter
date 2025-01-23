from os import getenv
import random
from pymongo import MongoClient
from MonsterLab import Monster
from dotenv import load_dotenv
import pandas as pd
from certifi import where

client = MongoClient(getenv("DB_URL"), tlsCAFile=where())
db = client['Database']
monsters_collection = db['monsters']


class Database:
    ''' The Database allows us to generate and
      manipulate random monster data'''
    def __init__(self,collection ):
        # Load environmental variables
        load_dotenv()

        # Create a connection to the MongoDB server
        self.client = client

        # Select the database
        self.db = self.client['Database']

        # Select the collection
        self.collection = self.db['Monsters']


    def reset(self):
        '''The reset function is called after init in order to
        drop all previous data before adding more'''
        self.collection.drop()


    def seed(self, num_docs):
        '''The seed function is used to genreate a specified
        number of documents into our collection'''
        monsters = [self.get_random_monster_name() for _ in range(num_docs)]
        self.collection.insert_many(monsters)


    def count(self):
        '''The Count function returns a count of the documents
        we just generated to ensure accuracy'''
        return self.collection.count_documents({})


    def dataframe(self):
        '''The dataframe function returns a dataframe containing our new collection'''
        return pd.DataFrame(list(self.collection.find()))


    def html_table(self):
        '''The html_table function converts our new dataframe into HTML format'''
        df = self.dataframe()
        if df.empty:
            return None
        return df.to_html()


    def get_random_monster_name(self):
        '''The get_random_monster_name function ensures that
        names are creates with two words each'''
        monster = Monster()  # Create a new monster instance
        name = monster.name
        if ' ' not in name:  # Check if the name has a space
            suffixes = ['Spirit', 'Ghost', 'Entity', 'Being']  # List of suffixes
            name += ' ' + random.choice(suffixes)  # Add a suffix
        return {'Name': name}  # Return a single dictionary

    def read_one(self, query: Dict) -> Dict:
        return self.collection.find_one(query, {"_id": False})

    def update_one(self, query: Dict, update: Dict) -> bool:
        return self.collection.update_one(query, {"$set": update}).acknowledged

    def delete_one(self, query: Dict) -> bool:
        return self.collection.delete_one(query).acknowledged

    def create_many(self, records: Iterable[Dict]) -> bool:
        return self.collection.insert_many(records).acknowledged

    def read_many(self, query: Dict) -> Iterator[Dict]:
        return self.collection.find(query, {"_id": False})

    def update_many(self, query: Dict, update: Dict) -> bool:
        return self.collection.update_many(query, {"$set": update}).acknowledged

    def delete_many(self, query: Dict) -> bool:
        return self.collection.delete_many(query).acknowledged

# This is an example of how to use the bandersnatch file
if __name__ == '__main__':
    db_database = database(monsters_collection)
    db_database.reset()  # Remove previous data
    db_database.seed(1000)  # Insert 1000 random monsters
    print(f"{db_database.count()} monsters have been inserted.")
    print(db_database.dataframe())  # Display the DataFrame
    print(db_database.html_table())  # Display the HTML table