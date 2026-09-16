from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/tracks", tags=["tracks"])

FAKE_TRACKS = [
    {"id": 1, "titre": "Strings of Life", "bpm": 122, "genre": "house"},
    {"id": 2, "titre": "Windowlicker", "bpm": 96, "genre": "electronica"},
]


@router.get("")
def list_tracks(
    genre: str | None = None,
    bpm_min: int = Query(default=0, ge=0, le=300),
    bpm_max: int = Query(default=300, ge=0, le=300),
):
    rows = FAKE_TRACKS
    if genre:
        rows = [t for t in rows if t["genre"] == genre]
    return [t for t in rows if bpm_min <= t["bpm"] and t["bpm"] <= bpm_max]


@router.get("/{track_id}")
def get_track(track_id: int):
    for t in FAKE_TRACKS:
        if t["id"] == track_id:
            return t
    raise HTTPException(status_code=404, detail="Morceau introuvable")

@router.post("")
def post_track(track : dict):
    track["id"] = max((t["id"] for t in FAKE_TRACKS), default=0) + 1
    FAKE_TRACKS.append(track)
    return track

@router.get("/search")
def search(q : str):
    return [track for track in FAKE_TRACKS if q.lower() in track["titre"].lower()]
    