"""Feature 3: Ranking (C2A) – benutzerdefinierte Sortierung, Aggregation, Komposition."""
from functools import partial, reduce
from operator import attrgetter, itemgetter

from functional import compose

SORTIERKRITERIEN = {
    "bewertung": attrgetter("bewertung"),
    "stimmen": attrgetter("stimmen"),
    "jahr": attrgetter("jahr"),
    "dauer": attrgetter("dauer"),
    "titel": lambda film: film.titel.lower(),
}


def sortiere(filme, kriterien: list[str], absteigend: bool = True) -> tuple:
    """Mehrstufige Sortierung: Python sortiert stabil, darum vom letzten zum ersten Kriterium."""
    gueltige = [k for k in kriterien if k in SORTIERKRITERIEN] or ["bewertung"]
    return reduce(
        lambda zwischenstand, kriterium: tuple(sorted(zwischenstand, key=SORTIERKRITERIEN[kriterium],
                                                      reverse=absteigend)),
        reversed(gueltige),
        tuple(filme),
    )


def _sammle(gruppen: dict, film) -> dict:
    anzahl, summe, stimmen = gruppen.get(film.regie, (0, 0.0, 0))
    return {**gruppen, film.regie: (anzahl + 1, summe + film.bewertung, stimmen + film.stimmen)}


def regie_aggregation(filme) -> tuple[dict, ...]:
    """Aggregiert pro Regie: Anzahl Filme, Durchschnittsbewertung, Stimmen total."""
    gruppen = reduce(_sammle, filme, {})
    return tuple(
        {"regie": regie, "anzahl": anzahl, "schnitt": round(summe / anzahl, 2), "stimmen": stimmen}
        for regie, (anzahl, summe, stimmen) in gruppen.items()
    )


def nur_mehrfach(eintraege) -> tuple[dict, ...]:
    return tuple(e for e in eintraege if e["anzahl"] > 1)


def nach_schnitt_und_anzahl(eintraege) -> tuple[dict, ...]:
    return tuple(sorted(eintraege, key=itemgetter("schnitt", "anzahl"), reverse=True))


def top(n: int, eintraege) -> tuple:
    return tuple(eintraege)[:n]


# Komposition: wird von rechts nach links ausgeführt
top_regie = compose(partial(top, 5), nach_schnitt_und_anzahl, nur_mehrfach, regie_aggregation)
