from sqlalchemy import Column, DateTime, ForeignKey, Integer, Table, Text, func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Tweet(Base):
    """
    Represents a tweet in the database.

    Attributes:
        id (int): The unique identifier of the tweet.
        content (str): The content of the tweet.
        created_at (datetime): The date and time when the tweet was created.
        author_id (int): The ID of the user who created the tweet.
        author (User): The User object associated with the tweet.
        media (list[Media]): The list of Media objects associated with the tweet.
        likes (list[User]): The list of User objects who have liked the tweet.
    """
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.timezone('UTC', func.now()))
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    author = relationship('User', back_populates='tweets', lazy="selectin")
    media = relationship(
        'Media',
        secondary='tweet_media_association',
        back_populates='tweet',
        lazy="selectin",
        cascade="all, delete"
    )
    likes = relationship(
        'User',
        secondary='tweet_likes',
        back_populates='liked_tweets',
        lazy="selectin"
    )


tweet_likes = Table(
    'tweet_likes',
    Base.metadata,
    Column('tweet_id', Integer, ForeignKey('tweets.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)
