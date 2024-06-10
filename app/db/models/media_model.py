from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base

tweet_media_association = Table(
    'tweet_media_association',
    Base.metadata,
    Column('tweet_id', Integer, ForeignKey('tweets.id'), primary_key=True),
    Column('media_id', Integer, ForeignKey('media.id'), primary_key=True)
)


class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)
    tweet = relationship(
        "Tweet",
        secondary=tweet_media_association,
        back_populates="media",
    )
