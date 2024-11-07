from sqlalchemy.orm import Session
from models import friend
from app.schemas import friend_schemas

def send_friend_request(db: Session, sender_id: int, receiver_id: int):
    db_request = friend.FriendRequest(sender_id=sender_id, receiver_id=receiver_id)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def approve_friend_request(db: Session, request_id: int):
    friend_request = db.query(friend.FriendRequest).filter_by(id=request_id, status=0).first()
    if friend_request:
        friend_request.status = 1
        db_friend = friend.UserFriend(user_id=friend_request.sender_id, friend_id=friend_request.receiver_id)
        db.add(db_friend)
        db.commit()
    return friend_request

def deny_friend_request(db: Session, request_id: int):
    friend_request = db.query(friend.FriendRequest).filter_by(id=request_id, status=0).first()
    if friend_request:
        friend_request.status = 2
        db.commit()
    return friend_request

def show_friend_profile(db: Session, user_id: int, friend_id: int):
    return db.query(friend.UserFriend).filter_by(user_id=user_id, friend_id=friend_id).first()

def get_friends(db: Session, user_id: int):
    return db.query(friend.UserFriend).filter_by(user_id=user_id).all()
