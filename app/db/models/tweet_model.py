from sqlalchemy import Column, DateTime, ForeignKey, Integer, Table, Text, func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.timezone('UTC', func.now()))
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    author = relationship('User', back_populates='tweets')
    media = relationship('Media', back_populates='tweets')
    likes = relationship('User', secondary='tweet_likes', back_populates='liked_tweets')


tweet_likes = Table(
    'tweet_likes',
    Base.metadata,
    Column('tweet_id', Integer, ForeignKey('tweets.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)
