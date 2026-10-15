from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TrackCreate(BaseModel):
    titre: str = Field(min_length=1, max_length=200)
    artiste: str = Field(min_length=1, max_length=200)
    bpm: int | None = Field(default=None, ge=40, le=250)
    duree_s: int | None = Field(default=None, ge=1)
    genre: str | None = None


class TrackOut(BaseModel):
    id: int
    titre: str
    artiste: str
    bpm: int | None
    duree_s: int | None
    genre: str | None
    cree_le: datetime

    model_config = ConfigDict(from_attributes=True)


class CrateCreate(BaseModel):
    nom: str = Field(min_length=1, max_length=80)
    description: str | None = None


class CrateOut(BaseModel):
    id: int
    nom: str
    description: str | None
    tracks: list[TrackOut] = []

    model_config = ConfigDict(from_attributes=True)