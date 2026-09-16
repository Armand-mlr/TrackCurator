from fastapi import FastAPI
from app.routers import tracks

app = FastAPI(
    title="TrackCurator API",
    description="Gestion de bacs a disques pour DJ",
    version="0.1.0",
)
app.include_router(tracks.router)


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}