"""Immutable Datentyp und Konstruktoren (B1B, A1I)."""
from dataclasses import dataclass, replace
from typing import Mapping


@dataclass(frozen=True)
class Film:
    """Immutable data type: nach dem Erzeugen nicht mehr veränderbar."""
    id: int
    titel: str
    jahr: int
    genre: str
    regie: str
    bewertung: float
    stimmen: int
    dauer: int

    @property
    def jahrzehnt(self) -> int:
        return self.jahr // 10 * 10


def film_aus_zeile(zeile: Mapping[str, str]) -> Film:
    """Konstruktor: baut aus einer CSV-Zeile einen gültigen Film."""
    return Film(
        id=int(zeile["id"]),
        titel=zeile["titel"].strip(),
        jahr=int(zeile["jahr"]),
        genre=zeile["genre"].strip(),
        regie=zeile["regie"].strip(),
        bewertung=float(zeile["bewertung"]),
        stimmen=int(zeile["stimmen"]),
        dauer=int(zeile["dauer"]),
    )


def mit_bewertung(film: Film, bewertung: float) -> Film:
    """Gibt eine Kopie mit neuer Bewertung zurück – das Original bleibt unverändert."""
    return replace(film, bewertung=bewertung)
