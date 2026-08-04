from fastapi import FastAPI, HTTPException, Query

app = FastAPI(
    title="TrackCurator",
    description="Gestion de bacs à disques pour DJ", 
    version="0.1.0",
)

@app.get("/health")
def health():
    return {"status": "ok"}

FAKE_TRACKS = [
    {"id": 1, "titre": "Strings of Life", "bpm": 122, "genre": "house"},
    {"id": 2, "titre": "Windowlicker", "bpm": 96, "genre": "electronica"},
]

@app.get("/tracks")
def liste_tracks(
    genre: str | None = None,
    bpm_min: int = Query(default=0, ge=0, le=300),
    bpm_max: int = Query(default=300, ge=0, le=300)):
    rows = FAKE_TRACKS
    if genre: 
        rows = [t for t in rows if t["genre"] == genre]
    return [t for t in rows if bpm_min <= t["bpm"] <= bpm_max]


@app.get("/tracks/{track_id}")
def get_track(track_id: int):
    for t in FAKE_TRACKS :
        if t["id"] == track_id :
            return t
    raise HTTPException(status_code=404, detail="Morceau introuvable")
    