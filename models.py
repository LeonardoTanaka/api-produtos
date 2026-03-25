from sqlalchemy import Column, Integer, String, Float
from database import engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    preco = Column(Float)

Base.metadata.create_all(bind=engine)