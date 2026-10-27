from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Book, Purchase, Reservation, User
from security import get_current_user

router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"]
)


@router.post("/{reservation_id}/complete")
def complete_purchase(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    reservation = (
        db.query(Reservation)
        .filter(
            Reservation.id == reservation_id,
            Reservation.user_id == current_user.id
        )
        .with_for_update()
        .first()
    )

    if reservation is None:
        raise HTTPException(
            status_code=404,
            detail="Reservation not found"
        )

    if reservation.status != "reserved":
        raise HTTPException(
            status_code=400,
            detail="Reservation is already completed or cancelled"
        )

    reservation.status = "completed"

    for _ in range(reservation.quantity):
        purchase = Purchase(
            user_id=current_user.id,
            book_id=reservation.book_id
        )
        db.add(purchase)

    db.commit()

    return {"message": "Purchase completed successfully"}


@router.get("/me")
def get_my_purchases(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    purchases = (
        db.query(Purchase)
        .filter(Purchase.user_id == current_user.id)
        .all()
    )

    result = []

    for purchase in purchases:
        book = db.query(Book).filter(Book.id == purchase.book_id).first()

        if book:
            result.append({
                "purchase_id": purchase.id,
                "book_id": book.id,
                "title": book.title,
                "author": book.author
            })

    return result