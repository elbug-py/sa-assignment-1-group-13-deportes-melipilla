import mongoengine
import dotenv
import os

dotenv.load_dotenv()

DB_NAME = os.getenv("DB_NAME", "library_db")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 27017))
DB_USER = os.getenv("DB_USER", None)


def connect_db():
    mongoengine.connect(
        db=DB_NAME,
        host=DB_HOST,
        port=DB_PORT,
        username=DB_USER,
    )

