from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, TEXT

Base = declarative_base()

class Idol(Base):
    __tablename__ = 'idol'

    id = Column(Integer, primary_key=True)
    stage_name = Column(VARCHAR(255))
    full_name = Column(VARCHAR(255))
    korean_name = Column(VARCHAR(255))
    idol_group = Column(VARCHAR(255))
    country = Column(VARCHAR(255))
    gender = Column(VARCHAR(255))

    image_urls = relationship('Idol_Picture', back_populates='idol')


class Idol_Picture(Base):
    __tablename__ = 'idol_picture'

    id = Column(Integer, primary_key=True)
    idol_id = Column(Integer, ForeignKey("idol.id"))
    url = Column(TEXT)

    idol = relationship('Idol', back_populates='image_urls')


class User(Base):
    __tablename__ = 'user_account'

    id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(255))


class Server(Base):
    __tablename__ = 'discord_server'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255))


class User_Server(Base):
    __tablename__ = 'user_server'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user_account.id"), primary_key=True)
    server_id = Column(Integer, ForeignKey("discord_server.id"), primary_key=True)
    server_profile_name = Column(TEXT)
    collection_name = Column(TEXT)

    user = relationship("User", backref="user_server")
    server = relationship("Server", backref="user_server")


class Idol_Server(Base):
    __tablename__ = 'idol_server'

    id = Column(Integer, primary_key=True, autoincrement=True)
    idol_id = Column(Integer, ForeignKey("idol.id"), primary_key=True)
    user_server_id = Column(Integer, ForeignKey("user_server.id"), primary_key=True)
    server_id = Column(Integer, ForeignKey("discord_server.id"), primary_key=True)
    status = Column(TEXT)

    idol = relationship("Idol", backref="idol_server")
    user_server = relationship("User_Server", backref="idol_server")
    server = relationship("Server", backref="idol_server")