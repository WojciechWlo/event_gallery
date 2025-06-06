from dotenv import load_dotenv
import os

load_dotenv()  # ładuje zmienne z .env

DEBUG = os.getenv("DEBUG", None)
APP_ENV = os.getenv("APP_ENV", None)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8000")
GUEST_NAME = os.getenv("GUEST_NAME", "Guest")
GUEST_PASSWORD = os.getenv("GUEST_PASSWORD", "pass")
SSL_KEYFILE = os.getenv("SSL_KEYFILE", None)
SSL_CERTFILE = os.getenv("SSL_CERTFILE", None)