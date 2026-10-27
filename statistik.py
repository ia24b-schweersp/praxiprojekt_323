"""Feature 2: Statistik-Seite (C2I) – Lambdas und verkettetes map/filter/reduce."""
from functools import reduce


def durchschnitt_wo(filme, bedingung) -> float:
    """Durchschnittsbewertung aller Filme, die die Bedingung (eine Funktion) erfüllen."""
    bewertungen = tuple(map(lambda f: f.bewertung, filter(bedingung, filme)))
    if not bewertungen:
        return 0.0
    return round(reduce(lambda a, b: a + b, bewertungen) / len(bewertungen), 2)


def durchschnitt_ab_jahr(filme, ab_jahr: int = 2000) -> float:
    return durchschnitt_wo(filme, lambda f: f.jahr >= ab_jahr)


def stunden_lange_filme(filme, min_minuten: int = 150) -> float:
    """Summe der Laufzeit (in Stunden) aller Filme, die mindestens min_minuten dauern."""
    return round(reduce(lambda summe, stunden: summe + stunden,
                        map(lambda f: f.dauer / 60,
                            filter(lambda f: f.dauer >= min_minuten, filme)),
                        0.0), 2)


def stimmen_pro_jahrzehnt(filme) -> dict[int, int]:
    jahrzehnte = sorted(set(map(lambda f: f.jahrzehnt, filme)))
    return {
        jahrzehnt: reduce(lambda summe, f: summe + f.stimmen,
                          filter(lambda f, j=jahrzehnt: f.jahrzehnt == j, filme), 0)
        for jahrzehnt in jahrzehnte
    }


def kennzahlen(filme) -> dict:
    return {
        "anzahl": len(filme),
        "schnitt_ab_2000": durchschnitt_ab_jahr(filme, 2000),
        "schnitt_vor_2000": durchschnitt_wo(filme, lambda f: f.jahr < 2000),
        "stunden_ueberlange": stunden_lange_filme(filme),
        "stimmen_pro_jahrzehnt": stimmen_pro_jahrzehnt(filme),
    }
