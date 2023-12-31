from .models import Base
from . import engine

def create_tables():
    with engine.connect() as connection:
        Base.metadata.create_all(connection)
    
    
if __name__ == "__main__":
    create_tables()