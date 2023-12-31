from sqlalchemy import create_engine
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
