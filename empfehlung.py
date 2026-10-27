"""Feature 4: Empfehlungen (C1B, C1I, C1A).

Algorithmus "gewichtete Bewertung" (wie bei IMDb):
    WR = v / (v + m) * R + m / (v + m) * C
    R = Bewertung des Films, v = Stimmen des Films,
    m = Mindeststimmen (Median), C = Durchschnittsbewertung aller Kandidaten
Filme mit wenigen Stimmen werden so zum Durchschnitt hin gezogen.
"""
from operator import itemgetter
from statistics import median_low

from functional import mittelwert, pipe
from models import Film


def kandidaten(filme, genre: str = "") -> tuple[Film, ...]:
    return tuple(f for f in filme if not genre or f.genre == genre)


def durchschnitt_bewertung(filme) -> float:
    return mittelwert(f.bewertung for f in filme)


def mindest_stimmen(filme) -> int:
    return median_low(f.stimmen for f in filme) if filme else 0


def gewichtete_bewertung(film: Film, m: int, c: float) -> float:
    v = film.stimmen
    if v + m == 0:
        return c
    return v / (v + m) * film.bewertung + m / (v + m) * c


def bewerte_alle(filme) -> tuple[tuple[Film, float], ...]:
    m, c = mindest_stimmen(filme), durchschnitt_bewertung(filme)
    return tuple((film, round(gewichtete_bewertung(film, m, c), 2)) for film in filme)


def beste(anzahl: int):
    def auswahl(bewertete):
        return tuple(sorted(bewertete, key=itemgetter(1), reverse=True)[:max(anzahl, 0)])
    return auswahl


def empfehlungen(filme, genre: str = "", anzahl: int = 5) -> tuple[tuple[Film, float], ...]:
    """Komposition der Teilfunktionen zu einem Ablauf."""
    return pipe(filme,
                lambda alle: kandidaten(alle, genre),
                bewerte_alle,
                beste(anzahl))
