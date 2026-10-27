from dataclasses import FrozenInstanceError

import pytest

from data_access import baue_index, lade_filme
from empfehlung import empfehlungen, gewichtete_bewertung, mindest_stimmen
from functional import compose, pipe
from models import Film
from paradigmen import (bonus_immutable, bonus_mutierend, formatiere_film, genre_durchschnitt_funktional,
                        genre_durchschnitt_oo, genre_durchschnitt_prozedural)
from ranking import regie_aggregation, sortiere, top_regie
from statistik import durchschnitt_ab_jahr, stunden_lange_filme
from suche import gesamtlaufzeit, suche

FILME = lade_filme()


def film(id=1, titel="A", jahr=2000, genre="Drama", regie="X", bewertung=8.0, stimmen=100, dauer=120):
    return Film(id, titel, jahr, genre, regie, bewertung, stimmen, dauer)


# --- A1 ---
def test_pure_function_gleiche_eingabe_gleiche_ausgabe():
    f = film(titel="Alien", jahr=1979, bewertung=8.5)
    assert formatiere_film(f) == formatiere_film(f) == "Alien (1979) - 8.5"


def test_prozedur_hat_seiteneffekt(capsys):
    import paradigmen
    paradigmen.verarbeitete_filme = 0
    paradigmen.drucke_filmliste(FILME[:3])
    paradigmen.drucke_filmliste(FILME[:3])
    assert paradigmen.verarbeitete_filme == 6     # gleicher Input, anderer Zustand
    assert "The Shawshank Redemption (1994) - 9.3" in capsys.readouterr().out


def test_film_ist_immutable():
    with pytest.raises(FrozenInstanceError):
        film().bewertung = 1.0


def test_mutation_vs_immutable():
    dicts = [{"bewertung": 9.8}]
    bonus_mutierend(dicts, 0.5)
    assert dicts[0]["bewertung"] == 10.0          # Original verändert
    original = (film(bewertung=9.8),)
    neu = bonus_immutable(original, 0.5)
    assert original[0].bewertung == 9.8           # Original unverändert
    assert neu[0].bewertung == 10.0


def test_drei_paradigmen_liefern_gleiches_ergebnis():
    assert genre_durchschnitt_prozedural(FILME) == genre_durchschnitt_oo(FILME) == genre_durchschnitt_funktional(FILME)
    assert genre_durchschnitt_funktional(FILME)["Musical"] == 4.65    # (2.8 + 6.5) / 2
    assert genre_durchschnitt_funktional(FILME)["Western"] == 8.37    # (8.5 + 8.8 + 7.8) / 3


def test_drei_paradigmen_leere_liste():
    assert genre_durchschnitt_prozedural(()) == genre_durchschnitt_oo(()) == genre_durchschnitt_funktional(()) == {}


# --- B1 ---
def test_compose_und_pipe():
    plus1 = lambda x: x + 1
    mal2 = lambda x: x * 2
    assert compose(plus1, mal2)(3) == 7           # plus1(mal2(3))
    assert pipe(3, plus1, mal2) == 8              # mal2(plus1(3))


# --- C1 ---
def test_gewichtete_bewertung_beispiel():
    f = film(bewertung=9.0, stimmen=100)
    assert gewichtete_bewertung(f, m=100, c=7.0) == 8.0


def test_gewichtete_bewertung_edge_case_keine_stimmen():
    assert gewichtete_bewertung(film(stimmen=0), m=0, c=7.5) == 7.5


def test_empfehlungen_wenig_stimmen_werden_abgewertet():
    filme = (film(id=1, bewertung=9.9, stimmen=10), film(id=2, bewertung=8.5, stimmen=10000),
             film(id=3, bewertung=7.0, stimmen=5000))
    assert [f.id for f, _ in empfehlungen(filme, anzahl=3)][0] == 2


def test_empfehlungen_edge_cases():
    assert empfehlungen((), anzahl=5) == ()
    assert empfehlungen(FILME, genre="GibtEsNicht") == ()
    assert empfehlungen(FILME, anzahl=0) == ()
    assert mindest_stimmen(()) == 0


# --- C2B ---
def test_suche_filter_und_reduce():
    treffer = suche(FILME, "nolan")
    assert {f.titel for f in treffer} >= {"Inception", "Memento"}
    assert gesamtlaufzeit(()) == 0
    assert gesamtlaufzeit((film(dauer=100), film(dauer=20))) == 120


# --- C2I ---
def test_statistik():
    filme = (film(jahr=1990, bewertung=6.0), film(jahr=2005, bewertung=8.0), film(jahr=2010, bewertung=9.0))
    assert durchschnitt_ab_jahr(filme, 2000) == 8.5
    assert durchschnitt_ab_jahr(filme, 2050) == 0.0
    assert stunden_lange_filme((film(dauer=180), film(dauer=90)), 150) == 3.0


# --- C2A ---
def test_mehrstufige_sortierung():
    filme = (film(id=1, bewertung=8.0, stimmen=5), film(id=2, bewertung=9.0, stimmen=1),
             film(id=3, bewertung=8.0, stimmen=50))
    assert [f.id for f in sortiere(filme, ["bewertung", "stimmen"])] == [2, 3, 1]
    assert [f.id for f in sortiere(filme, ["unbekannt"], absteigend=False)] == [1, 3, 2]


def test_regie_aggregation_und_top():
    filme = (film(regie="A", bewertung=8.0), film(regie="A", bewertung=9.0), film(regie="B", bewertung=9.5))
    assert {"regie": "A", "anzahl": 2, "schnitt": 8.5, "stimmen": 200} in regie_aggregation(filme)
    assert [e["regie"] for e in top_regie(filme)] == ["A"]   # B hat nur einen Film


# --- D1A ---
def test_index():
    index = baue_index(FILME)
    assert index[5].titel == "Inception"
    assert index.get(999) is None
