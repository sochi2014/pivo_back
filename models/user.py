from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
import datetime
from app.database import Base


user_friends = Table(
    'user_friends',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('friend_id', Integer, ForeignKey('users.id'), primary_key=True)
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    level_id = Column(Integer, ForeignKey(
        "levels.id"), nullable=False, default=1)
    username = Column(String, unique=False, index=False, nullable=False)
    email = Column(String, unique=True, index=True)
    avatar_url = Column(String, nullable=True)
    register_at = Column(DateTime, default=datetime.datetime.utcnow)
    phone_number = Column(String)
    level = relationship("Level", back_populates="users")
    auth_codes = relationship("AuthCode", back_populates="user")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    feedbacks = relationship('Feedback', back_populates='user')
    friends = relationship(
        'User',
        secondary=user_friends,
        primaryjoin=id == user_friends.c.user_id,
        secondaryjoin=id == user_friends.c.friend_id,
        backref='added_by'
    )
