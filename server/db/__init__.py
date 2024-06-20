from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")

if not DB_URL:
    print("DB_URL environment variable is not set !")
    sys.exit(0)

engine = create_engine(DB_URL, echo=True)

SessionLocal = sessionmaker(engine, autoflush=False, autocommit=False)
