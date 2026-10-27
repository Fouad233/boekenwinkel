from fastapi import FastAPI

from database import engine, Base
import models

app = FastAPI(title="Boekenwinkel API")

# Create the database tables
Base.metadata.create_all(bind=engine)


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