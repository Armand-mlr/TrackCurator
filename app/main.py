from fastapi import FastAPI
from app.routers import tracks

app = FastAPI(title="Crate API")
app.include_router(tracks.router)


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}