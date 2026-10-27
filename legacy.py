"""Alter Code VOR dem Refactoring (D1I, D1A). Bleibt nur für Tests und Benchmark erhalten."""


def bericht(l):
    r = []
    g = []
    for x in l:
        if x.genre not in g:
            g.append(x.genre)
    for gg in g:
        s = 0
        n = 0
        d = 0
        for x in l:
            if x.genre == gg:
                s = s + x.bewertung
                n = n + 1
                d = d + x.dauer
        if n > 0:
            if s / n >= 8.0:
                k = "Top"
            else:
                if s / n >= 7.0:
                    k = "Solide"
                else:
                    k = "Schwach"
            r.append({"genre": gg, "anzahl": n, "schnitt": round(s / n, 2),
                      "laufzeit_h": round(d / 60, 1), "klasse": k})
    r.sort(key=lambda e: e["schnitt"], reverse=True)
    return r


def finde_film(filme, film_id):
    for f in filme:
        if f.id == film_id:
            return f
    return None
