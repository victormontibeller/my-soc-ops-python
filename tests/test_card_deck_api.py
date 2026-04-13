import pytest
from fastapi.testclient import TestClient

from app.data import QUESTIONS
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestStartCardDeck:
    def test_start_card_deck_returns_200(self, client: TestClient):
        client.get("/")
        response = client.post("/start-card-deck")
        assert response.status_code == 200

    def test_start_card_deck_returns_draw_button(self, client: TestClient):
        client.get("/")
        response = client.post("/start-card-deck")
        assert "Draw a Card" in response.text

    def test_start_card_deck_shows_cards_remaining(self, client: TestClient):
        client.get("/")
        response = client.post("/start-card-deck")
        assert "24" in response.text


class TestDrawCard:
    def test_draw_card_returns_200(self, client: TestClient):
        client.get("/")
        client.post("/start-card-deck")
        response = client.post("/card-deck/draw")
        assert response.status_code == 200

    def test_draw_card_shows_card_text(self, client: TestClient):
        client.get("/")
        client.post("/start-card-deck")
        response = client.post("/card-deck/draw")
        found = any(question in response.text for question in QUESTIONS)
        assert found, "Expected at least one question from QUESTIONS to appear in the drawn card response"

    def test_draw_card_decrements_count(self, client: TestClient):
        client.get("/")
        client.post("/start-card-deck")
        response = client.post("/card-deck/draw")
        assert "23" in response.text


class TestResetCardDeck:
    def test_reset_card_deck_returns_200(self, client: TestClient):
        client.get("/")
        client.post("/start-card-deck")
        response = client.post("/card-deck/reset")
        assert response.status_code == 200

    def test_reset_card_deck_returns_start_screen(self, client: TestClient):
        client.get("/")
        client.post("/start-card-deck")
        response = client.post("/card-deck/reset")
        assert "Start Game" in response.text
