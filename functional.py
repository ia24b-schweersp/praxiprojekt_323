"""Komponierbare Operatoren (B1B, C2A)."""
from functools import reduce
from typing import Callable, Iterable


def compose(*funktionen: Callable) -> Callable:
    """compose(f, g, h)(x) == f(g(h(x)))"""
    return reduce(lambda f, g: lambda x: f(g(x)), funktionen, lambda x: x)


def pipe(wert, *funktionen: Callable):
    """pipe(x, h, g, f) == f(g(h(x))) – liest sich von links nach rechts."""
    return reduce(lambda zwischenwert, funktion: funktion(zwischenwert), funktionen, wert)


def mittelwert(werte: Iterable[float]) -> float:
    werte = tuple(werte)
    return sum(werte) / len(werte) if werte else 0.0


def formatiere_laufzeit(minuten: int) -> str:
    return f"{minuten // 60} h {minuten % 60} min"
