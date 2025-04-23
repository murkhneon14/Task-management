import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient("mongodb+srv://nectarsof:abha5UstEPZmtXQF@cluster0.kx0ampt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["taskdb"]
task_collection = db["tasks"]

async def check_db_connection():
    try:
        await client.admin.command('ping')
        print("MongoDB connection successful.")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
