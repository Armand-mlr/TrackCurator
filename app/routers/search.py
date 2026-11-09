from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Track
from app.schemas import TrackOut
from app.services import deezer

router = APIRouter(tags=["search"])

@router.get("/search")
async def search_tracks(q: str = Query(min_length=2), limit: int = Query(10, le=25)):
    try:
        return await deezer.search_cached(q, limit)
    except deezer.DeezerError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

@router.post("/tracks/import/{deezer_id}", response_model=TrackOut, status_code=201)
async def import_track(
    deezer_id: int, genre: str | None = None, db: Session = Depends(get_db)
):
    existing = db.scalar(select(Track).where(Track.deezer_id == deezer_id))
    if existing:
        return existing

    try:
        data = await deezer.track_detail(deezer_id)
    except deezer.DeezerError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    track = Track(**data, genre=genre)
    db.add(track)
    db.commit()
    db.refresh(track)
    return track