"""Feature 5: Genre-Bericht NACH dem Refactoring (D1B, D1I, D1A).

Refactorings gegenüber legacy.bericht:
  - Extract Function: klassifiziere, gruppiere_nach_genre, genre_zeile
  - Rename Variable: l/r/g/s/n/d -> sprechende Namen
  - Replace Magic Number with Constant: TOP_GRENZE, SOLIDE_GRENZE
Performance:
  - ein Durchlauf (O(n)) statt verschachtelter Schleife (O(Genres * n))
  - dict statt Liste für die Genre-Gruppen (Lookup O(1) statt O(Genres))
"""
from operator import itemgetter

from models import Film

TOP_GRENZE = 8.0
SOLIDE_GRENZE = 7.0
MINUTEN_PRO_STUNDE = 60


def klassifiziere(schnitt: float) -> str:
    if schnitt >= TOP_GRENZE:
        return "Top"
    if schnitt >= SOLIDE_GRENZE:
        return "Solide"
    return "Schwach"


def gruppiere_nach_genre(filme) -> dict[str, tuple[Film, ...]]:
    """Lokale Mutation, nach aussen pure: Reihenfolge = erstes Auftreten des Genres."""
    gruppen: dict[str, list[Film]] = {}
    for film in filme:
        gruppen.setdefault(film.genre, []).append(film)
    return {genre: tuple(gruppe) for genre, gruppe in gruppen.items()}


def genre_zeile(genre: str, filme: tuple[Film, ...]) -> dict:
    anzahl = len(filme)
    schnitt = sum(f.bewertung for f in filme) / anzahl
    return {
        "genre": genre,
        "anzahl": anzahl,
        "schnitt": round(schnitt, 2),
        "laufzeit_h": round(sum(f.dauer for f in filme) / MINUTEN_PRO_STUNDE, 1),
        "klasse": klassifiziere(schnitt),
    }


def genre_bericht(filme) -> list[dict]:
    zeilen = (genre_zeile(genre, gruppe) for genre, gruppe in gruppiere_nach_genre(filme).items())
    return sorted(zeilen, key=itemgetter("schnitt"), reverse=True)
