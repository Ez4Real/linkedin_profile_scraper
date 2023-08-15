from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from config import DB_NAME, DB_USER, DB_PASSWORD, dotenv_path

load_dotenv(dotenv_path)

class Database:
    def __init__(self, mongo_uri: str, db_name: str):
        self.client = AsyncIOMotorClient(mongo_uri)
        self.db = self.client.get_database(db_name)
        
    def get_user_collection(self):
        return self.db["users"]

    def get_scrape_sites_collection(self):
        return self.db["scrape_sites"]

uri = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@webharvesthub.fvnkinf.mongodb.net/?retryWrites=true&w=majority"

db = Database(uri, DB_NAME)

user_collection = db.get_user_collection()