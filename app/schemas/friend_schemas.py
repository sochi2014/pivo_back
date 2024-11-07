from pydantic import BaseModel

class FriendRequestCreate(BaseModel):
    receiver_id: int

class FriendRequestResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    status: int

    class Config:
        orm_mode = True

class UserFriendResponse(BaseModel):
    user_id: int
    friend_id: int

    class Config:
        orm_mode = True
