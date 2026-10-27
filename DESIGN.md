# Design-Blatt (B1I): Feature „Empfehlungen“

## Deklarative Anforderungen
- Die Empfehlungsliste **enthält** nur Filme des gewählten Genres (leeres Genre = alle).
- Jeder Film **hat** einen Score = gewichtete Bewertung `v/(v+m)·R + m/(v+m)·C`.
- `m` **ist** der Median der Stimmen der Kandidaten, `C` **ist** ihre Durchschnittsbewertung.
- Die Liste **ist** absteigend nach Score sortiert und **enthält höchstens** `anzahl` Einträge.
- Bei leerer Kandidatenmenge **ist** das Ergebnis leer (kein Fehler).
- Die Eingabedaten **bleiben** unverändert.

## Datenfluss
```
tuple[Film]  (aus lade_filme, immutable)
   │  kandidaten(filme, genre)           -> tuple[Film]
   ▼
tuple[Film]
   │  bewerte_alle(filme)                -> tuple[(Film, float)]
   │     ├─ mindest_stimmen(filme)       -> int    (m)
   │     ├─ durchschnitt_bewertung(...)  -> float  (C)
   │     └─ gewichtete_bewertung(f,m,c)  -> float  (pro Film)
   ▼
tuple[(Film, float)]
   │  beste(anzahl)(bewertete)           -> tuple[(Film, float)]
   ▼
Template empfehlungen.html
```

## Geplante Operatoren
| Operator | Zweck |
|---|---|
| `filter` (Generator in `kandidaten`) | Genre-Auswahl |
| `map` (Generator in `bewerte_alle`) | Film → (Film, Score) |
| `sorted(key=itemgetter(1))` | Sortierung nach Score |
| Slice `[:anzahl]` | Begrenzung |
| `pipe` (functional.py) | Komposition der Schritte zu einem Ablauf |
| Closure `beste(anzahl)` | Parametrisierte Funktion für die Pipeline |
