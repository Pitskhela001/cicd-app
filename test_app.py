import pytest
from app import app, notes


@pytest.fixture(autouse=True)
def clear_notes():
    """Reset notes list before each test."""
    notes.clear()
    yield
    notes.clear()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_get_notes_empty(client):
    response = client.get("/notes")
    assert response.status_code == 200
    data = response.get_json()
    assert data["notes"] == []
    assert data["count"] == 0


def test_create_note(client):
    response = client.post("/notes", json={"content": "Buy groceries"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["content"] == "Buy groceries"
    assert data["id"] == 1


def test_create_note_missing_content(client):
    response = client.post("/notes", json={})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_note_empty_content(client):
    response = client.post("/notes", json={"content": "   "})
    assert response.status_code == 400


def test_get_notes_after_creation(client):
    client.post("/notes", json={"content": "First note"})
    client.post("/notes", json={"content": "Second note"})
    response = client.get("/notes")
    data = response.get_json()
    assert data["count"] == 2


def test_delete_note(client):
    client.post("/notes", json={"content": "To be deleted"})
    response = client.delete("/notes/1")
    assert response.status_code == 200


def test_delete_nonexistent_note(client):
    response = client.delete("/notes/999")
    assert response.status_code == 404
