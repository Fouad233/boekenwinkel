from fastapi import FastAPI

from database import engine, Base
import models
from routers.books import router as books_router

app = FastAPI(title="Boekenwinkel API")

Base.metadata.create_all(bind=engine)

app.include_router(books_router)


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