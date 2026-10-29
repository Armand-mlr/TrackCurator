from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Crate, Track
from app.schemas import TrackCreate, TrackOut, CrateCreate, CrateOut

router = APIRouter(prefix="/crates", tags=["crates"])

""" GET /crates	lister les bacs	liste éventuellement vide
POST /crates	créer un bac	201, valider le nom
GET /crates/{id}	un bac + ses morceaux	404 si absent ; renvoyer aussi ses tracks
POST /crates/{id}/tracks/{track_id}	ajouter un morceau à un bac	404 si l'un manque ; idempotent
DELETE /crates/{id}/tracks/{track_id} """

@router.get("", response_model=list[CrateOut])
def list_crates(db: Session = Depends(get_db)):
    return db.scalars(select(Crate)).all()

@router.post("", response_model=CrateOut, status_code=status.HTTP_201_CREATED)
def create_crate(payload: CrateCreate, db: Session = Depends(get_db)):
    crate = Crate(**payload.model_dump())
    db.add(crate)
    db.commit()
    db.refresh(crate)
    return crate

@router.get("/{crate_id}", response_model=CrateOut)
def get_crate(crate_id: int, db: Session = Depends(get_db)):
    crate = db.get(Crate, crate_id)
    if crate is None:
        raise HTTPException(status_code=404, detail="Bac introuvable")
    return crate

@router.post("/{crate_id}/tracks/{track_id}", response_model=CrateOut)
def add_track(crate_id: int, track_id: int, db: Session = Depends(get_db)):
    crate = db.get(Crate, crate_id)
    track = db.get(Track, track_id)
    if crate is None or track is None:
        raise HTTPException(status_code=404, detail="Bac ou morceau introuvable")
    if track not in crate.tracks:        # idempotent : pas de doublon
        crate.tracks.append(track)
        db.commit()
        db.refresh(crate)
    return crate


@router.delete("/{crate_id}/tracks/{track_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_track(crate_id: int, track_id: int, db: Session = Depends(get_db)):
    crate = db.get(Crate, crate_id)
    if crate is None:
        raise HTTPException(status_code=404, detail="Bac introuvable")
    track = db.get(Track, track_id)
    if track and track in crate.tracks:  # tolerant : retirer l'absent n'echoue pas
        crate.tracks.remove(track)
        db.commit()