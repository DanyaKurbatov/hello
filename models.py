from db import Base
from sqlalchemy import Column, String, Integer


class Name(Base):
    __tablename__ = 'names'

    name = Column(String)
    id = Column(Integer, primary_key=True, index=True, unique=True)
