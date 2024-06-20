from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, TEXT

Base = declarative_base()

class Server(Base):
    __tablename__ = 'discord_server'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255))