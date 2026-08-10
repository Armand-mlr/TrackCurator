from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/tracks", tags=["tracks"])


@router.get("")
def list_tracks():
    return []


@router.get("/{track_id}")
def get_track(track_id: int):
    raise HTTPException(status_code=404, detail="Morceau introuvable")