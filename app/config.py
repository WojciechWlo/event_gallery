from dotenv import load_dotenv
import os

load_dotenv()

DEBUG = os.getenv("DEBUG", None)
APP_ENV = os.getenv("APP_ENV", None)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8000")
EVENT_GALLERY_HOST = os.getenv("EVENT_GALLERY_HOST", "0.0.0.0")
EVENT_GALLERY_PORT = int(os.getenv("EVENT_GALLERY_PORT", 8000))
SSL_KEYFILE = os.getenv("SSL_KEYFILE", None)
SSL_CERTFILE = os.getenv("SSL_CERTFILE", None)