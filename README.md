# CineStats – M323 Praxisprojekt

Flask-App zur Analyse einer Filmdatenbank (`data/filme.csv`): Suche, Statistik, Ranking,
Empfehlungen, Genre-Bericht und ein Paradigmen-Vergleich.

## Starten
```
pip install -r requirements.txt
python app.py          # http://127.0.0.1:5000
python -m pytest       # Tests
python benchmark.py    # Performance-Messung (D1A)
```

## Kompetenzraster → Fundort im Code

| Feld | Pflicht-Artefakt | Fundort |
|---|---|---|
| **A1B** | Prozedur + pure function nebeneinander | `paradigmen.py`: `drucke_filmliste` vs. `formatiere_film` |
| **A1I** | Mutation + immutable Variante | `paradigmen.py`: `bonus_mutierend` vs. `bonus_immutable`; `models.py`: `@dataclass(frozen=True)`, `mit_bewertung` |
| **A1A** | gleiche Aufgabe OO / prozedural / funktional | `paradigmen.py`: `genre_durchschnitt_prozedural`, `GenreStatistik` + `genre_durchschnitt_oo`, `genre_durchschnitt_funktional`; Seite `/paradigmen` |
| **B1B** | Elemente Functional Design mit Fundort | immutable data type: `models.Film`; Konstruktor: `models.film_aus_zeile`; composable operators: `functional.compose`, `functional.pipe`; immutable Collections: `tuple`, `MappingProxyType` in `data_access.py` |
| **B1I** | Design-Blatt | `DESIGN.md` (Feature Empfehlungen) |
| **B1A** | imperative Route deklarativ umgesetzt | `app.py`: `suche_imperativ_route` (`/imperativ/suche`) vs. `suche_route` (`/`) + `suche.py`; Test `test_imperativ_und_deklarativ_gleich` |
| **C1B** | Algorithmus mit Beispieldurchlauf | `empfehlung.py` (gewichtete Bewertung, Formel im Docstring); Test `test_gewichtete_bewertung_beispiel`: R=9.0, v=100, m=100, C=7.0 → 8.0 |
| **C1I** | Algorithmus in Teilfunktionen mit Signaturen | `empfehlung.py`: `kandidaten`, `durchschnitt_bewertung`, `mindest_stimmen`, `gewichtete_bewertung`, `bewerte_alle`, `beste` |
| **C1A** | Komposition + Testfälle inkl. Edge Case | `empfehlung.empfehlungen` (mit `pipe`); Tests `test_empfehlungen_*`, `test_gewichtete_bewertung_edge_case_keine_stimmen` |
| **C2B** | Funktion in Variable, map/filter/reduce einzeln | **Feature Suche** – `suche.py`: `passt_text = titel_oder_regie_enthaelt(text)`, `filter` in `suche`, `map` in `anzeige_zeilen`, `reduce` in `gesamtlaufzeit` |
| **C2I** | Lambda + verkettetes map/filter/reduce | **Feature Statistik** – `statistik.py`: `durchschnitt_wo`, `stunden_lange_filme`, `stimmen_pro_jahrzehnt` |
| **C2A** | Aggregation / benutzerdef. Sortierung | **Feature Ranking** – `ranking.py`: `sortiere` (mehrstufig, vom User wählbar), `regie_aggregation` (reduce), `top_regie` (compose) |
| **D1B** | 3 Refactoring-Techniken + 2 Performance-Massnahmen | Docstring `bericht.py`: Extract Function, Rename Variable, Replace Magic Number with Constant; Performance: dict-Index (`data_access.baue_index`), Memoization (`@lru_cache` auf `lade_filme`), Ein-Durchlauf-Gruppierung |
| **D1I** | Vorher/Nachher, gleiches Verhalten per Test | vorher `legacy.bericht`, nachher `bericht.genre_bericht`; `tests/test_refactoring.py` |
| **D1A** | Messung vorher/nachher + Wahl Datenstruktur | `benchmark.py` (Beispielmessung: Bericht 201 ms → 8 ms, 1000 Lookups 401 ms → 0.12 ms); `dict` statt `list` für Gruppen und Index |

## Hinweis zu D1I (Commit-Historie)
Für D1I wird ein Vorher/Nachher **aus der Commit-Historie** verlangt. Empfohlener Ablauf:
1. Commit mit dem alten Stand (`legacy.bericht` wird in `/bericht` verwendet),
2. Commit mit dem Refactoring (`bericht.genre_bericht`), Tests grün.
