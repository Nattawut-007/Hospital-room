import os
from dotenv import load_dotenv

load_dotenv()  # โหลด .env เข้า environment

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    MONGODB_SETTINGS = {
        'db': os.getenv('MONGO_DB_NAME'),
        'host': os.getenv('MONGO_HOST', 'localhost'),
        'port': int(os.getenv('MONGO_PORT', 27017))
    }
