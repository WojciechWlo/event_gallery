from dotenv import load_dotenv
import os

load_dotenv()  # ładuje zmienne z .env

DEBUG = os.getenv("DEBUG", "False")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8000")
GUEST_NAME = os.getenv("GUEST_NAME", "Guest")
GUEST_PASSWORD = os.getenv("GUEST_PASSWORD", "pass")