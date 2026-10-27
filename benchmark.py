"""D1A: Messung vorher/nachher. Start: python benchmark.py"""
from dataclasses import replace
from timeit import timeit

from bericht import genre_bericht
from data_access import baue_index, lade_filme
from legacy import bericht as bericht_alt
from legacy import finde_film as finde_film_alt

ANZAHL_FILME = 20_000
ANZAHL_GENRES = 200
WIEDERHOLUNGEN = 5


def gross_datensatz():
    basis = lade_filme()
    return tuple(replace(basis[i % len(basis)], id=i, genre=f"Genre {i % ANZAHL_GENRES}")
                 for i in range(ANZAHL_FILME))


def messe(name, funktion):
    sekunden = timeit(funktion, number=WIEDERHOLUNGEN) / WIEDERHOLUNGEN
    print(f"{name:<42} {sekunden * 1000:9.2f} ms")
    return sekunden


if __name__ == "__main__":
    filme = gross_datensatz()
    print(f"{ANZAHL_FILME} Filme, {ANZAHL_GENRES} Genres, Mittel aus {WIEDERHOLUNGEN} Läufen\n")

    alt = messe("Genre-Bericht vorher (legacy)", lambda: bericht_alt(filme))
    neu = messe("Genre-Bericht nachher (dict, 1 Durchlauf)", lambda: genre_bericht(filme))
    print(f"-> Faktor {alt / neu:.1f}x schneller\n")

    ids = range(0, ANZAHL_FILME, 20)  # 1000 Abfragen
    index = baue_index(filme)
    alt = messe("1000 Lookups lineare Suche (Liste)", lambda: [finde_film_alt(filme, i) for i in ids])
    neu = messe("1000 Lookups Index (dict)", lambda: [index.get(i) for i in ids])
    print(f"-> Faktor {alt / neu:.1f}x schneller")
