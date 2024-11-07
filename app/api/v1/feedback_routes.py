import os
import pathlib
from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import config
from app.config import UPLOAD_FOLDER
from app.crud.test_crud import get_test_db, get_tests_db
from app.dependencies import get_db
from app.schemas.feedback_scheme import FeedbackOut, FeedbackCreate
from app.schemas.photo_scheme import PhotoOut
from app.schemas.test_scheme import TestOut
from models import Feedback, Photo

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
        db: Session = Depends(get_db)
):
    feedback = Feedback(
        text=feedback_data.text,
        ratings=feedback_data.ratings,
        user_id=feedback_data.user_id,
        beer_id=feedback_data.beer_id,
        place_id=feedback_data.place_id,
        type_feedback=feedback_data.type_feedback
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    for url in feedback_data.photo_urls:
        photo = Photo(photo_url=url, feedback_id=feedback.id)
        db.add(photo)

    db.commit()

    return FeedbackOut(
        id=feedback.id,
        text=feedback.text,
        ratings=feedback.ratings,
        user_id=feedback.user_id,
        beer_id=feedback.beer_id,
        place_id=feedback.place_id,
        type_feedback=feedback.type_feedback,
        photos=[PhotoOut(id=photo.id, photo_url=photo.photo_url) for photo in feedback.photos]
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
        sort_by: Optional[str] = None,  # Поле для сортировки
        sort_order: Optional[str] = "asc",  # Направление сортировки, по умолчанию "asc"
        text: Optional[str] = None,  # Фильтрация по тексту
        ratings_min: Optional[int] = None,  # Минимальный рейтинг
        ratings_max: Optional[int] = None,  # Максимальный рейтинг
        type_feedback: Optional[str] = None,  # Фильтрация по типу фидбека
        db: Session = Depends(get_db)
):
    query = db.query(Feedback)

    if text:
        query = query.filter(Feedback.text.ilike(f"%{text}%"))

    if ratings_min is not None:
        query = query.filter(Feedback.ratings >= ratings_min)

    if ratings_max is not None:
        query = query.filter(Feedback.ratings <= ratings_max)

    if type_feedback:
        query = query.filter(Feedback.type_feedback == type_feedback)

    if sort_by:
        if sort_order == "asc":
            query = query.order_by(getattr(Feedback, sort_by).asc())
        else:
            query = query.order_by(getattr(Feedback, sort_by).desc())

    feedbacks = query.offset(offset).limit(limit).all()

    if not feedbacks:
        raise HTTPException(status_code=404, detail="No feedbacks found")

    return feedbacks