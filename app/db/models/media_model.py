from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    file = Column(String)
    type = Column(String(10))
    tweet_id = Column(String, ForeignKey('tweets.id'), nullable=False)
    tweets = relationship('Tweet', back_populates='media')
    