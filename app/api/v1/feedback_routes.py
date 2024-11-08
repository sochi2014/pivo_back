import os
import pathlib
from typing import List, Optional
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload

from app.crud.level_crud import update_user_level
from app.crud.user_crud import get_current_user
from app.dependencies import get_db
from app.schemas.feedback_scheme import FeedbackOut, FeedbackCreate
from app.schemas.photo_scheme import PhotoOut
from app.schemas.beer_schemas import BeerOut
from app.schemas.place_scheme import PlaceOut
from app.schemas.user_scheme import UserReturnSchema
from models import Feedback, Photo, User, Place, Beer
_path_file = pathlib.Path(__file__)
PREFIX = f'/{_path_file.parent.parent.name}/{_path_file.parent.name}/{_path_file.stem}'

router = APIRouter(
    prefix=PREFIX
)

# async def upload_files(files: List[UploadFile] = File(...)):
#     file_urls = []
#     try:
#         for file in files:
#             unique_filename = f"{uuid4()}_{file.filename}"
#             file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
#
#             with open(file_path, "wb") as buffer:
#                 buffer.write(await file.read())
#
#             file_url = f"/static/uploads/{unique_filename}"
#             file_urls.append(file_url)
#
#         return {"file_urls": file_urls}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error uploading files: {e}")


@router.post("/create", response_model=FeedbackOut)
async def create_feedback_route(
        feedback_data: FeedbackCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    if feedback_data.type_feedback not in ['beer', 'place']:
        raise HTTPException(status_code=404, detail="Incorrect feedback type")

    place = None
    if feedback_data.place_id:
        place = db.query(Place).filter(
            Place.id == feedback_data.place_id).first()
        if place is None:
            raise HTTPException(status_code=404, detail="Place not found")

    beer = None
    if feedback_data.beer_id:
        beer = db.query(Beer).filter(Beer.id == feedback_data.beer_id).first()
        if beer is None:
            raise HTTPException(status_code=404, detail="Beer not found")

    feedback = Feedback(
        text=feedback_data.text,
        ratings=feedback_data.ratings,
        beer_id=beer.id if beer else None,
        user_id=current_user.id,
        place_id=place.id if place else None,
        type_feedback=feedback_data.type_feedback
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    update_user_level(current_user.id, db)

    for url in feedback_data.photo_urls:
        photo = Photo(photo_url=url, feedback_id=feedback.id)
        db.add(photo)

    db.commit()
    db.refresh(feedback)
    return FeedbackOut(
        id=feedback.id,
        text=feedback.text,
        ratings=feedback.ratings,
        type_feedback=feedback.type_feedback,
        photos=[PhotoOut(id=photo.id, photo_url=photo.photo_url)
                for photo in feedback.photos],
        user=UserReturnSchema.from_orm(current_user),
        beer=BeerOut.from_orm(beer) if beer else None,
        place=PlaceOut.from_orm(place) if place else None
    )


@router.get("/{feedback_id}", response_model=FeedbackOut)
def read_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if feedback is None:
        raise HTTPException(status_code=404, detail=f"Feedback with id {feedback_id} not found")

    return feedback


@router.get("", response_model=List[FeedbackOut])
def read_feedbacks(
        offset: int = 0,
        limit: int = 10,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "asc",
        text: Optional[str] = None,
        ratings_min: Optional[int] = None,
        ratings_max: Optional[int] = None,
        type_feedback: Optional[str] = None,
        db: Session = Depends(get_db)
):
    query = db.query(Feedback).options(
        joinedload(Feedback.user),
        joinedload(Feedback.photos),
        joinedload(Feedback.beer),
        joinedload(Feedback.place),
    )

    if text:
        query = query.filter(Feedback.text.ilike(f"%{text}%"))

    if ratings_min is not None:
        query = query.filter(Feedback.ratings >= ratings_min)

    if ratings_max is not None:
        query = query.filter(Feedback.ratings <= ratings_max)

    if type_feedback:
        if type_feedback not in ['beer', 'place']:
            raise HTTPException(
                status_code=404, detail="Incorrect feedback type")
        query = query.filter(Feedback.type_feedback == type_feedback)

    if sort_by:
        try:
            sort_column = getattr(Feedback, sort_by)
            query = query.order_by(
                sort_column.asc() if sort_order == "asc" else sort_column.desc())
        except AttributeError:
            raise HTTPException(status_code=404,
                                detail="Incorrect sort type, choose from: id, text, ratings, user_id, beer_id, place_id, type_feedback")

    feedbacks = query.offset(offset).limit(limit).all()

    if not feedbacks:
        raise HTTPException(status_code=404, detail="No feedbacks found")

    return [FeedbackOut.from_orm(feedback) for feedback in feedbacks]
