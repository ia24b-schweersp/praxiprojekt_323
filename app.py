"""CineStats – Flask-Praxisprojekt M323 Funktional Programmieren."""
from flask import Flask, abort, render_template, request

from bericht import genre_bericht
from data_access import baue_index, lade_filme
from empfehlung import empfehlungen
from functional import formatiere_laufzeit
from models import Film
from paradigmen import (bonus_immutable, bonus_mutierend, formatiere_film, genre_durchschnitt_funktional,
                        genre_durchschnitt_oo, genre_durchschnitt_prozedural)
from ranking import SORTIERKRITERIEN, regie_aggregation, sortiere, top_regie
from statistik import kennzahlen
from suche import anzeige_zeilen, gesamtlaufzeit, suche

app = Flask(__name__)

FILME = lade_filme()
INDEX = baue_index(FILME)
GENRES = tuple(sorted({film.genre for film in FILME}))


@app.route("/")
def suche_route():
    """Deklarative Variante (B1A, C2B)."""
    text = request.args.get("q", "")
    genre = request.args.get("genre", "")
    treffer = suche(FILME, text, genre)
    return render_template("suche.html", filme=anzeige_zeilen(treffer), genres=GENRES, q=text,
                           genre=genre, laufzeit=formatiere_laufzeit(gesamtlaufzeit(treffer)),
                           modus="deklarativ")


@app.route("/imperativ/suche")
def suche_imperativ_route():
    """Imperative Variante derselben Route (B1A) – nur zum Vergleich."""
    text = request.args.get("q", "")
    genre = request.args.get("genre", "")
    gesucht = text.strip().lower()
    zeilen = []
    minuten = 0
    for film in FILME:
        if gesucht not in film.titel.lower() and gesucht not in film.regie.lower():
            continue
        if genre != "" and film.genre != genre:
            continue
        zeilen.append({"id": film.id, "titel": film.titel, "jahr": film.jahr, "genre": film.genre,
                       "regie": film.regie, "bewertung": film.bewertung, "dauer": film.dauer})
        minuten = minuten + film.dauer
    laufzeit = str(minuten // 60) + " h " + str(minuten % 60) + " min"
    return render_template("suche.html", filme=zeilen, genres=GENRES, q=text, genre=genre,
                           laufzeit=laufzeit, modus="imperativ")


@app.route("/statistik")
def statistik_route():
    return render_template("statistik.html", k=kennzahlen(FILME))


@app.route("/ranking")
def ranking_route():
    kriterien = request.args.getlist("kriterium") or ["bewertung", "stimmen"]
    absteigend = request.args.get("richtung", "ab") == "ab"
    return render_template("ranking.html", filme=sortiere(FILME, kriterien, absteigend),
                           kriterien=kriterien, alle_kriterien=tuple(SORTIERKRITERIEN),
                           absteigend=absteigend, top=top_regie(FILME),
                           regie=sorted(regie_aggregation(FILME), key=lambda e: e["regie"]))


@app.route("/empfehlungen")
def empfehlungen_route():
    genre = request.args.get("genre", "")
    anzahl = request.args.get("anzahl", 5, type=int)
    return render_template("empfehlungen.html", liste=empfehlungen(FILME, genre, anzahl),
                           genres=GENRES, genre=genre, anzahl=anzahl)


@app.route("/bericht")
def bericht_route():
    return render_template("bericht.html", zeilen=genre_bericht(FILME))


@app.route("/paradigmen")
def paradigmen_route():
    beispiel = FILME[:3]
    als_dicts = [{"titel": f.titel, "bewertung": f.bewertung} for f in beispiel]
    vorher = [d["bewertung"] for d in als_dicts]
    bonus_mutierend(als_dicts, 0.5)
    neue = bonus_immutable(beispiel, 0.5)
    return render_template(
        "paradigmen.html",
        formatiert=list(map(formatiere_film, beispiel)),
        mutation={"vorher": vorher, "nachher": [d["bewertung"] for d in als_dicts]},
        immutable={"original": [f.bewertung for f in beispiel], "kopie": [f.bewertung for f in neue]},
        prozedural=genre_durchschnitt_prozedural(FILME),
        oo=genre_durchschnitt_oo(FILME),
        funktional=genre_durchschnitt_funktional(FILME),
    )


@app.route("/film/<int:film_id>")
def film_route(film_id: int):
    film: Film | None = INDEX.get(film_id)  # O(1) dank Index (D1A)
    if film is None:
        abort(404)
    return render_template("film.html", film=film)


if __name__ == "__main__":
    app.run(debug=True)
