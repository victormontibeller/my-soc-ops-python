import pytest
from fastapi.testclient import TestClient

from app.data import QUESTIONS
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestStartScavenger:
    def test_start_scavenger_returns_200(self, client: TestClient):
        client.get("/")
        response = client.post("/start-scavenger")
        assert response.status_code == 200

    def test_start_scavenger_returns_checklist(self, client: TestClient):
        client.get("/")
        response = client.post("/start-scavenger")
        # Progress indicator should show 0 out of 24 checked
        assert "0 / 24" in response.text or "0/24" in response.text

    def test_start_scavenger_returns_checklist_items(self, client: TestClient):
        client.get("/")
        response = client.post("/start-scavenger")
        # At least one question from the pool should appear in the response
        found = any(question in response.text for question in QUESTIONS)
        assert found, "Expected at least one question from QUESTIONS to appear in response"


class TestToggleScavengerItem:
    def test_toggle_scavenger_item_returns_200(self, client: TestClient):
        client.get("/")
        client.post("/start-scavenger")
        response = client.post("/scavenger/toggle/0")
        assert response.status_code == 200

    def test_toggle_scavenger_item_updates_progress(self, client: TestClient):
        client.get("/")
        client.post("/start-scavenger")
        response = client.post("/scavenger/toggle/0")
        # After toggling one item, progress should show 1 checked
        assert "1 / 24" in response.text or "1/24" in response.text


class TestResetScavenger:
    def test_reset_scavenger_returns_start_screen(self, client: TestClient):
        client.get("/")
        client.post("/start-scavenger")
        response = client.post("/scavenger/reset")
        assert response.status_code == 200
        assert "Start Game" in response.text
