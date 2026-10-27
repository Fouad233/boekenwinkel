from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import get_db
from models import Book, Reservation, User
from security import get_current_user

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)


class ReservationCreate(BaseModel):
    book_id: int
    quantity: int = Field(gt=0)


class ReservationResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    quantity: int
    status: str

    model_config = {"from_attributes": True}


@router.post(
    "/",
    response_model=ReservationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_reservation(
    reservation_data: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    book = (
        db.query(Book)
        .filter(Book.id == reservation_data.book_id)
        .with_for_update()
        .first()
    )

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    if book.stock < reservation_data.quantity:
        raise HTTPException(
            status_code=400,
            detail="Not enough books in stock"
        )

    book.stock -= reservation_data.quantity

    reservation = Reservation(
        user_id=current_user.id,
        book_id=book.id,
        quantity=reservation_data.quantity,
        status="reserved"
    )

    db.add(reservation)

    try:
        db.commit()
        db.refresh(reservation)
    except Exception:
        db.rollback()
        raise

    return reservation


@router.get("/", response_model=list[ReservationResponse])
def get_my_reservations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(Reservation)
        .filter(Reservation.user_id == current_user.id)
        .order_by(Reservation.id)
        .all()
    )