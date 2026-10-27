"""Feature 1: Filmsuche (C2B, B1A deklarativ)."""
from functools import reduce
from typing import Callable

from models import Film

Bedingung = Callable[[Film], bool]


def titel_oder_regie_enthaelt(text: str) -> Bedingung:
    """Gibt eine Funktion zurück, die prüft, ob der Text im Titel oder in der Regie vorkommt."""
    gesucht = text.strip().lower()

    def pruefe(film: Film) -> bool:
        return gesucht in film.titel.lower() or gesucht in film.regie.lower()
    return pruefe


def hat_genre(genre: str) -> Bedingung:
    def pruefe(film: Film) -> bool:
        return not genre or film.genre == genre
    return pruefe


def addiere_dauer(summe: int, film: Film) -> int:
    return summe + film.dauer


def als_anzeige(film: Film) -> dict:
    return {"id": film.id, "titel": film.titel, "jahr": film.jahr, "genre": film.genre,
            "regie": film.regie, "bewertung": film.bewertung, "dauer": film.dauer}


def suche(filme, text: str = "", genre: str = "") -> tuple[Film, ...]:
    """Deklarativ: beschreibt WAS ein Treffer ist, nicht WIE die Schleife läuft."""
    passt_text = titel_oder_regie_enthaelt(text)   # Funktion in Variable gespeichert
    passt_genre = hat_genre(genre)
    nach_text = filter(passt_text, filme)          # filter
    return tuple(filter(passt_genre, nach_text))


def anzeige_zeilen(filme) -> list[dict]:
    return list(map(als_anzeige, filme))           # map


def gesamtlaufzeit(filme) -> int:
    return reduce(addiere_dauer, filme, 0)         # reduce
