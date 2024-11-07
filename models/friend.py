from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base


class UserFriend(Base):
    __tablename__ = "user_friends"
    __table_args__ = {'extend_existing': True}

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    friend_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

class FriendRequest(Base):
    __tablename__ = "friend_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Integer, default=0)  # 0 - Pending, 1 - Approved, 2 - Denied
