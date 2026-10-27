"""D1I: Das Refactoring verändert das Verhalten nicht."""
from bericht import genre_bericht, klassifiziere
from data_access import baue_index, lade_filme
from legacy import bericht as bericht_alt
from legacy import finde_film as finde_film_alt
from models import Film

FILME = lade_filme()


def test_bericht_gleich_wie_vorher():
    assert genre_bericht(FILME) == bericht_alt(FILME)


def test_bericht_leere_liste():
    assert genre_bericht(()) == bericht_alt(()) == []


def test_bericht_gleichstand_reihenfolge():
    filme = (Film(1, "a", 2000, "B", "x", 8.0, 1, 60), Film(2, "b", 2000, "A", "x", 8.0, 1, 60))
    assert genre_bericht(filme) == bericht_alt(filme)


def test_klassifizierung_grenzen():
    assert klassifiziere(8.0) == "Top"
    assert klassifiziere(7.99) == "Solide"
    assert klassifiziere(7.0) == "Solide"
    assert klassifiziere(6.99) == "Schwach"


def test_index_gleich_wie_lineare_suche():
    index = baue_index(FILME)
    for film_id in (1, 16, 32, 999):
        assert index.get(film_id) == finde_film_alt(FILME, film_id)
