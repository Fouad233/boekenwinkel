from fastapi import FastAPI

from database import engine, Base
import models
from routers.books import router as books_router
from dotenv import load_dotenv
load_dotenv()
from routers.users import router as users_router
from routers.reservations import router as reservations_router
from routers.purchases import router as purchases_router
from routers.reviews import router as reviews_router

app = FastAPI(title="Boekenwinkel API")

Base.metadata.create_all(bind=engine)

app.include_router(books_router)
app.include_router(users_router)
app.include_router(reservations_router)
app.include_router(purchases_router)
app.include_router(reviews_router)

@app.get("/")
def home():
    return {"message": "Welkom bij de Boekenwinkel API!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/database-status")
def database_status():
    return {
        "database": "connected",
        "tables": list(Base.metadata.tables.keys())
    }