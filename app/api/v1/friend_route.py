from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud.friend_crud import send_friend_request, approve_friend_request, deny_friend_request, show_friend_profile, get_friends
from app.schemas.friend_schemas import FriendRequestCreate, FriendRequestResponse, UserFriendResponse
from app.dependencies import get_db
from app.crud.user_crud import get_current_user

router = APIRouter()

@router.post("/send_request", response_model=FriendRequestResponse)
def send_request(friend_request: FriendRequestCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return send_friend_request(db, sender_id=current_user.id, receiver_id=friend_request.receiver_id)

@router.post("/approve_request/{request_id}", response_model=FriendRequestResponse)
def approve_request(request_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    request = approve_friend_request(db, request_id=request_id)
    if not request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Friend request not found or already processed")
    return request

@router.post("/deny_request/{request_id}", response_model=FriendRequestResponse)
def deny_request(request_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    request = deny_friend_request(db, request_id=request_id)
    if not request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Friend request not found or already processed")
    return request

@router.get("/show_friend_profile/{friend_id}", response_model=UserFriendResponse)
def show_friend_profile(friend_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    friend = show_friend_profile(db, user_id=current_user.id, friend_id=friend_id)
    if not friend:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Friend not found")
    return friend

@router.get("/show_friends", response_model=list[UserFriendResponse])
def show_friends(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    friends = get_friends(db, user_id=current_user.id)
    return friends
