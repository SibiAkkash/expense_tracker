from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()


DB_NAME = "transactions.db"
DIR_ROOT = Path(__file__).parent.parent.parent
DB_PATH = os.getenv("DB_PATH", f"sqlite:///{DIR_ROOT / DB_NAME}")

engine = create_engine(DB_PATH, connect_args={"check_same_thread": False}, echo=True)

SessionLocal = sessionmaker(engine, autoflush=False, autocommit=False)


# Foreign key support must be explicitly enabled for each sqlite connection
# Enabling Foreign Key Support: https://www.sqlite.org/foreignkeys.html
# https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#foreign-key-support

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dpapi_connection, connection_record):
    cursor = dpapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()