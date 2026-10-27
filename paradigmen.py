"""Vergleich der Paradigmen (A1B, A1I, A1A)."""
from itertools import groupby
from operator import attrgetter

from functional import mittelwert
from models import Film, mit_bewertung

MAX_BEWERTUNG = 10.0

# --- A1B: Prozedur vs. pure function -------------------------------------

verarbeitete_filme = 0


def drucke_filmliste(filme) -> None:
    """Prozedur: kein Rückgabewert, Seiteneffekte (Konsole + globaler Zähler)."""
    global verarbeitete_filme
    for film in filme:
        print(f"{film.titel} ({film.jahr}) - {film.bewertung}")
        verarbeitete_filme += 1


def formatiere_film(film: Film) -> str:
    """Pure function: gleiche Eingabe -> gleiche Ausgabe, keine Seiteneffekte."""
    return f"{film.titel} ({film.jahr}) - {film.bewertung:.1f}"


# --- A1I: Mutation vs. immutable -----------------------------------------

def bonus_mutierend(filme: list[dict], bonus: float) -> None:
    """Verändert die übergebenen Dicts direkt – der Aufrufer sieht die Änderung."""
    for film in filme:
        film["bewertung"] = min(MAX_BEWERTUNG, film["bewertung"] + bonus)


def bonus_immutable(filme: tuple[Film, ...], bonus: float) -> tuple[Film, ...]:
    """Erzeugt neue Film-Objekte – die Originale bleiben unverändert."""
    return tuple(mit_bewertung(film, min(MAX_BEWERTUNG, film.bewertung + bonus)) for film in filme)


# --- A1A: dieselbe Aufgabe in drei Paradigmen ----------------------------
# Aufgabe: Durchschnittsbewertung pro Genre

def genre_durchschnitt_prozedural(filme) -> dict[str, float]:
    summen = {}
    anzahl = {}
    for film in filme:
        if film.genre not in summen:
            summen[film.genre] = 0.0
            anzahl[film.genre] = 0
        summen[film.genre] += film.bewertung
        anzahl[film.genre] += 1
    ergebnis = {}
    for genre in summen:
        ergebnis[genre] = round(summen[genre] / anzahl[genre], 2)
    return ergebnis


class GenreStatistik:
    """OO: Zustand (die Bewertungen) und Verhalten sind im Objekt gekapselt."""

    def __init__(self):
        self._bewertungen: dict[str, list[float]] = {}

    def hinzufuegen(self, film: Film) -> None:
        self._bewertungen.setdefault(film.genre, []).append(film.bewertung)

    def durchschnitte(self) -> dict[str, float]:
        return {genre: round(sum(werte) / len(werte), 2) for genre, werte in self._bewertungen.items()}

def genre_durchschnitt_funktional(filme) -> dict[str, float]:
    nach_genre = attrgetter("genre")
    gruppen = groupby(sorted(filme, key=nach_genre), key=nach_genre)
    return {genre: round(mittelwert(film.bewertung for film in gruppe), 2) for genre, gruppe in gruppen}

def genre_durchschnitt_oo(filme) -> dict[str, float]:
    statistik = GenreStatistik()
    for film in filme:
        statistik.hinzufuegen(film)
    return statistik.durchschnitte()



