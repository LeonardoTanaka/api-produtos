from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:123456@localhost:5432/projeto"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)