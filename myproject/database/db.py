from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DB_URL = 'postgresql://postgres:admin@localhost/glovo_app'

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass