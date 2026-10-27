from fastapi import FastAPI

app = FastAPI(title="Boekenwinkel API")


@app.get("/")
def home():
    return {"message": "Welkom bij de Boekenwinkel API!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}