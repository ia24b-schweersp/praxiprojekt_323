"""Laden der Daten und Index für schnelle Zugriffe (D1B, D1A)."""
import csv
from functools import lru_cache
from pathlib import Path
from types import MappingProxyType
from typing import Iterable, Mapping

from models import Film, film_aus_zeile

DATEI = Path(__file__).parent / "data" / "filme.csv"


@lru_cache(maxsize=None)
def lade_filme(pfad: str = str(DATEI)) -> tuple[Film, ...]:
    """Liest die CSV nur einmal ein (Memoization) und liefert ein unveränderliches Tupel."""
    with open(pfad, encoding="utf-8", newline="") as datei:
        return tuple(map(film_aus_zeile, csv.DictReader(datei)))


def baue_index(filme: Iterable[Film]) -> Mapping[int, Film]:
    """Dict-Index id -> Film: Zugriff in O(1) statt linearer Suche in O(n)."""
    return MappingProxyType({film.id: film for film in filme})
