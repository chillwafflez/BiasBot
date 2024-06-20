from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, TEXT

Base = declarative_base()

class User(Base):
    __tablename__ = 'user_account'

    id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(255))


class User_Server(Base):
    __tablename__ = 'user_server'

    id = Column(Integer)
    user_id = Column(Integer, ForeignKey("user_account.id"), primary_key=True)
    server_id = Column(Integer, ForeignKey("discord_server.id"), primary_key=True)
    server_profile_name = Column(TEXT)
    collection_name = Column(TEXT)