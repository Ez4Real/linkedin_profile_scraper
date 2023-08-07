import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv('config/.env')

class Database:
    def __init__(self, mongo_uri: str):
        self.client = AsyncIOMotorClient(mongo_uri)
        self.db = self.client.get_database()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

uri = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@webharvesthub.fvnkinf.mongodb.net/?retryWrites=true&w=majority"

db = Database("mongodb://localhost:27017")