from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Track
from app.schemas import TrackCreate, TrackOut

router = APIRouter(prefix="/tracks", tags=["tracks"])


@router.post("", response_model=TrackOut, status_code=status.HTTP_201_CREATED)
def create_track(payload: TrackCreate, db: Session = Depends(get_db)):
    track = Track(**payload.model_dump())
    db.add(track)
    db.commit()
    db.refresh(track)
    return track


@router.get("", response_model=list[TrackOut])
def list_tracks(db: Session = Depends(get_db)):
    return db.scalars(select(Track).order_by(Track.cree_le.desc())).all()


@router.get("/{track_id}", response_model=TrackOut)
def get_track(track_id: int, db: Session = Depends(get_db)):
    track = db.get(Track, track_id)
    if track is None:
        raise HTTPException(status_code=404, detail="Morceau introuvable")
    return track


@router.delete("/{track_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_track(track_id: int, db: Session = Depends(get_db)):
    track = db.get(Track, track_id)
    if track is None:
        raise HTTPException(status_code=404, detail="Morceau introuvable")
    db.delete(track)
    db.commit()