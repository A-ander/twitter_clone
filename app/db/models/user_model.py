from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from app.db.database import Base

user_followers = Table(
    'user_followers',
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('followed_id', Integer, ForeignKey('users.id'), primary_key=True)
)


class User(Base):
    """
    Represents a user in the database.

    Attributes:
        id (int): The unique identifier of the user.
        name (str): The name of the user.
        api_key (str): The API key associated with the user.
        tweets (list[Tweet]): The list of Tweet objects created by the user.
        liked_tweets (list[Tweet]): The list of Tweet objects liked by the user.
        followers (list[User]): The list of User objects following the user.
        following (list[User]): The list of User objects the user is following.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    api_key = Column(Text, unique=True)

    tweets = relationship('Tweet', back_populates='author', lazy='selectin')
    liked_tweets = relationship('Tweet', secondary='tweet_likes', back_populates='likes', lazy='selectin')

    followers = relationship(
        'User',
        secondary=user_followers,
        primaryjoin=(id == user_followers.c.followed_id),
        secondaryjoin=(id == user_followers.c.follower_id),
        back_populates='following',
        lazy='selectin'
    )
    following = relationship(
        'User',
        secondary=user_followers,
        primaryjoin=(id == user_followers.c.follower_id),
        secondaryjoin=(id == user_followers.c.followed_id),
        back_populates='followers',
        lazy='selectin'
    )
