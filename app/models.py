from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Table, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

crate_tracks = Table(
    "crate_tracks",
    Base.metadata,
    Column("crate_id", ForeignKey("crates.id", ondelete="CASCADE"), primary_key=True),
    Column("track_id", ForeignKey("tracks.id", ondelete="CASCADE"), primary_key=True),
)


class Track(Base):
    __tablename__ = "tracks"

    id: Mapped[int] = mapped_column(primary_key=True)
    titre: Mapped[str] = mapped_column(String(200))
    artiste: Mapped[str] = mapped_column(String(200))
    bpm: Mapped[int | None] = mapped_column(default=None)
    duree_s: Mapped[int | None] = mapped_column(default=None)
    genre: Mapped[str | None] = mapped_column(String(60), index=True, default=None)
    deezer_id: Mapped[int | None] = mapped_column(unique=True, default=None)
    cree_le: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    crates: Mapped[list["Crate"]] = relationship(
        secondary=crate_tracks, back_populates="tracks"
    )


class Crate(Base):
    __tablename__ = "crates"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(80))
    description: Mapped[str | None] = mapped_column(String(300), default=None)

    tracks: Mapped[list[Track]] = relationship(
        secondary=crate_tracks, back_populates="crates"
    )