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