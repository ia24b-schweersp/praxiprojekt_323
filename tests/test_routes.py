import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


@pytest.mark.parametrize("url", ["/", "/?q=nolan&genre=Action", "/imperativ/suche?q=nolan", "/statistik",
                                 "/ranking?kriterium=jahr&kriterium=titel&richtung=auf", "/empfehlungen?genre=Drama",
                                 "/bericht", "/paradigmen", "/film/1"])
def test_seiten_laden(client, url):
    assert client.get(url).status_code == 200


def test_unbekannter_film(client):
    assert client.get("/film/999").status_code == 404


def test_imperativ_und_deklarativ_gleich(client):
    deklarativ = client.get("/?q=spielberg").get_data(as_text=True)
    imperativ = client.get("/imperativ/suche?q=spielberg").get_data(as_text=True)
    assert deklarativ.replace("deklarativ", "X").replace("imperativ", "X").replace("/X/suche", "/") == \
        imperativ.replace("deklarativ", "X").replace("imperativ", "X").replace("/X/suche", "/")
