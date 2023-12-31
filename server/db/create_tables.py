from .models import Base
from . import engine

def create_tables():
    print('Creating all tables specified in the models file')
    with engine.connect() as connection:
        Base.metadata.drop_all(connection)
        Base.metadata.create_all(connection)