from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import get_db
from models import Purchase, Review, User
from security import get_current_user

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)


class ReviewCreate(BaseModel):
    book_id: int
    score: int = Field(ge=1, le=5)
    text: str = Field(min_length=1, max_length=2000)


@router.post("/")
def create_review(
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    purchase = (
        db.query(Purchase)
        .filter(
            Purchase.user_id == current_user.id,
            Purchase.book_id == review_data.book_id
        )
        .first()
    )

    if purchase is None:
        raise HTTPException(
            status_code=403,
            detail="You can only review books you have purchased"
        )

    review = Review(
        user_id=current_user.id,
        book_id=review_data.book_id,
        score=review_data.score,
        text=review_data.text
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return {
        "id": review.id,
        "book_id": review.book_id,
        "score": review.score,
        "text": review.text
    }


@router.get("/book/{book_id}")
def get_book_reviews(
    book_id: int,
    db: Session = Depends(get_db)
):
    reviews = (
        db.query(Review)
        .filter(Review.book_id == book_id)
        .order_by(Review.id.desc())
        .all()
    )

    return [
        {
            "id": review.id,
            "user_id": review.user_id,
            "score": review.score,
            "text": review.text
        }
        for review in reviews
    ]