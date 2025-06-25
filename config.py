import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb+srv://nitin:b9rYtx8ARITfRuXA@test-cluster.4j2vnrc.mongodb.net/?retryWrites=true&w=majority&appName=test-cluster")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "test-cluster")
    
    # Web scraping settings
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    REQUEST_TIMEOUT = 30
    MAX_RETRIES = 3